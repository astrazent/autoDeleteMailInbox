import pandas as pd

# Đọc dữ liệu từ file csv
file_path = 'temp/addSimilarity.csv'  # Đường dẫn file csv
output_path = 'temp/addCountSimilarAndRatio.csv'  # Đường dẫn file csv xuất ra
data = pd.read_csv(file_path)

# Bước 1: Nhóm các email giống nhau lại với nhau
data['Email'] = data['Email'].str.lower()  # Chuẩn hóa email về dạng viết thường
groups = data.groupby('Email')

# Danh sách lưu kết quả
processed_rows = []

# Bước 2: Xử lý từng nhóm
for email, group in groups:
    # Sắp xếp các dòng theo Similarity giảm dần
    group = group.sort_values(by='Similarity', ascending=False)

    # Thêm cột CountSimilarValues vào group
    group['Count similar values'] = 0

    # Tạo danh sách các giá trị Similarity sau khi làm tròn
    similarity_rounded_list = group['Similarity'].apply(lambda x: round(x, 1))

    # Duyệt qua từng dòng trong nhóm
    for index, row in group.iterrows():
        similarity_rounded = round(row['Similarity'], 1)
        if similarity_rounded != 0:
            # Đếm số dòng khác có giá trị Similarity giống với dòng hiện tại
            count_similar = (similarity_rounded_list == similarity_rounded).sum() - 1  # Trừ chính dòng hiện tại
            group.at[index, 'Count similar values'] = count_similar
        else:
            group.at[index, 'Count similar values'] = 0

    # Bước 3: Tính tỷ lệ giống nhau tuyệt đối
    count_similar_zero = (group['Count similar values'] == 0).sum()  # Đếm số dòng có CountSimilarValues = 0
    total_rows = len(group)  # Tổng số dòng trong nhóm
    similarity_ratio = 1 -  (count_similar_zero / total_rows)  # Tính tỷ lệ

    # Thêm cột tỷ lệ vào group
    group['Similarity ratio'] = similarity_ratio

    # Thêm nhóm đã xử lý vào danh sách kết quả
    processed_rows.append(group)

# Gộp tất cả các nhóm lại
result_data = pd.concat(processed_rows)

# Xuất ra file CSV
result_data.to_csv(output_path, index=False)

print("Xác định số mail tương đồng với nhau, tỉ lệ tương đồng của mail đó \u2713")
