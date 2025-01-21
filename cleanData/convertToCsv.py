import csv

# Đọc dữ liệu từ file TXT
# input_file = "valid_emails.txt"
input_file = "temp/rmMidSpaceAndDecoding.txt"
emails = []

def extract_date(full_date):
    try:
        # Tách chuỗi ngày tháng theo khoảng trắng
        parts = full_date.split(" ")

        # Tách ngày, tháng và năm từ chuỗi
        day = parts[1]
        month_str = parts[2]
        year = parts[3]

        # Chuyển tháng sang số
        month_map = {
            "jan": "01", "feb": "02", "mar": "03", "apr": "04", "may": "05", "jun": "06",
            "jul": "07", "aug": "08", "sep": "09", "oct": "10", "nov": "11", "dec": "12"
        }
        
        if len(day) == 1:
            day = "0" + day
        month = month_map.get(month_str.lower())

        if month is None:
            return "NaT"  # Nếu không tìm thấy tháng, trả về NaT

        # Trả về ngày theo định dạng ngày-tháng-năm
        return f"{day}-{month}-{year}"
    except IndexError:
        return "NaT"


def sender_name_if_email_none(data):
    # Tìm vị trí của 'sender:', 'subject:', 'date:', và 'body:'
    sender_index = data.index('sender:') + 1
    subject_index = next((i for i, val in enumerate(data) if val == 'subject:'), None)
    date_index = next((i for i, val in enumerate(data) if val == 'date:'), None)
    body_index = next((i for i, val in enumerate(data) if val == 'body:'), None)

    # Tính toán chỉ số kết thúc cho tên người gửi
    end_index = subject_index if subject_index is not None else (date_index if date_index is not None else body_index)

    # Lấy tên người gửi
    sender_name = " ".join(data[sender_index:end_index]) if end_index else "Không tìm thấy tên người gửi"
    return sender_name

def extract_sender_and_email(data):
    # Tìm vị trí của "sender:" để xác định bắt đầu tên người gửi
    sender_index = next((i for i, val in enumerate(data) if val == 'sender:'), None)

    if sender_index is not None:
        # Kiểm tra phần tử giữa sender và email
        email_index = next((i for i, val in enumerate(data[sender_index + 1:], start=sender_index + 1) if '@' in val), None)

        subject_index = next((i for i, val in enumerate(data) if val == 'subject:'), None)
        date_index = next((i for i, val in enumerate(data) if val == 'date:'), None)
        body_index = next((i for i, val in enumerate(data) if val == 'body:'), None)

        # xử lý trường hợp chỉ có email nhưng không có sender
        onlyEmail = False
        # Nếu không tìm thấy email trong khoảng giữa sender và email

        if email_index == 1:
            # Kiểm tra phần tử tiếp theo sau email_index (bên phải)
            email_index = next((i for i, val in enumerate(data[email_index + 1:], start=email_index + 1) if '@' in val), None)
            if email_index != 2:
                email_index = None
                onlyEmail = True
        
        #Xử lý thêm trường hợp nếu email tìm được là thuộc các thành phần khác trong inbox
        if email_index is not None:
            if subject_index is not None and (email_index > subject_index):
                email_index = None
            elif date_index is not None and (email_index > date_index):
                email_index = None
            elif body_index is not None and (email_index > body_index):
                email_index = None
        
        #Xử lý các TH không None còn lại
        if email_index is not None:
            # Lấy tên người gửi từ sender_index đến trước email_index
            sender_name = data[sender_index + 1:email_index]
            email = data[email_index]
            sdn = ' '.join(sender_name)
            return sdn, email
        else:
            if onlyEmail:
                sender_name = "None"
                email = data[1]
            else:
                # Lấy tên người gửi từ sender_index đến trước email_index
                sender_name = sender_name_if_email_none(data)
                email = "None"
            
            return sender_name, email
    else:
        if email_index is not None:
            # Lấy tên người gửi từ sender_index đến trước email_index
            sender_name = "None"
            email = data[email_index]
            sdn = "None"
            return sdn, email
    return "None", "None"

with open(input_file, mode="r", encoding="utf-8") as file:
    lines = file.readlines()
    for line in lines:
        line = line.strip()
        if line.startswith("sender:"):
            # Tách các phần dựa trên khoảng trắng và loại bỏ các ký tự rỗng
            parts = [part for part in line.split(" ") if part]
            try:
                # Tách subject và body từ các phần còn lại
                subject_none = 0
                date_none = 0
                body_none = 0
                try:
                    subject_index = next(i for i, part in enumerate(parts) if part.startswith("subject:"))
                except StopIteration:
                    subject_index = -1
                    subject_none = 1
                try:
                    date_index = next(i for i, part in enumerate(parts) if part.startswith("date:"))
                    if subject_index == -1:
                        subject_index = date_index
                except StopIteration:
                    date_index = -1
                    date_none = 1
                try:
                    body_index = next(i for i, part in enumerate(parts) if part.startswith("body:"))
                    if subject_index == -1:
                        subject_index = body_index
                    if date_index == -1:
                        date_index = body_index
                except StopIteration:
                    body_index = len(parts) - 1
                    if subject_index == -1:
                        subject_index = body_index
                    if date_index == -1:
                        date_index = body_index
                    body_none = 1

                sender_name, email = extract_sender_and_email(parts)
                
                sdn = sender_name if sender_name else "None"
                email = email if email else "None"
                
                # Kiểm tra None
                if subject_none == 0:
                    subject = " ".join(parts[subject_index + 1:date_index]) if parts[subject_index + 1:date_index] else "None"
                else:
                    subject = "None"

                if date_none == 0:
                    full_date = " ".join(parts[date_index + 1:body_index]) if parts[date_index + 1:body_index] else "None"
                    date = extract_date(full_date) if full_date else "None"
                else:
                    date = "None"

                if body_none == 0:
                    body = " ".join(parts[body_index + 1:]) if parts[body_index + 1:] else "None"
                else:
                    body = "None"
                
                email_data = {
                    "id": len(emails) + 1,  # Thêm cột id tăng dần
                    "sender": sdn,
                    "email": email,
                    "subject": subject,
                    "body": body,
                    "date": date 
                }
                emails.append(email_data)
            except (IndexError, StopIteration):
                print(IndexError, StopIteration)


# Tên file CSV
output_file = "temp/convertToCsv.csv"

# Ghi dữ liệu vào file CSV
with open(output_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    
    # Ghi tiêu đề cột
    writer.writerow(["ID", "Sender", "Email", "Subject", "Body", "Date"])
    
    # Ghi nội dung từng email
    for email in emails:
        writer.writerow([email["id"], email["sender"], email["email"], email["subject"], email["body"], email["date"]])

print("Chuyển sang file csv \u2713")
