import re

def clean_html_from_file(input_file, output_file):
    # Đọc nội dung từ file đầu vào
    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Loại bỏ dấu <> quanh email (nếu có)
    content = re.sub(r'<([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})>', r'\1', content)
    
        # Loại bỏ nội dung giữa các thẻ <style> và </style>
    content = re.sub(r'<style.*?>.*?</style>', '', content, flags=re.DOTALL)
    
    # Loại bỏ các khối CSS dạng .selector { ... }
    content = re.sub(r'\.[a-zA-Z0-9_-]+\s*{[^}]*}', '', content)

    # Loại bỏ các thẻ HTML
    content = re.sub(r'<[^>]+>', '', content)

    # Ghi nội dung đã xử lý vào file đầu ra
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(content)

# Đường dẫn file đầu vào và đầu ra
input_file = 'temp/raw.txt'  # Đường dẫn file txt đầu vào
output_file = 'temp/rmHtmlCss.txt'  # Đường dẫn file txt đầu ra

# Gọi hàm xử lý
clean_html_from_file(input_file, output_file)
print("Loại bỏ Html/CSS \u2713")
