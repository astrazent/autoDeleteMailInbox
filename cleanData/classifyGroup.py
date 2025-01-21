import csv
import string

# Đọc từ khóa từ file words.txt
def load_keywords_from_file(filename):
    group_1_keywords = []
    group_2_keywords = []
    current_group = None
    
    with open(filename, mode="r", encoding="utf-8") as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip().lower()
            if line == "!1":
                current_group = 1
            elif line == "!2":
                current_group = 2
            elif line:
                if current_group == 1:
                    group_1_keywords.append(line)
                elif current_group == 2:
                    group_2_keywords.append(line)
    return group_1_keywords, group_2_keywords

# Hàm kiểm tra từ khóa
def check_keywords(text, group_1_keywords, group_2_keywords):
    matched_keywords = []
    group = 0
    # Chuyển văn bản thành chữ thường và loại bỏ dấu câu
    text_lower = text.lower()
    
    # Kiểm tra với nhóm 1
    for keyword in group_1_keywords:
        keyword_lower = keyword.lower()

        # TH1: Kiểm tra cả từ lớn (nhiều chữ) có nằm trong text không
        if keyword_lower in text_lower:
            matched_keywords.append(keyword)
            print
            group = max(group, 1)  # Cập nhật nhóm với số lớn hơn nếu có

        # TH2: Kiểm tra từng từ khóa có ẩn trong từng từ của text không
        words_in_text = text_lower.split()  # Tách văn bản thành các từ
        for word_in_text in words_in_text:
            if keyword_lower in word_in_text:
                matched_keywords.append(keyword)
                group = max(group, 1)  # Cập nhật nhóm với số lớn hơn nếu có
                break  # Nếu tìm thấy, không cần kiểm tra nữa, thoát khỏi vòng lặp

    # Kiểm tra với nhóm 2 nếu không tìm thấy từ khóa ở nhóm 1
    for keyword in group_2_keywords:
        keyword_lower = keyword.lower()
        
        # TH1: Kiểm tra cả từ lớn (nhiều chữ) có nằm trong text không
        if keyword_lower in text_lower:
            matched_keywords.append(keyword)
            group = max(group, 2)  # Cập nhật nhóm với số lớn hơn nếu có
        
        # TH2: Kiểm tra từng từ khóa có ẩn trong từng từ của text không
        for word_in_text in words_in_text:
            if keyword_lower in word_in_text:
                matched_keywords.append(keyword)
                group = max(group, 2)  # Cập nhật nhóm với số lớn hơn nếu có
                break  # Nếu tìm thấy, không cần kiểm tra nữa, thoát khỏi vòng lặp

    return matched_keywords, group

# Đọc dữ liệu từ file CSV đầu vào
input_csv_file = "temp/rmErrorData.csv"
output_csv_file = "temp/classifyGroup.csv"
keywords_file = "words.txt"  # Đọc từ khóa từ file words.txt

# Load keywords từ file
group_1_keywords, group_2_keywords = load_keywords_from_file(keywords_file)

# Đọc và xử lý dữ liệu từ file CSV
with open(input_csv_file, mode="r", encoding="utf-8") as infile:
    reader = csv.DictReader(infile)
    
    # Tạo file CSV đầu ra với thêm các cột "Từ khoá trùng khớp" và "Nhóm"
    with open(output_csv_file, mode="w", newline="", encoding="utf-8") as outfile:
        fieldnames = reader.fieldnames + ["Keyword match", "Group"]
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in reader:
            # Kiểm tra từ khóa trong toàn bộ dòng (tất cả các cột)
            matched_keywords, group = check_keywords(" ".join(row.values()), group_1_keywords, group_2_keywords)
            if matched_keywords:
                unique_words = []
                for word in matched_keywords:
                    if word not in unique_words:
                        unique_words.append(word)
                row["Keyword match"] = ", ".join(unique_words)
                row["Group"] = group
                writer.writerow(row)  # Ghi dữ liệu vào file CSV
            else:
                row["Keyword match"] = "None"
                row["Group"] = 0
                writer.writerow(row)  # Ghi dữ liệu vào file CSV
print("Phân loại nhóm theo từ khoá \u2713")
