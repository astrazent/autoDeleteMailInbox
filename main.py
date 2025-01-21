import subprocess
import psutil
import os
import sys
import time

def monitor_process(proc):
    """
    Giám sát tài nguyên (CPU, RAM) của quá trình đang chạy.
    """
    try:
        while proc.poll() is None:  # Kiểm tra nếu process còn chạy
            time.sleep(1)
            process_info = psutil.Process(proc.pid)
            print(f"CPU: {process_info.cpu_percent()}%, RAM: {process_info.memory_info().rss / (1024 * 1024):.2f} MB")
    except psutil.NoSuchProcess:
        pass

# Danh sách file tạm và script tương ứng
temp_files_and_scripts = {
    "temp/raw.txt": "crawAll.py",
    "temp/rmHtmlCss.txt": "cleanData/rmHtmlCss.py",
    "temp/rmOutSpaceAndQuotes.txt": "cleanData/rmOutSpaceAndQuotes.py",
    "temp/rmMidSpaceAndDecoding.txt": "cleanData/rmMidSpaceAndDecoding.py",
    "temp/convertToCsv.csv": "cleanData/convertToCsv.py",
    "temp/rmErrorData.csv": "cleanData/rmErrorData.py",
    "temp/classifyGroup.csv": "cleanData/classifyGroup.py",
    "temp/addQuantity.csv": "cleanData/addQuantity.py",
    "temp/addSimilarity.csv": "cleanData/addSimilarity.py",
    "temp/addCountSimilarAndRatio.csv": "cleanData/addCountSimilarAndRatio.py",
    "temp/addAvgAndTotalmonths.csv": "cleanData/addAvgAndTotalmonths.py",
    "temp/addFirstLastDateAndPeriod.csv": "cleanData/addFirstLastDateAndPeriod.py",
}

# Đường dẫn đến file chính
main_script = "dataAnalysis/analysis.py"

# Các file không cần kiểm tra bộ nhớ tạm
standalone_scripts = [
    "autoTool/grabColorAndMousePos.py",
    "autoTool/autoDelete.py",
]

# Lấy đường dẫn Python interpreter của môi trường ảo
python_exe = sys.executable

# Kiểm tra sự tồn tại của tất cả file tạm
all_temp_exist = all(os.path.exists(temp_file) for temp_file in temp_files_and_scripts.keys())

if all_temp_exist:
    # Nếu tất cả file tạm đã tồn tại, chạy trực tiếp file chính
    print("Bộ nhớ đệm đầy đủ. Chạy script chính...")
    subprocess.run([python_exe, main_script], shell=True)
else:
    # Nếu thiếu file tạm, xử lý từng file bị thiếu
    print("Bộ nhớ đệm bị thiếu. Đang bổ sung...")
    for temp_file, script in temp_files_and_scripts.items():
        if not os.path.exists(temp_file):
            print(f"Bộ nhớ đệm không tồn tại: {temp_file}. Đang bổ sung: {script}")
            proc = subprocess.Popen([python_exe, script])
            monitor_process(proc)

    # Chạy file chính sau khi hoàn thành xử lý các file tạm
    print("Hoàn thành bổ sung bộ nhớ. Chạy script chính...")
    subprocess.run([python_exe, main_script], shell=True)

# Thực thi các file không cần kiểm tra bộ nhớ tạm sau cùng
for script in standalone_scripts:
    print(f"Đang thực thi auto click: {script}")
    subprocess.run([python_exe, script], shell=True)
