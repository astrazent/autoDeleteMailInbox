import pandas as pd

# Đọc file CSV
file_path = "temp/classifyGroup.csv"  # Đường dẫn tới file CSV
data = pd.read_csv(file_path)

# Kiểm tra xem cột email có tồn tại không
if 'Email' not in data.columns:
    raise ValueError("File CSV không chứa cột 'email'.")

# Nhóm các email giống nhau và đếm số lượng
data['Quantity'] = data.groupby('Email')['Email'].transform('count')

# Ghi kết quả vào file mới
output_file_path = "temp/addQuantity.csv"
data.to_csv(output_file_path, index=False)

print("Xác định số lượng các inbox/mail \u2713")
