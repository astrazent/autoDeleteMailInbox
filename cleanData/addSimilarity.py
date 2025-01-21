import pandas as pd

# Hàm trích xuất từ khóa với step = 3
def extract_keywords(text, step=1):
    # Kiểm tra và chuyển giá trị về chuỗi nếu cần
    if not isinstance(text, str):
        text = str(text)
    words = text.split()
    return words[::step]

# Hàm tính tỷ lệ giống nhau giữa 2 danh sách từ khóa
def calculate_similarity(keywords1, keywords2):
    set1, set2 = set(keywords1), set(keywords2)
    if not set1 or not set2:
        return 0
    return len(set1.intersection(set2)) / len(set1.union(set2))

# Hàm chính: tính toán tỷ lệ giống nhau từ file CSV và thêm cột tương đồng vào
def calculate_similarity_from_csv(input_csv, output_csv):
    # Đọc dữ liệu từ file CSV
    df = pd.read_csv(input_csv)
    
    # Sắp xếp theo email
    df = df.sort_values(by="Email")

    # Tạo danh sách để lưu cột Similarity
    similarity_column = [0] * len(df)

    i = 0
    # Lặp qua từng email và tính tỷ lệ tương đồng
    for email, group in df.groupby("Email"):
        group = group.reset_index()
        group_size = len(group)
        
        # Lặp qua từng dòng trong nhóm để tính tỷ lệ tương đồng
        for index, row in group.iterrows():
            body1 = row["Body"]
            similarities = []
            if not pd.isna(body1):
                # Duyệt qua tất cả các dòng còn lại trong nhóm để tính sự tương đồng
                for other_index, other_row in group.iterrows():
                    if index != other_index:  # Đảm bảo không so sánh với chính nó
                        body2 = other_row["Body"]
                        if not pd.isna(body2): 
                            keywords1, keywords2 = extract_keywords(body1), extract_keywords(body2)
                            similarity = calculate_similarity(keywords1, keywords2)
                            similarities.append(similarity)
                # Tính trung bình sự tương đồng cho body1
                avg_similarity = sum(similarities) / len(similarities) if similarities else 0
            else:
                avg_similarity = 0
            similarity_column[i] = avg_similarity
    
    # Thêm cột Similarity vào DataFrame gốc
    df["Similarity"] = similarity_column

    # Lưu kết quả ra file CSV
    df.to_csv(output_csv, index=False)
    print("Xác định độ tương đồng giữa các inbox/mail \u2713")

input_file = "temp/addQuantity.csv"
output_file = "temp/addSimilarity.csv"

calculate_similarity_from_csv(input_file, output_file)
