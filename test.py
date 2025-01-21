import time
import pygame

# Khởi tạo pygame mixer
pygame.mixer.init()

# Load file âm thanh
pygame.mixer.music.load("D:/crawl_project/crawlNameEmail/sound/completed.mp3")

# Phát âm thanh
pygame.mixer.music.play()

# Tăng âm lượng từ từ qua 100 mức
for volume in range(0, 101):
    pygame.mixer.music.set_volume(volume / 100)  # Chỉnh âm lượng từ 0 đến 1
    time.sleep(0.1)  # Chờ 0.1 giây mỗi lần thay đổi âm lượng

# Hỏi người dùng có muốn tắt nhạc không
user_input = input("Bạn có muốn tắt nhạc không? (yes/no): ").strip().lower()

if user_input == "yes":
    pygame.mixer.music.stop()  # Dừng nhạc
    print("Nhạc đã dừng.")
else:
    print("Nhạc tiếp tục phát.")
