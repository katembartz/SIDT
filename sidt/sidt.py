import pandas as pd
import numpy as np
import subprocess

def sidt_alg(path_data, tmp, tol_m, tol_s, maxIter, limit):
    # ---------------- INPUT ------------------------
    tmp = str(tmp)
    limit = int(str(limit))
    tol_m = float(str(tol_m))
    tol_s = float(str(tol_s))
    maxIter = int(str(maxIter))
    data = pd.read_csv(path_data)
    rho = data.columns # get ROIs
    pd.DataFrame(rho).to_csv(f'{tmp}/regions.csv', index=False, header=False)
    B = data.to_numpy()
    rows, cols = B.shape
    print(B.shape) # verify data inputted correctly
    rm_list = []
    rs_list = []

    # ---------------- INITIALIZATION ------------------------
    third = np.around(rows/10*3).astype(np.int64)
    B_curr = B[0:third, :] # grab first ~30% of image segmentations
    pd.DataFrame(B_curr).to_csv(tmp + '/B_curr.csv', index=False, header=False)
    subprocess.run(["Rscript", "sidt/stats_iter.r", f'{tmp}/B_curr.csv', '0', f'{tmp}/regions.csv', tmp],
                        check=True,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL)

    m_data = pd.read_csv(f"{tmp}/0_mu_stats.csv")
    m_curr_data = m_data.to_numpy()
    m_curr = m_curr_data[:,1]
    s_data = pd.read_csv(f"{tmp}/0_sd_stats.csv")
    s_curr_data = s_data.to_numpy()
    s_curr = s_curr_data[:,1]

    zeros = np.zeros(cols-1)
    r_m = zeros - m_curr
    r_s = zeros - s_curr
    j = 1
    B_curr = B

    # --------------------- ITERATION -----------------------

    def summarize_stats(mu, std, data):
        rows, cols = data.shape
        outliers = []

        for i in range(rows-1):
            i = i + 1
            count = 0
            for j in range(cols-1):
                j = j + 1
                curr = float(data[i,j])

                avg = float(mu[j-1])
                this_std = float(std[j-1])
                offset = round((curr - avg)/this_std,6) # determine offset

                if abs(offset) >= 3:
                    count = count + 1

            outliers.append(count)

        return outliers

    removed = []

    # initalize norms and differences
    curr_rm_norm = np.linalg.norm(r_m)
    curr_rs_norm = np.linalg.norm(r_s)
    diff_rm = 100

    rm_list.append(curr_rm_norm)
    rs_list.append(curr_rs_norm)

    all_removed = set()

    while (curr_rm_norm > tol_m or curr_rs_norm > tol_s) and j < maxIter and diff_rm > -0.5: 
        print(f"======Iteration {j}=======")

        last_rm_norm = curr_rm_norm.copy()
        last_rs_norm = curr_rs_norm.copy()

        print(f"Mean norm: {last_rm_norm}")
        print(f"Stdev norm: {last_rs_norm}")

        m_past = m_curr.copy()
        s_past = s_curr.copy()
        B_past = B_curr.copy()

        rows, cols = B_past.shape
        outliers = summarize_stats(m_past, s_past, B_past)

        B_curr = np.empty((0, 127)) 
        B_curr = np.vstack([B_curr, rho])
            
        current_removed = []

        for i in range(rows-1):
            subject = B_past[i+1,0]
            num = outliers[i]

            if num > limit and subject not in all_removed:
                current_removed.append(subject)
                all_removed.add(subject)
            else:
                B_curr = np.vstack([B_curr, B_past[i+1, :]])

        removed.append(current_removed)
        print(f"Size of matrix: {B_curr.shape}")

        # save B_curr as csv
        pd.DataFrame(B_curr).to_csv(tmp + '/B_curr.csv', index=False)

        # calculate statistics
        subprocess.run(["Rscript", "sidt/stats_iter.r", f'{tmp}/B_curr.csv', str(j), f'{tmp}/regions.csv', tmp],
                        check=True,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL)

        # get new mean and sd values
        m_data = pd.read_csv(f"{tmp}/{j}_mu_stats.csv")
        m_curr_data = m_data.to_numpy()
        m_curr = m_curr_data[:,1]
        s_data = pd.read_csv(f"{tmp}/{j}_sd_stats.csv")
        s_curr_data = s_data.to_numpy()
        s_curr = s_curr_data[:,1]

        # update residual vectors
        r_m = m_curr - m_past
        r_s = s_curr - s_past

        # update norms and save
        curr_rm_norm = np.linalg.norm(r_m)
        curr_rs_norm = np.linalg.norm(r_s)
        rm_list.append(curr_rm_norm)
        rs_list.append(curr_rs_norm)

        # calculate change
        diff_rm = last_rm_norm - curr_rm_norm

        j = j + 1

    print(f"EXITED LOOP at j = {j-1}")

    pd.DataFrame(removed).to_csv(tmp + '/removed.csv', index=True, header=False)

    m_curr = pd.read_csv(f"{tmp}/{j-1}_mu_stats.csv")
    s_curr = pd.read_csv(f"{tmp}/{j-1}_sd_stats.csv")

    pd.DataFrame(m_curr).to_csv(tmp + '/final_mean.csv', index=False, header=True)
    pd.DataFrame(s_curr).to_csv(tmp + '/final_sd.csv', index=False, header=True)
    pd.DataFrame(rm_list).to_csv(tmp + '/rm_norm.csv', index=False, header=False)
    pd.DataFrame(rs_list).to_csv(tmp + '/rs_norm.csv', index=False, header=False)