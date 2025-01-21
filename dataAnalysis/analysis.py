import pandas as pd
from datetime import datetime, timedelta

def interface_cleaner():
    while True:
        # Hỏi người dùng chọn chức năng
        print("Chọn chức năng muốn xoá:")
        print("1. Chỉ xoá mail rác")
        print("2. Xoá toàn bộ")
        choice = input("Nhập số (1 hoặc 2): ")

        if choice == "1":
            print("Bạn đã chọn: Chỉ xoá mail rác.")
            break
        elif choice == "2":
            print("Bạn đã chọn: Xoá toàn bộ.")
            deleteAll()
            print("-----------------------------------------------------------")
            print("Hãy xoá các mail mà bạn không muốn xoá trong file.")
            while True:
                try:
                    ask = int(input("Nhập số 1 để hoàn tất, số 2 để dừng (1 hoặc 2): "))
                    if ask == 1:
                        exportToTarget(0)
                        return "Lấy danh sách thành công!"
                    elif ask == 2:
                        return "Dừng chương trình."
                    else:
                        print("Lựa chọn không hợp lệ, vui lòng nhập lại.")
                except ValueError:
                    print("Vui lòng nhập một số hợp lệ.")
        else:
            print("Lựa chọn không hợp lệ. Vui lòng nhập lại.")

    # Hỏi thêm các tiêu chí từ người dùng
    while True:
        try:
            print("-----------------------------------------------------------")
            T = int(input("Bạn quan tâm đến những email trong khoảng bao nhiêu ngày trở lại đây? (ngày): "))
            B = int(input("Theo bạn tổng số lượng inbox của một mail nên là bao nhiêu thì phù hợp? (inbox): "))
            C = float(input("Bạn thấy tần suất mail gửi tới nên là bao nhiêu thì phù hợp? (mail/tháng): "))
            break
        except ValueError:
            print("Vui lòng nhập giá trị hợp lệ.")

    # Hỏi tiêu chí hay dùng thuật toán
    while True:
        print("-----------------------------------------------------------")
        print("Bạn muốn xoá theo tiêu chí nêu trên hay dùng thuật toán để phân loại mail rác?")
        print("1. Xoá theo tiêu chí")
        print("2. Dùng thuật toán (đề xuất một danh sách email đã lọc)")
        method_choice = input("Nhập số (1 hoặc 2): ")

        if method_choice == "1":
            while True:
                # Lựa chọn tiêu chí để xoá
                print("Bạn đã chọn: Xoá theo tiêu chí.")
                print("-----------------------------------------------------------")
                print(f"1. Tổng số lượng inbox của một mail lớn hơn {B} inbox")
                print(f"2. Tần suất mail gửi lớn hơn {C} mail/tháng")
                print(f"3. Email không nằm trong khoảng {T} ngày trở lại đây")
                criterion = input("Nhập số tiêu chí (1, 2 hoặc 3): ")

                if criterion == "1":
                    deleteByInbox(B)
                elif criterion == "2":
                    deleteByFrequency(C)
                elif criterion == "3":
                    deleteByDate(T)
                else:
                    print("Lựa chọn tiêu chí không hợp lệ. Vui lòng nhập lại.")
                    continue

                print("-----------------------------------------------------------")
                print("Hãy xoá các dòng mà bạn không muốn xoá trong file.")
                while True:
                    try:
                        ask = int(input("Nhập số 1 để hoàn tất, số 2 để dừng (1 hoặc 2): "))
                        if ask == 1:
                            exportToTarget(int(criterion))
                            return "Lấy danh sách thành công!"
                        elif ask == 2:
                            return "Dừng chương trình."
                        else:
                            print("Lựa chọn không hợp lệ, vui lòng nhập lại.")
                    except ValueError:
                        print("Vui lòng nhập một số hợp lệ.")
                break

        elif method_choice == "2":
            # Dùng thuật toán đề xuất danh sách
            print("-----------------------------------------------------------")
            print("Bạn đã chọn: Dùng thuật toán để phân loại mail rác.")
            print("Hệ thống đang xử lý, vui lòng chờ trong giây lát!")
            print("...")
            deleteWithAI()
            print("-----------------------------------------------------------")
            print("Hãy xoá các dòng mà bạn không muốn xoá trong file.")
            while True:
                try:
                    ask = int(input("Nhập số 1 để hoàn tất, số 2 để dừng (1 hoặc 2): "))
                    if ask == 1:
                        exportToTarget(4)
                        return "Lấy danh sách thành công!"
                    elif ask == 2:
                        return "Dừng chương trình."
                    else:
                        print("Lựa chọn không hợp lệ, vui lòng nhập lại.")
                except ValueError:
                    print("Vui lòng nhập một số hợp lệ.")
        else:
            print("Lựa chọn không hợp lệ. Vui lòng nhập lại.")

# Hàm tính điểm và trả về trạng thái
def calculate_score(row):
    score = 0
    # interface_cleaner()
    reason_reward = []
    reason_punish = []
    # Điều kiện 0: Những nhóm ưu tiên cao => điểm càng thấp
    if row['Group'] == 1:
        score -= 2

    if row['Group'] == 2:
        score -= 10

    # Điều kiện 1: Những mail có từ khoá @gmail
    if isinstance(row['Email'], str) and "@gmail" in row['Email']:
        score -= 2
        reason_reward.append("have @gmail")

    # Điều kiện 2: Nếu tỉ lệ tương đồng tương đối cao => nhiều mail giống với nó => rác
    if row['Similarity'] >= 0.6:
        score += 1
        reason_punish.append("high similarity")

    # Điều kiện 3: Nếu tỉ lệ tương đồng tuyệt đối cao => nhiều mail giống nhau => rác
    if row['Similarity ratio'] >= 0.5:
        score += 1
        reason_punish.append("high similarity ratio")

    # Điều kiện 4: Nếu mail có số lượng lớn và tần suất trung bình từ đều đặn đến cao => rác
    if row['Quantity'] >= 30 and row['Quantity']  / (row['Period (day)'] / 30) >= 3:
        score += 1
        reason_punish.append("high quantity")

        # Gửi rất nhiều và rất đều => subscription => rác
        if row['Total months with email'] / (row['Period (day)'] / 30) > 0.6:
            score += 1
            reason_punish.append("long term")

        # Gửi rất nhiều nhưng trong thời gian ngắn => rác
        if row['Total months with email'] / (row['Period (day)'] / 30) < 0.3:
            score += 1
            reason_punish.append("a lot in short time")

    # Điều kiện 5: Những mail ở phía sau khoảng 30% thời gian và thời gian đó tối thiểu là T thì được coi là mail cũ
    try:
        if isinstance(row['Last date'], str):
            last_date = datetime.strptime(row['Last date'], '%Y-%m-%d')
            old_date = last_date - pd.to_timedelta(row['Period (day)'] * 0.3, unit='D')
            if (datetime.now() - old_date).days >= 30:
                score += 1
                reason_punish.append("old date")
    except (ValueError, TypeError):
        print(row['ID'])
        pass  # Bỏ qua nếu không thể chuyển đổi định dạng ngày tháng

    # Điều kiện 6: Những mail có tần suất hội tụ cao và thời điểm hội tụ sau T thì không dùng nữa
    try:
        if isinstance(row['Last date'], str):
            last_date = datetime.strptime(row['Last date'], '%Y-%m-%d')
            if (datetime.now() - last_date).days > 30:
                if row['Avg send per month'] > 3 * 1.5:
                    score += 1
                    reason_punish.append("a lot in short time & no longer used")
    except (ValueError, TypeError):
        print(row['ID'])
        pass  # Bỏ qua nếu không thể chuyển đổi định dạng ngày tháng

    # Điều kiện loại biên
    if row['Quantity'] >= 30 * 2:
        score += 2
        reason_punish.append("too much")

    if row['Similarity'] >= 0.8:
        score += 2
        reason_punish.append("too similar")

    if row['Avg send per month'] > 3 * 2:
        score += 2
        reason_punish.append("too high frequency")

    if 30 * 3 < 300 and row['Period (day)'] > 30 * 3:
        score += 2
        reason_punish.append("very long time")

    elif row['Period (day)'] > 30:
        score == 2
        reason_punish.append("very long time")

    reward = ", ".join(reason_reward)
    punish = ", ".join(reason_punish)

    # Trả về điểm, trạng thái "hoàn thành", và thêm chuỗi mới "Xử lý xong"
    return score, reward, punish

# Hàm xử lý dữ liệu và thêm cột Status và Process_Status
def deleteWithAI():
    # Đọc dữ liệu từ file CSV
    input_file = "temp/addFirstLastDateAndPeriod.csv"  # Đường dẫn tới file CSV đầu vào
    output_file = "temp/analysis.csv"  # Đường dẫn tới file CSV đầu ra
    data = pd.read_csv(input_file)

    # Tính điểm cho từng dòng và thêm vào cột mới "Score", "Reward reason", và "Punish reason"
    data[['Score', 'Reward reason', 'Punish reason']] = data.apply(calculate_score, axis=1, result_type="expand")

    # Xuất dữ liệu ra file CSV mới
    data.to_csv(output_file, index=False)

    # Hiển thị danh sách cho người dùng
    file_path = 'temp/analysis.csv'  # Đổi tên file đầu vào của bạn ở đây
    output_path = 'result.csv'  # Đường dẫn file xuất ra
    listFile = pd.read_csv(file_path)

    # Bước 1: Chỉ lấy cột ID, Sender, và Body (Body chỉ lấy 15 từ đầu tiên)
    listFile['Body'] = listFile['Body'].apply(lambda x: ' '.join(str(x).split()[:10]))  # Chỉ lấy 10 từ đầu tiên trong Body

    # Bước 2: Kiểm tra và thay thế 'Sender' nếu bắt đầu bằng '=utf-8'
    listFile['Sender'] = listFile['Sender'].apply(lambda x: 'error name' if isinstance(x, str) and x.startswith('=?utf-8') else x)

    # Bước 3: Loại bỏ các dòng trùng lặp theo email
    # Tạo một bản sao rõ ràng của DataFrame để đảm bảo không gặp lỗi SettingWithCopyWarning
    data_sorted = listFile.sort_values(by='Count similar values')  # Sắp xếp theo Count similar values tăng dần
    unique_emails = data_sorted.drop_duplicates(subset='Email', keep='first').copy()  # Tạo bản sao rõ ràng

    # Bước 4: Tính trung bình của Score cho mỗi nhóm email
    # Sử dụng .loc[] để gán giá trị rõ ràng và tránh cảnh báo
    unique_emails['Score'] = unique_emails.groupby('Email')['Score'].transform('mean').values

    # Bước 5: Lựa chọn các cột ID, Sender, Body, và Score
    final_data = unique_emails[['ID', 'Sender', 'Email', 'Body', 'Reward reason', 'Punish reason', 'Score']]

    # Sắp xếp dữ liệu theo cột 'Score'
    df_sorted = final_data.sort_values(by='Score', ascending=False)

    # Bước 6: Xuất ra file CSV mới
    df_sorted.to_csv(output_path, index=False)

    print(f"Danh sách cuối cùng được in ra tại: {output_path}")


def deleteAll():
    file_path = 'temp/addFirstLastDateAndPeriod.csv'  # Đổi tên file đầu vào của bạn ở đây
    output_path = 'result.csv'  # Đường dẫn file xuất ra
    listFile = pd.read_csv(file_path)

    # Chỉ lấy cột ID, Sender, và Body (Body chỉ lấy 15 từ đầu tiên)
    listFile['Body'] = listFile['Body'].apply(lambda x: ' '.join(str(x).split()[:15]))  # Chỉ lấy 15 từ đầu tiên trong Body

    # Kiểm tra và thay thế 'Subject' nếu bắt đầu bằng '=utf-8'
    listFile['Sender'] = listFile['Sender'].apply(lambda x: 'error name' if isinstance(x, str) and x.startswith('=?utf-8') else x)

    # Loại bỏ các dòng trùng lặp theo email
    # Chúng ta sẽ nhóm theo cột 'Email' và lấy dòng có 'Count similar values' bé nhất
    data_sorted = listFile.sort_values(by='Count similar values')  # Sắp xếp theo Count similar values tăng dần
    unique_emails = data_sorted.drop_duplicates(subset='Email', keep='first')  # Lấy dòng đầu tiên của mỗi email

    # Sắp xếp dữ liệu theo cột 'Score'
    df_sorted = unique_emails.sort_values(by='Email')

    # Lựa chọn các cột ID, Sender, Body
    final_data = df_sorted[['ID', 'Sender', 'Email', 'Body']]

    # Xuất ra file CSV mới
    final_data.to_csv(output_path, index=False)

    print(f"Danh sách cuối cùng được in ra tại: {output_path}")

def deleteByInbox(inbox):
    # Đường dẫn tới tệp CSV
    input_file = 'temp/addFirstLastDateAndPeriod.csv'
    output_file = 'result.csv'

    # Đọc file CSV vào DataFrame
    df = pd.read_csv(input_file)

    df['Body'] = df['Body'].apply(lambda x: ' '.join(str(x).split()[:15]))  # Chỉ lấy 15 từ đầu tiên trong Body

    # Loại bỏ các dòng trùng lặp theo email
    # Chúng ta sẽ nhóm theo cột 'Email' và lấy dòng có 'Count similar values' bé nhất
    data_sorted = df.sort_values(by='Count similar values')  # Sắp xếp theo Count similar values tăng dần
    unique_emails = data_sorted.drop_duplicates(subset='Email', keep='first')  # Lấy dòng đầu tiên của mỗi email

    # Lọc các dòng có giá trị cột 'Sum' > inbox
    filtered_df = unique_emails[unique_emails['Quantity'] > inbox]

    # Sắp xếp dữ liệu theo cột 'Quantity'
    df_sorted = filtered_df.sort_values(by='Quantity', ascending=False)

    # Lựa chọn các cột ID, Sender, Body
    final_data = df_sorted[['ID', 'Sender', 'Email', 'Body', 'Quantity']]

    # Ghi các dòng lọc được vào file mới
    final_data.to_csv(output_file, index=False)

    print(f"Lọc thành công! Các mail có tổng trên {inbox} đã được lưu vào '{output_file}'.")

def deleteByFrequency(freq):
    # Đường dẫn tới tệp CSV
    input_file = 'temp/addFirstLastDateAndPeriod.csv'
    output_file = 'result.csv'

    # Đọc file CSV vào DataFrame
    df = pd.read_csv(input_file)

    df['Body'] = df['Body'].apply(lambda x: ' '.join(str(x).split()[3:17]))  # Chỉ lấy 10 từ ở khoảng giữa Body

    # Lọc các dòng có giá trị cột 'Sum' > inbox
    filtered_df = df[df['Avg send per month'] > freq]

    df_sorted = filtered_df.sort_values(by='Avg send per month', ascending=False)

    # Lựa chọn các cột ID, Sender, Body
    final_data = df_sorted[['ID', 'Sender', 'Email', 'Body', 'Avg send per month']]

    # Ghi các dòng lọc được vào file mới
    final_data.to_csv(output_file, index=False)

    print(f"Lọc thành công! Các dòng có tần suất trên {freq} đã được lưu vào '{output_file}'.")

def deleteByDate(period):
    # Đường dẫn tới tệp CSV
    input_file = 'temp/addFirstLastDateAndPeriod.csv'
    output_file = 'result.csv'

    # Đọc file CSV vào DataFrame
    df = pd.read_csv(input_file)

    df['Body'] = df['Body'].apply(lambda x: ' '.join(str(x).split()[3:17]))  # Chỉ lấy 10 từ ở khoảng giữa Body

    # Chuyển cột 'Date' thành kiểu dữ liệu datetime
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    # Tính thời điểm hiện tại cộng 30 ngày
    current_date_plus_period = datetime.now() - timedelta(days=period)

    # Lọc các dòng có 'Date' sau thời điểm hiện tại + 30 ngày
    filtered_df = df[df['Date'] < current_date_plus_period]

    # Sắp xếp dữ liệu theo cột 'Score'
    df_sorted = filtered_df.sort_values(by='Date', ascending=False)

    # Lựa chọn các cột ID, Sender, Body
    final_data = df_sorted[['ID', 'Sender', 'Email', 'Body', 'Date']]

    # Ghi các dòng lọc được vào file mới
    final_data.to_csv(output_file, index=False)

    print(f"Lọc thành công! Các mail được nhận trước {current_date_plus_period} đã được lưu vào '{output_file}'.")

def exportToTarget(type):
    # Đường dẫn tới tệp CSV
    input_file = 'result.csv'
    output_file = 'scripts/target.txt'

    # Đọc file CSV
    df = pd.read_csv(input_file)

    if type == 0 or type == 4 or type == 1:
        column = df['Email']
    else:
        column = df['Body']

    nan_log_file = "temp/nan_log.txt"  # Tên file log cho các dòng NaN

    with open(output_file, 'w', encoding='utf-8') as out_file, open(nan_log_file, 'w', encoding='utf-8') as log_file:
        for index, value in zip(column.index, column):  # Duyệt qua index và giá trị của cột
            if pd.notna(value):  # Kiểm tra nếu giá trị không phải NaN
                out_file.write(f"{value}\n")
            else:
                id_value = df.loc[index, 'ID']  # Lấy giá trị ID từ DataFrame
                log_file.write(f"NaN found at ID: {id_value}\n")

    print(f"Xuất dữ liệu cần xoá sang file mục tiêu \u2713")

interface_cleaner()
