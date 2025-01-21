import pandas as pd
import warnings

# Tắt tất cả các cảnh báo UserWarning
warnings.filterwarnings("ignore", category=UserWarning)

# Đọc dữ liệu từ file CSV
df = pd.read_csv('temp/addAvgAndTotalmonths.csv')

# Chuyển cột Date sang định dạng datetime
df['Date'] = pd.to_datetime(df['Date'])

# Sắp xếp theo Email và Date
df_sorted = df.sort_values(by=['Email', 'Date'])

# Hàm tính toán ngày bắt đầu, ngày kết thúc và vòng đời
def add_group_info(group):
    first_date = group['Date'].iloc[0]  # Ngày đầu tiên
    last_date = group['Date'].iloc[-1]  # Ngày cuối cùng
    time_diff = (last_date - first_date).days  # Vòng đời
    group['First date'] = first_date  # Thêm cột 'First date'
    group['Last date'] = last_date  # Thêm cột 'Last date'
    group['Period (day)'] = time_diff  # Thêm cột 'Period (day)'
    return group

# Lưu cột 'Email' để nối lại sau khi drop
emails = df_sorted['Email']

# Tách cột 'Email' khỏi DataFrame trước khi nhóm
df_sorted_no_email = df_sorted.drop(columns=['Email'])

# Áp dụng hàm add_group_info trên từng nhóm email và giữ nguyên các cột gốc
df_updated = df_sorted_no_email.groupby(emails, group_keys=False, sort=False).apply(add_group_info)

# Thêm lại cột 'Email' vào DataFrame đã cập nhật
df_updated['Email'] = emails

# Đổi thứ tự cột sao cho 'Email' ở vị trí thứ 4
columns = df_updated.columns.tolist()
columns.remove('Email')  # Xoá 'Email' khỏi danh sách cột
columns.insert(4, 'Email')  # Thêm 'Email' vào vị trí thứ 4 (chỉ số bắt đầu từ 0)

# Sắp xếp lại cột theo thứ tự mong muốn
df_updated = df_updated[columns]

# Ghi DataFrame đã cập nhật vào file CSV mới
df_updated.to_csv('temp/addFirstLastDateAndPeriod.csv', index=False)

print("Xác định ngày bắt đầu/kết thúc/vòng đời của email \u2713")
