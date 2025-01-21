from PIL import ImageGrab
import pyautogui
import time
import keyboard
import os
from pathlib import Path


saved = False
# Hàm để lấy màu tại vị trí con trỏ chuột
def get_color_at_mouse():
    try:
        # Lấy vị trí con trỏ chuột
        x, y = pyautogui.position()
        
        # Lấy màu pixel tại vị trí con trỏ chuột
        screenshot = ImageGrab.grab(bbox=(x, y, x+1, y+1))  # Chụp ảnh nhỏ chỉ 1 pixel
        color = screenshot.getpixel((0, 0))  # Lấy màu tại pixel (0, 0) trong ảnh nhỏ
        
        return (x, y, color)  # Trả về tọa độ và giá trị RGB
    except Exception as e:
        print(f"Lỗi khi lấy màu tại vị trí con trỏ: {e}")
        return None

# Hàm để xử lý các thao tác dựa trên đầu vào
def handle_action(action_type):
    if action_type == "1":
        print("Hãy di chuột đến vị trí lựa chọn, sau đó bấm ESC để lưu vị trí đó.")
        while not keyboard.is_pressed("esc"):
            time.sleep(0.1)
        x, y = pyautogui.position()
        with open("scripts/peripheral.txt", "a") as file:
            file.write(f"({x}, {y})\n")
        print(f"Đã lưu tọa độ: ({x}, {y})")

    elif action_type == "2":
        # Nhập dữ liệu bàn phím
        text = input("Nhập văn bản (script riêng) hoặc đường dẫn file nhâp liệu có sẵn (không dấu) (Nhập 0 để dùng đường dẫn file mặc định): ")

        if text.strip() == '0':
            with open("scripts/peripheral.txt", "a") as file:
                file.write(f"scripts/target.txt\n")
                print(f"Thêm đường dẫn thành công: {text}")
                return
        elif not Path(text.lower()).is_file():
            with open("scripts/customedScripts.txt", "a") as file:
                file.write(f"{text}\n")
            with open("scripts/peripheral.txt", "a") as file:
                file.write("text input\n")
        else:
            with open("scripts/peripheral.txt", "a") as file:
                file.write(f"{text.lower()}\n")
        print(f"Đã lưu dữ liệu: {text}")

    elif action_type == "3":
        print("Hãy di chuột đến vị trí lựa chọn, sau đó bấm ESC để lưu vị trí và màu sắc.")
        while True:
            result = get_color_at_mouse()
            if result:
                x, y, color = result
                print(f"({x}, {y}) - {color}")
            time.sleep(0.5)
            if keyboard.is_pressed("esc"):
                break
            
        with open("scripts/peripheral.txt", "a") as file:
            file.write(f"({x}, {y}) - {color}\n")
        print(f"Đã lưu tọa độ và màu sắc: ({x}, {y}) - {color}")

    elif action_type == "4":
        funtion_key = ["f1 -> f12", "esc", "tab", "ctrl", "alt", "shift", "enter", "backspace", "insert", "delete", "home", "end", "page up", "page down", "up", "down", "left", "right", "caps lock", "num lock"]
        print("danh sách các phím: " + str(funtion_key))
        key = input("Nhập phím chức năng từ bàn phím (nhập đúng chữ trên phím): ")
        # Ghi lại phím vào file
        with open("scripts/peripheral.txt", "a") as file:
            file.write(f"{key}\n")
        print(f"Đã lưu phím: {key}")
    
    elif action_type == "5":
        global saved
        # Đường dẫn file nguồn và file đích
        source_file = "scripts/peripheral.txt"
        destination_file = input("Nhập tên file: ")
        if not destination_file.endswith((".txt", ".csv")):
            destination_file = destination_file + ".txt"

        if os.path.exists(source_file):
            # Mở file nguồn để đọc và file đích để ghi
            with open(source_file, "r") as src, open(destination_file, "w") as dest:
                # Đọc nội dung từ file nguồn
                content = src.read()
                # Ghi nội dung vào file đích
                dest.write(content)
        else:
            print(f"File {source_file} không tồn tại!")
        saved = True
        print("Lưu thành công!")
    else:
        print("Vui lòng chờ...")

def remove_last_line(file_path):
    try:
        # Đọc tất cả các dòng trong file
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
        
        # Kiểm tra nếu file có nội dung
        if lines:
            last_line = lines[-1]  # Lấy dòng cuối cùng
            # Ghi lại nội dung không bao gồm dòng cuối
            with open(file_path, "w", encoding="utf-8") as file:
                file.writelines(lines[:-1])  # Loại bỏ dòng cuối cùng

            print(f"Đã hoàn tác: {last_line.strip()}")
        else:
            print("Tệp rỗng, không có dòng để xóa.")
    except Exception as e:
        print(f"Lỗi xảy ra: {e}")

# Hàm chính
def main():
    begin = True
    while True:
        if begin == True:
            useScript = input("Bạn đã có kịch bản? (1. Có 0. Không): ")
        if useScript.strip() == '1':
            return
        else:
            if begin == True:
                print("Hướng dẫn:")
                print("1: Lấy tọa độ chuột (click)")
                print("2: Nhập văn bản hoặc đường dẫn file (scripts/target.txt)")
                print("3: Lấy tọa độ và màu sắc (dùng để tránh ngoại lệ)")
                print("4: Chọn phím chức năng")
                print("5: Lưu kịch bản (điền đường dẫn và tên file)")
                print("Nhấn giữ ESC để lưu và chuyển sang thao tác tiếp theo")
                print("Nhập 0 để thoát chương trình")

                file_path = "scripts/peripheral.txt"
                with open(file_path, "w") as mouse_file, open("scripts/customedScripts.txt", "w") as keyboard_file:
                    mouse_file.write("")  # Xóa nội dung cũ trong file
                    keyboard_file.write("")  # Xóa nội dung cũ trong file
                begin = False

            while True:
                action_type = input("Nhập loại hành động (1, 2, 3, 4, 5, \"back\" để hoàn tác hoặc 0 để thoát): ").strip()
                if action_type == "0":
                    if not saved:
                        save_request = input("Bạn có muốn lưu kịch bản không? (Viết đường dẫn nếu có hoặc nhập 0 nếu không): ")
                        if save_request == '0':
                            break
                        else:
                            # Đường dẫn file nguồn và file đích
                            source_file = "scripts/peripheral.txt"
                            destination_file = save_request
                            if not destination_file.endswith((".txt", ".csv")):
                                destination_file = destination_file + ".txt"

                            if os.path.exists(source_file):
                                # Mở file nguồn để đọc và file đích để ghi
                                with open(source_file, "r") as src, open(destination_file, "w") as dest:
                                    # Đọc nội dung từ file nguồn
                                    content = src.read()
                                    # Ghi nội dung vào file đích
                                    dest.write(content)
                                break
                            else:
                                print(f"File {source_file} không tồn tại!")
                    else:
                        print("Đã thoát chương trình.")
                        break
                elif action_type.strip() == '1' or action_type.strip() == '2' or action_type.strip() == '3' or action_type.strip() == '4' or action_type.strip() == '5':
                    break
                elif action_type.strip() == 'back':
                    remove_last_line("scripts/peripheral.txt")
                else:
                    print("Vui lòng nhập giá trị hợp lệ!")

            if action_type == "0":
                break
            handle_action(action_type)

if __name__ == "__main__":
    main()