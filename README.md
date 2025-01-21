# Dự án xoá mail hàng loạt 

Dự án Xoá Email Hàng Loạt được tạo ra nhằm giải quyết những hạn chế của giao diện Gmail hiện tại, khi chưa có tính năng hỗ trợ xoá số lượng lớn email một cách dễ dàng. Người dùng chỉ có thể xoá tối đa 50 email mỗi lần, điều này khiến việc làm sạch inbox trở nên tốn thời gian và công sức. Hơn nữa, người dùng có thể vô tình xoá đi những email quan trọng khi thực hiện thao tác.

Dự án này tự động hoá quá trình xoá email hàng loạt, giúp tiết kiệm thời gian và giảm thiểu rủi ro xoá nhầm email quan trọng. Các tính năng chính của dự án bao gồm:

* Xoá email hàng loạt: Tính năng xoá toàn bộ email trong hộp thư đến hoặc theo các tiêu chí tuỳ chỉnh (ví dụ: mốc thời gian, số lượng email, tần suất gửi trung bình).

* Phát hiện email rác: Sử dụng hệ thống chấm điểm để đánh giá khả năng một email là rác, giúp người dùng ưu tiên xoá các email không mong muốn.

Dự án sử dụng IMAP để truy vấn email và PyAutoGUI để tự động hoá quá trình xoá, đảm bảo trải nghiệm xoá email nhanh chóng và hiệu quả.





# Hướng dẫn sử dụng
## Chuẩn bị

* Cài Đặt Python 3

Tải và cài đặt Python 3 từ trang chính thức [Python.org](https://www.python.org/).
Sau khi cài đặt, thiết lập biến môi trường để sử dụng Python từ mọi thư mục trên hệ thống.
Tham khảo hướng dẫn chi tiết tại đây: [Video hướng dẫn](https://youtu.be/ofzWMjQodbY?si=P2SVam0TZOb3X58X).

* Tạo mật khẩu ứng dụng gmail

Truy cập vào trang [Tài khoản google - mật khẩu ứng dụng](https://myaccount.google.com/apppasswords).
Đăng nhập và làm theo hướng dẫn để tạo mật khẩu ứng dụng.
Mật khẩu này sẽ được sử dụng để kết nối với Gmail qua IMAP.

* Cấu hình IMAP cho gmail

Truy cập trang [Chuyển tiếp và POP/IMAP](https://mail.google.com/mail/u/0/#settings/fwdandpop), sau đó chọn bật IMAP và bấm lưu cài đặt

* Cấu hình file credentials.yml

Mở file `crawData/credentials.yml` và thêm thông tin theo định dạng sau:

```yaml
email: "your-email@gmail.com"
password: "your-app-password"
```





## Thực thi

Chuột phải vào folder dự án -> chọn open in terminal, sau đó chạy file bằng lệnh:
```
python main.py
```
Sau đó làm theo các bước được hiển thị trên giao diện. Khi đến bước lấy toạ độ, mọi người lấy thông tin các điểm sao cho hoàn thành một chu kì xoá mail. Vậy là xong!





## Tác giả
Dự án có tham khảo cách giải nén email tại [AMT2 - Extracting Emails from your Gmail Inbox using python](https://youtu.be/K21BSZPFIjQ)

Mình là nguyenshyn - một sinh viên năm 4 của trường học viện Công nghệ Bưu chính viễn thông (PTIT). Dự án này mình làm chỉ với mục đích học tập, ắt hẳn sẽ còn nhiều thiết sót. Hy vọng mọi người sẽ để lại những đánh giá để mình có thể hoàn thiện bản thân hơn trong tương lai!

Contact: phannguyen2300@gmail.com
