import re

def process_email_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Loại bỏ dòng trống, dòng chứa "--------------------------------------------------" và khoảng trắng dư thừa
    lines = [
        line.strip() for line in lines
        if line.strip() and "--------------------------------------------------" not in line
    ]

    processed_content = []
    current_email = ""

    for line in lines:
        if line.lower().startswith("sender:"):  # Dòng bắt đầu email mới
            if current_email:  # Nếu đã có nội dung email trước đó, lưu lại
                processed_content.append(current_email)
            current_email = line  # Khởi tạo email mới
        else:
            current_email += " " + line  # Gộp các dòng thuộc về email hiện tại

    # Thêm email cuối cùng vào danh sách
    if current_email:
        processed_content.append(current_email)

    # Loại bỏ các đường link, dấu ' và " và chuyển thành chữ thường
    processed_content = [
        re.sub(r"http[s]?://\S+", "", email.lower()) for email in processed_content
    ]
    processed_content = [
        re.sub(r"[\'\"]", "", email) for email in processed_content  # Loại bỏ dấu ' và "
    ]

    # Ghi vào file đầu ra
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write("\n".join(processed_content))

    print("Loại bỏ khoảng trắng bên ngoài và dấu ngoặc kép \u2713")

# Đường dẫn tệp đầu vào và đầu ra
input_file = "temp/rmHtmlCss.txt"  # Tệp đầu vào
output_file = "temp/rmOutSpaceAndQuotes.txt"  # Tệp đầu ra

# Gọi hàm xử lý
process_email_file(input_file, output_file)
