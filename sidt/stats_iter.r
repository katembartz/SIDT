
args <- commandArgs(trailingOnly = TRUE)
path <- args[1]
data <- read.csv(path, sep = ",")
iter <- args[2]
region_path <- args[3]
tmp <- args[4]
print(dim(data))
regions <- read.csv(region_path, sep = ",")

mu_stats <- data.frame(region=character(0), avg=numeric(0))
std_stats <- data.frame(region=character(0), std=numeric(0))

for (i in 1:126) { 
  i = i + 1 # skip subjects
  numeric_data <- as.numeric(data[[i]])
  numeric_data <- numeric_data[!is.na(numeric_data)]

  curr_data <- numeric_data
  unfiltered <- data[[i]]
  label <- regions[i-1,1]

  stat <- boxplot.stats(curr_data)
  count <- 0
  filtered <- vector(mode = "numeric") 

  r <- length(curr_data)

  q1 <- quantile(curr_data, 0.25, na.rm = TRUE)
  q3 <- quantile(curr_data, 0.75, na.rm = TRUE)
  iqr <- q3 - q1
  lower <- q1 - 1.5 * iqr
  upper <- q3 + 1.5 * iqr
  filtered <- curr_data[curr_data >= lower & curr_data <= upper]
  
  curr_data <- filtered

  mu <- mean(curr_data)
  std <- sd(curr_data)
  mu_stats <- rbind(mu_stats, data.frame(region = label, avg = mu))
  std_stats <- rbind(std_stats, data.frame(region = label, std = std))
}

write.csv(mu_stats, file = paste0(tmp, "/", iter, "_mu_stats.csv"), row.names = FALSE)
write.csv(std_stats, file = paste0(tmp, "/", iter, "_sd_stats.csv"), row.names = FALSE)
print("saved metric files")
