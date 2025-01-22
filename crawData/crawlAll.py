# Importing libraries
import imaplib
import email
import yaml
import time
import csv
from tqdm import tqdm
import time
import pygame

# Khởi tạo pygame mixer
pygame.mixer.init()

# Đọc thông tin đăng nhập từ tệp credentials.yml
with open("crawData/credentials.yml") as f:
    content = f.read()

my_credentials = yaml.load(content, Loader=yaml.FullLoader)
user, password = my_credentials["user"], my_credentials["password"]

# URL cho IMAP
imap_url = 'imap.gmail.com'

# Kết nối với Gmail qua SSL
my_mail = imaplib.IMAP4_SSL(imap_url)

# Đăng nhập
my_mail.login(user, password)

# Chọn hộp thư (ví dụ: Inbox)
my_mail.select('Inbox')

# Tìm tất cả email
key = 'ALL'  # Lấy tất cả email
_, data = my_mail.search(None, key)

# Danh sách chứa ID của các email
mail_id_list = data[0].split()

# Danh sách chứa thông tin email
emails = []

# Ghi lại thời gian bắt đầu
start_time = time.time()
start_time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time))
print(f"Bắt đầu lúc: {start_time_str}")

# Lặp qua từng email để lấy thông tin với thanh tiến trình
for num in tqdm(mail_id_list, desc="Đang xử lý email", unit="email"):
    _, message_data = my_mail.fetch(num, '(RFC822)')
    for response_part in message_data:
        if isinstance(response_part, tuple):
            msg = email.message_from_bytes(response_part[1])

            # Lấy thông tin từ header
            sender = msg['From']
            subject = msg['Subject']
            date = msg['Date']

            # Lấy nội dung email
            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition"))

                    if content_type == "text/plain" and "attachment" not in content_disposition:
                        body = part.get_payload(decode=True).decode("utf-8", errors="ignore")
                        break
            else:
                body = msg.get_payload(decode=True).decode("utf-8", errors="ignore")

            emails.append({
                "Sender": sender,
                "Subject": subject,
                "Date": date,
                "Body": body
            })

# Ghi danh sách thông tin email vào tệp txt
output_file = "temp/raw.txt"
with open(output_file, "w", encoding="utf-8") as f:
    for email_info in emails:
        f.write(f"Sender: {email_info['Sender']}\n")
        f.write(f"Subject: {email_info['Subject']}\n")
        f.write(f"Date: {email_info['Date']}\n")
        f.write(f"Body:\n{email_info['Body']}\n")
        f.write("\n" + "-" * 50 + "\n")

# Ghi lại thời gian hoàn thành
end_time = time.time()
end_time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(end_time))
total_time = end_time - start_time
total_emails = len(emails)

# In ra màn hình
print(f"Hoàn thành lúc: {end_time_str}")
print(f"Tổng thời gian thực hiện: {total_time:.2f} giây")
print(f"Tổng số inbox: {total_emails}")

# Ghi log vào file CSV
log_file = "temp/crawAll_log.csv"
with open(log_file, "w", newline="", encoding="utf-8") as csvfile:
    csvwriter = csv.writer(csvfile)
    # Ghi tiêu đề cột
    csvwriter.writerow(["Start Time", "End Time", "Total Time (s)", "Total Inbox"])
    # Ghi dữ liệu
    csvwriter.writerow([start_time_str, end_time_str, round(total_time, 2), total_emails])

print(f"Đã lưu thông tin log vào file '{log_file}'.")

# Đóng kết nối
my_mail.logout()

# Phát âm thanh
pygame.mixer.music.play()

# Hỏi người dùng có muốn tắt nhạc không
user_input = input("Bạn có ở đó không? (yes/no): ").strip().lower()

if user_input == "yes":
    pygame.mixer.music.stop()  # Dừng nhạc
    print("Nhạc đã dừng.")
else:
    print("Nhạc tiếp tục phát.")
