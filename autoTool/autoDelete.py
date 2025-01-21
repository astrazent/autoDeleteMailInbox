import pyautogui
import time
from datetime import datetime
from PIL import ImageGrab
import keyboard  # Thư viện để kiểm tra phím tắt
from pathlib import Path
import pygame

# Khởi tạo pygame mixer
pygame.mixer.init()

def is_color_at_position(x, y, target_rgb=(235, 237, 241), tolerance=10):
    """Kiểm tra nếu màu tại vị trí (x, y) gần giống với màu mục tiêu."""
    try:
        screenshot = ImageGrab.grab(bbox=(x, y, x+1, y+1))  # Chụp ảnh nhỏ chỉ 1 pixel
        color = screenshot.getpixel((0, 0))
        r, g, b = color
        target_r, target_g, target_b = target_rgb

        if (abs(r - target_r) <= tolerance and 
            abs(g - target_g) <= tolerance and 
            abs(b - target_b) <= tolerance):
            return True
    except Exception as e:
        print(f"Lỗi khi kiểm tra màu tại vị trí ({x}, {y}): {e}")
    return False

def parse_action_line(line):
    """Phân tích một dòng hành động để xác định loại hành động."""
    line = line.strip()
    if not line:
        return None, None

    if line.startswith("(") and "-" not in line:
        # Dòng chỉ chứa tọa độ
        coord_part = line.strip()
        x, y = map(int, coord_part.strip("() ").split(","))
        return ("click", (x, y))

    elif line.startswith("(") and "-" in line:
        # Dòng chứa tọa độ và giá trị RGB
        coord_part, color_part = line.split("-")
        x, y = map(int, coord_part.strip("() ").split(","))
        r, g, b = map(int, color_part.strip("() ").split(","))
        return ("color_check", (x, y, r, g, b))

    elif line.lower() == "text input":
        # Dòng yêu cầu nhập dữ liệu từ file keyboard.txt
        return ("text_input", "scripts/customedScripts.txt")

    elif Path(line).is_file():
        # Dòng yêu cầu đọc từ file cụ thể
        return ("file_input", line)

    elif line[0].isalpha():
        # Dòng chứa phím chức năng
        key = line.strip().lower()
        return ("key_press", key)
    else:
        print("Dữ liệu lỗi: " + line)

    return None, None 

def delete_log(keyword):
    with open("deleted.txt", "a") as delete_done_file:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        delete_done_file.write(f"{keyword} [{current_time}]\n")


def execute_actions(file_path, delay, times):
    """Thực hiện các hành động từ file, với delay giữa các thao tác."""
    try:
        with open(file_path, "r") as file:
            actions = file.readlines()

        # Kiểm tra các dòng đặc biệt và phân loại
        text_input_lines = []
        file_input_lines = []
        i1 = 0
        i2 = 0
        t = 1 # số lần thực hiện
        if int(times) == 0:
            t = -1 * 10**9
        for action in actions:
            action_type, action_data = parse_action_line(action)
            if action_type == "text_input":
                with open(action_data, "r") as text_file:
                    text_input_lines.extend(text_file.readlines())
            elif action_type == "file_input":
                with open(action_data, "r") as text_file:
                    file_input_lines.extend(text_file.readlines())
        
        if not file_input_lines:
            with open("scripts/target.txt", "r") as text_file:
                file_input_lines.extend(text_file.readlines())

        while True:
            # Kiểm tra điều kiện kết thúc chương trình
            if times == 0:
                if (i1 >= len(text_input_lines) and len(text_input_lines)) or (i2 >= len(file_input_lines) and len(file_input_lines)):
                    break
            if t <= int(times):
                # vì không biết thằng nào bằng 0 trước nên phải tách ra như này
                if i1 >= len(text_input_lines) and len(text_input_lines):
                    i1 = 0
                if i2 >= len(file_input_lines) and len(file_input_lines):
                    i2 = 0
            else:
                break

            # Thực hiện các hành động theo thứ tự
            for action in actions:
                if keyboard.is_pressed('esc'):
                    print("Đã dừng chương trình theo yêu cầu.")
                    break

                action_type, action_data = parse_action_line(action)

                if action_type == "click":
                    x, y = action_data
                    print(f"Click tại tọa độ: ({x}, {y})")
                    pyautogui.click(x, y)

                elif action_type == "color_check":
                    x, y, r, g, b = action_data
                    print(f"Kiểm tra màu tại tọa độ: ({x}, {y}) với RGB: ({r}, {g}, {b})")
                    if is_color_at_position(x, y, (r, g, b)):
                        print(f"Màu tại ({x}, {y}) thỏa mãn, thực hiện click.")
                        pyautogui.click(x, y)
                    else:
                        print(f"Màu tại ({x}, {y}) không thỏa mãn, bỏ qua.")

                elif action_type == "key_press":
                    key = action_data
                    print(f"Nhấn phím chức năng: {key}")
                    pyautogui.press(key)

                elif action_type == "text_input" and text_input_lines:
                    pyautogui.typewrite(text_input_lines[i1].strip())  
                    delete_log("text_input: " + text_input_lines[i1].strip())  
                    i1 += 1

                elif action_type == "file_input" and file_input_lines:
                    pyautogui.typewrite(file_input_lines[i2].strip())
                    delete_log("file_input: " + file_input_lines[i2].strip())  
                    i2 += 1
                else:
                    print(f"Định dạng không hợp lệ: {action}")
                
                time.sleep(delay)  # Thực hiện delay giữa các hành động
            t += 1

    except FileNotFoundError:
        print(f"Không tìm thấy file: {file_path}")
    except Exception as e:
        print(f"Lỗi khi thực hiện hành động: {e}")

def main():
    file_path = None
    delay = None
    times = None
    while True:
        if file_path is None:
            file_path = input("Nhập đường dẫn file kịch bản (không có nhấn 0): ")
            if not file_path == '0' and not file_path.endswith((".txt", ".csv")):
                print("File không tồn tại!")
                file_path = None
                continue
        
        if delay is None:
            try:    
                delay = input("Nhập thời gian delay giữa các hành động (giây) (hoàn tác nhập \"back\"): ")
                if delay == 'back':
                    file_path = None
                    delay = None
                    continue
                if float(delay) <= 0:
                    print("Thời gian delay phải là số lớn hơn 0.")
            except ValueError:
                print("Vui lòng nhập số hợp lệ.")
                continue
        
        if times is None:
            try:
                times = input("Số lần thực hiện (lần) (nhập 0 để dừng tự động) ((hoàn tác nhập \"back\")): ")
                if times == 'back':
                    delay = None
                    times = None
                    continue
                if int(times) <= 0:
                    print("Số lần thực hiện phải là số nguyên dương.")
                else:
                    break
            except ValueError:
                print("Vui lòng nhập số hợp lệ.")
                continue

    if file_path == '0':
        file_path = "scripts/peripheral.txt"  # Đường dẫn tới file kịch bản mặc định

    print("Bắt đầu thực hiện các hành động. Nhấn ESC để dừng chương trình.")
    execute_actions(file_path, delay, times)
    print("Hoàn thành các hành động.")

    # Load file âm thanh
    pygame.mixer.music.load("D:/crawl_project/crawlNameEmail/sound/completed.mp3")

    # Phát âm thanh
    pygame.mixer.music.play()

    # Hỏi người dùng có muốn tắt nhạc không
    user_input = input("Bạn có muốn tắt nhạc không? (yes/no): ").strip().lower()

    if user_input == "yes":
        pygame.mixer.music.stop()  # Dừng nhạc
        print("Nhạc đã dừng.")
    else:
        print("Nhạc tiếp tục phát.")

if __name__ == "__main__":
    main()