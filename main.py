import pdfplumber
import csv

# pdf_path = "SRIP Results 2025 _ SRIP.pdf"
# csv_path = "SRIP_Results_2025.csv"

# with pdfplumber.open(pdf_path) as pdf, open(csv_path, "w", newline="", encoding="utf-8") as csv_file:
#     writer = csv.writer(csv_file)
#     writer.writerow(["Intern ID", "Full Name", "Project Code"])  # Header row

#     for page in pdf.pages:
#         text = page.extract_text()
#         lines = text.split("\n")

#         for line in lines:
#             parts = line.split()
#             if len(parts) >= 3:
#                 intern_id = parts[0]
#                 full_name = " ".join(parts[1:-1])
#                 project_code = parts[-1]
#                 writer.writerow([intern_id, full_name, project_code])

# print(f"CSV saved as: {csv_path}")

import pandas as pd
df = pd.read_csv("SRIP_Results_2025.csv")
print(df.head())
df_grouped = df.groupby(["Intern ID", "Full Name"])["Project Code"].count().reset_index()

# Sort by most projects
df_sorted = df_grouped.sort_values(by="Project Code", ascending=False)
print(df_sorted.head())