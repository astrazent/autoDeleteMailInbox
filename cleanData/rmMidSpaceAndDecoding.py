import re
import html
from email.header import decode_header

def remove_extra_spaces(text):
    """
    Loại bỏ các khoảng trắng thừa giữa các từ trong đoạn văn bản nhưng không cắt xuống dòng.
    """
    # Đảm bảo giữ lại dấu xuống dòng và thay thế khoảng trắng thừa trong mỗi dòng
    lines = text.split('\n')  # Tách văn bản thành các dòng

    #Loại bỏ kí tự ZWNJ, ZWSP (unicode giả dấu cách) và dấu cách thật
    cleaned_lines = [' '.join(line.replace('\u200b', '').replace('\u200c', '').split()) for line in lines]  # Loại bỏ khoảng trắng thừa trong mỗi dòng
    return '\n'.join(cleaned_lines)  # Kết hợp lại các dòng với dấu xuống dòng

def decode_email_header(encoded_text):
    """
    Decode một chuỗi email header được mã hóa (e.g., =?utf-8?b?...?=).
    """
    try:
        decoded_parts = decode_header(encoded_text)
        decoded_string = ""
        for part, encoding in decoded_parts:
            if isinstance(part, bytes):  # Nếu phần này là bytes, cần decode
                decoded_string += part.decode(encoding or 'utf-8')
            else:  # Nếu đã là string, chỉ cần nối
                decoded_string += part
        return decoded_string
    except Exception as e:
        return encoded_text  # Nếu không giải mã được, giữ nguyên văn bản gốc

def decode_email_line(line):
    """
    Giải mã từng phần của dòng email.
    """
    # Tìm và giải mã tất cả các chuỗi mã hóa MIME trong dòng
    pattern = r"(=\?[^?]+\?[bq]\?[^?]+\?=)"
    decoded_line = re.sub(
        pattern,
        lambda match: decode_email_header(match.group(0)),
        line
    )
    return decoded_line

def process_text_file(input_file, output_file):
    """
    Đọc văn bản từ file đầu vào, loại bỏ khoảng trắng thừa và ghi kết quả vào file đầu ra.
    """
    # Đọc nội dung từ file đầu vào
    with open(input_file, 'r', encoding='utf-8') as f:
        body_text = f.read()

    # Loại bỏ khoảng trắng thừa
    cleaned_text = remove_extra_spaces(body_text)

    # Giải mã HTML entities
    decoded_str = html.unescape(cleaned_text)

    lines = decoded_str.splitlines()

    decoded_lines = [decode_email_line(line.strip()) for line in lines]

    # Ghi kết quả vào file đầu ra
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for decoded_line in decoded_lines:
            outfile.write(decoded_line + '\n')

    print("Loại bỏ khoảng trắng giữa các từ và mã hoá base64 \u2713")

# Đặt tên file đầu vào và đầu ra
# input_file = 'valid_emails.txt'
input_file = 'temp/rmOutSpaceAndQuotes.txt'
output_file = 'temp/rmMidSpaceAndDecoding.txt'

# Xử lý tệp tin
process_text_file(input_file, output_file)

