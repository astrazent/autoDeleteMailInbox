import pandas as pd
import warnings

# Tắt cảnh báo UserWarning (không tắt tất cả các cảnh báo)
warnings.filterwarnings("ignore", category=UserWarning)

# Đọc dữ liệu từ file CSV
df = pd.read_csv('temp/addCountSimilarAndRatio.csv')

# Chuyển đổi cột 'Date' thành định dạng datetime
df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y', errors='coerce')

# Lấy danh sách tất cả các email trong cột 'Email'
emails = df['Email'].unique()

# Tạo cột mới để lưu tần suất gửi trung bình (lần/tháng) và tổng số tháng có email
df['Avg send per month'] = None
df['Total months with email'] = None

# Lặp qua các email để tính toán
def calculate_email_statistics(email_to_filter):
    # Lọc dữ liệu theo email và tạo bản sao để tránh "SettingWithCopyWarning"
    df_filtered = df[df['Email'] == email_to_filter].copy()

    # Tính năm-tháng từ cột 'Date'
    df_filtered['YearMonth'] = df_filtered['Date'].dt.to_period('M')

    # Đếm số lần gửi email theo từng tháng
    monthly_counts = df_filtered.groupby('YearMonth').size()

    # Tính trung bình số lần gửi email theo tháng
    avg_per_month = round(monthly_counts.mean(), 2)

    # Tính tổng số tháng có email
    total_months = len(monthly_counts)

    # Gán giá trị vào DataFrame gốc bằng cách sử dụng .loc[]
    df.loc[df['Email'] == email_to_filter, 'Avg send per month'] = avg_per_month
    df.loc[df['Email'] == email_to_filter, 'Total months with email'] = total_months

# Chạy hàm tính toán cho từng email
for email_to_filter in emails:
    calculate_email_statistics(email_to_filter)

# Lưu DataFrame với các cột mới vào file CSV mới
df.to_csv('temp/addAvgAndTotalmonths.csv', index=False)

print("Xác định tần suất gửi trung bình và tổng số tháng có email \u2713")
