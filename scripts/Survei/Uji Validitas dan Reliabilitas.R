# Importing

library(readr)
library(psych)

# Menggunakan nama file yang diunggah sebelumnya (penyiaran_pretest.csv)
df_pretest <- read_csv('sample_pretest.csv')

df_pretest <- df_pretest[-1, ] 

# Subsetting featured dataset for pretest

items_list <- list(
  A = colnames(df_pretest)[18:21], # A1 sampai A4
  B = colnames(df_pretest)[22:28], # B1 sampai B7
  C = colnames(df_pretest)[29:33], # C1 sampai C5
  D = colnames(df_pretest)[34:37]  # D1 sampai D4
)

# Alias map 
alias_map <- c(
  setNames(paste0("A", 1:4), items_list$A),
  setNames(paste0("B", 1:7), items_list$B),
  setNames(paste0("C", 1:5), items_list$C),
  setNames(paste0("D", 1:4), items_list$D)
)

# Mendefinisikan struktur variabel
variable_map <- list(
  "V1: Ancaman/Kekhawatiran Kreator (A1-A4)" = list(items = items_list$A, alias = paste0("A", 1:4)),
  "V2: Kompetensi Pemerintah/DPR (B1-B7)" = list(items = items_list$B, alias = paste0("B", 1:7)),
  "V3: Manfaat RUU Penyiaran (C1-C5)" = list(items = items_list$C, alias = paste0("C", 1:5)),
  "V4: Persepsi terhadap Platform (D1-D4)" = list(items = items_list$D, alias = paste0("D", 1:4))
)

# Nilai Kritis Validitas (N=25, df=23, alpha=0.05)
N <- nrow(df_pretest) 
df_crit <- N - 2 
r_tabel <- qt(0.975, df_crit) / sqrt(df_crit + qt(0.975, df_crit)^2) 
# r_tabel = 0.396

cat(paste("Jumlah Responden (N):", N, "\n"))
cat(paste("Nilai Kritis Validitas (r_tabel, α=0.05, df=23):", round(r_tabel, 3), "\n"))
cat("----------------------------------------------------------\n")

# Membentuk fungsi analisis (tetap sama)

analyze_variable_R_by_name <- function(data, items_info, var_name, r_tabel) {
  items <- items_info$items # Sekarang item_info adalah list, sehingga $items valid
  alias <- items_info$alias # Sekarang item_info adalah list, sehingga $alias valid
  
  cat(paste("\n--- ANALISIS:", var_name, "---\n"))
  
  # Ambil subset data
  data_items <- data[, items]
  
  # Konversi Tipe Data menjadi Numerik 
  data_numeric <- as.data.frame(sapply(data_items, as.numeric))
  
  # Fungsi alpha akan berjalan lancar dengan data numerik
  alpha_result <- alpha(data_numeric)
  
  # Uji Validitas
  cat("HASIL VALIDITAS (Korelasi Item-Total, r_drop > 0.396):\n")
  
  validity_df <- data.frame(
    Alias = alias,
    r_drop = round(alpha_result$item.stats$r.drop, 3),
    Valid = ifelse(alpha_result$item.stats$r.drop > r_tabel, "YA", "TIDAK")
  )
  colnames(validity_df) <- c("Alias", "r_hitung", "Valid")
  print(validity_df, row.names = FALSE)
  
  # Item yang Valid
  valid_items_indices <- which(validity_df$Valid == "YA")
  valid_items_names <- items[valid_items_indices]
  
  # Uji Reliabilitas 
  cat("\nHASIL RELIABILITAS (hanya item yang Valid):\n")
  
  if (length(valid_items_names) > 1) {
    # Ambil data item yang valid (pastikan juga diubah ke numerik)
    data_valid_numeric <- as.data.frame(sapply(data[, valid_items_names], as.numeric))
    final_alpha_result <- alpha(data_valid_numeric)
    alpha_value <- final_alpha_result$total$raw_alpha
    
    reliability_status <- ifelse(alpha_value >= 0.70, "Reliabel (Baik)", 
                                 ifelse(alpha_value >= 0.60, "Reliabel (Dapat Diterima)", 
                                        "TIDAK Reliabel"))
    
    cat(paste("Cronbach's Alpha:", round(alpha_value, 3), "->", reliability_status, "\n"))
    valid_alias <- alias[validity_df$Valid == "YA"]
    cat(paste("Item Valid yang Digunakan:", paste(valid_alias, collapse = ", "), "\n"))
  } else {
    cat("Tidak dapat dihitung (jumlah item valid kurang dari 2).\n")
  }
  cat("----------------------------------------------------------\n")
}

# Jalankan Analisis untuk Setiap Variabel
# Iterasi Analisis

for (var_name in names(variable_map)) {
  analyze_variable_R_by_name(df_pretest, variable_map[[var_name]], var_name, r_tabel)
}