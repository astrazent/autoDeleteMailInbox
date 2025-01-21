import pandas as pd

def filter_emails(data):
    """
    Lọc các email theo quy tắc đã định nghĩa:
    1. Nếu email bị trùng nội dung (Body) nhưng ID lớn hơn email khác, thì Body được gán None.
    2. Định nghĩa email khác nhau dựa trên đuôi và nội dung email.
    """
    def is_different(email1, email2):
        # Tách phần trước và sau dấu @
        local1, domain1 = email1.split('@')
        local2, domain2 = email2.split('@')
        if domain1 == 'gmail.com' and domain2 == 'gmail.com':
            return local1 != local2
        else:
            # Nếu không phải @gmail, kiểm tra similarity của domain
            domain1_parts = domain1.split('.')
            domain2_parts = domain2.split('.')
            matches = sum(1 for part1, part2 in zip(domain1_parts, domain2_parts) if part1 == part2)
            similarity = matches / max(len(domain1_parts), len(domain2_parts))
            return similarity < 0.6

    # Nhóm theo Body
    grouped = data.groupby('Body')

    for body, group in grouped:
        # Chỉ xử lý nhóm có nhiều hơn 1 email (có Body giống nhau)
        if len(group) > 1:
            # Sắp xếp theo ID trong từng group
            group = group.sort_values(by='ID')

            # Duyệt qua các email đàn con trong group
            i = 0
            email1 = group.iloc[i]
            for j in range(i + 1, len(group)):  # So sánh với tất cả email phía dưới email1
                email2 = group.iloc[j]
                # Kiểm tra điều kiện
                if is_different(email1['Email'], email2['Email']) and email2['ID'] > email1['ID']:
                    # Gán Body của email thứ hai thành None nếu điều kiện thỏa mãn
                    data.at[email2.name, 'Body'] = None
    return data


# Đọc tệp CSV
data = pd.read_csv('temp/convertToCsv.csv')

# # Lọc email bằng hàm filter_emails
filtered_data = filter_emails(data)

# # Kết hợp dữ liệu đã lọc với dữ liệu gốc
# data.update(filtered_data)

# Lưu kết quả vào tệp mới
filtered_data.to_csv('temp/rmErrorData.csv', index=False)

print("Loại dữ liệu trùng lặp giữa các dòng (cột Body) \u2713")
