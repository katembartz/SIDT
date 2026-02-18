import argparse
from pathlib import Path

import numpy as np
import sys
import csv
from datetime import datetime

from .sidt import sidt_alg

def main(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-path", type=Path, required=True, help="Path to csv file containing databank B")
    parser.add_argument("--tmp-dir", type=Path, default=None, help="Path to directory to store intermediate results")
    parser.add_argument("--tol-m", type=Path, default=None, help="Tolerance for mean")
    parser.add_argument("--tol-s", type=Path, default=None, help="Tolerance for standard deviation")
    parser.add_argument("--maxIter", type=Path, default=None, help="Maximum iterations to perform")
    parser.add_argument("--k", type=Path, required=True, help="Tolerance for regions out of distribution")
    parsed = parser.parse_args(args)
    
    if parsed.tmp_dir == None:
        now = datetime.now()
        formatted = now.strftime("%Y_%m_%d_%H_%M_%S")
        res_dir = Path(f"{str(Path.cwd())}/sidt_results_{formatted}")
        parsed.results_dir =  res_dir
        res_dir.mkdir(exist_ok=True)
        print(f'All intermediate results will be saved to {parsed.results_dir}')
        
    if parsed.tol_m == None:
        parsed.tol_m = 0.05
        
    if parsed.tol_s == None:
        parsed.tol_s = 0.05
        
    if parsed.maxIter == None:
        parsed.maxIter = 20
        
    parsed.tmp_dir.mkdir(exist_ok=True)
        
    if not str(parsed.data_path).lower().endswith(".csv"):
        raise ValueError(f"Specified data path must be a csv file. Check the readME for more information.")
    
    if not parsed.data_path.exists():
        raise FileNotFoundError(f"File does not exist: {parsed.data_path}")
    
    # SIDT
    print("===== Running sidt on database =====")
    sidt_alg(parsed.data_path, parsed.tmp_dir, parsed.tol_m, parsed.tol_s, parsed.maxIter, parsed.k)
    
if __name__ == "__main__":
    main()
