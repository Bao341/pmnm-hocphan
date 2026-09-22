# BÁO CÁO PHÂN TÍCH BÀI TẬP 1.2: DỰ ÁN RẼ NHÁNH DO MÂU THUẪN CỘNG ĐỒNG
**Chủ đề:** Cuộc rẽ nhánh từ MySQL sang MariaDB và bài học về quyền sở hữu phần mềm mã nguồn mở

---

## 1. Giới thiệu tổng quan
Trong lịch sử phát triển của phần mềm mã nguồn mở (FOSS), sự kiện một dự án bị phân nhánh (fork) thường là kết quả của những mâu thuẫn không thể dung hòa giữa cộng đồng phát triển và nhà quản trị. Cuộc rẽ nhánh từ **MySQL sang MariaDB** năm 2009 là một trong những ví dụ điển hình nhất. Nó phản ánh sự xung đột gay gắt giữa mô hình quản trị doanh nghiệp khép kín và tinh thần tự do, minh bạch của cộng đồng nguồn mở.

---

## 2. Nguyên nhân mâu thuẫn
MySQL được phát triển từ năm 1995 bởi công ty MySQL AB và nhanh chóng trở thành hệ quản trị cơ sở dữ liệu mã nguồn mở phổ biến nhất thế giới. Tuy nhiên, bước ngoặt xảy ra vào năm 2008 khi Sun Microsystems mua lại MySQL AB, và sau đó đến lượt **Oracle Corporation** thâu tóm Sun Microsystems vào năm 2009–2010. 

Sự xuất hiện của Oracle – một gã khổng lồ nổi tiếng với các phần mềm thương mại đắt đỏ – đã dấy lên làn sóng lo ngại trong cộng đồng. Xung đột bùng nổ xung quanh các vấn đề chính:
- **Mối lo về bản quyền và độc quyền:** Giới lập trình viên lo sợ Oracle sẽ triệt hạ hoặc hạn chế tính năng của MySQL để bảo vệ cơ sở dữ liệu thương mại đắt tiền Oracle Database.
- **Thiếu minh bạch trong phát triển:** Oracle bắt đầu áp dụng quy trình phát triển đóng, hạn chế sự đóng góp của cộng đồng bên ngoài và khóa một số tính năng nâng cao (như Enterprise Plugins) đằng sau giấy phép trả phí.
- **Đóng góp của cộng đồng bị phớt lờ:** Các báo cáo lỗi và mã đóng góp (pull request) từ cộng đồng không còn được ưu tiên xử lý.

---

## 3. Diễn biến cuộc rẽ nhánh (Forking)
Trước nguy cơ "đứa con tinh thần" mất đi tính tự do, **Michael "Monty" Widenius** – nhà sáng lập chính của MySQL – đã quyết định rời đi cùng nhiều kỹ sư nòng cốt. Năm 2009, nhóm phát triển mở một mã nguồn mới dựa trên MySQL 5.1 và đặt tên là **MariaDB**. 

Mục tiêu ban đầu của MariaDB là trở thành một bản "thay thế trực tiếp" (drop-in replacement) hoàn toàn tương thích với MySQL. Để ngăn chặn kịch bản bị thâu tóm một lần nữa, **MariaDB Foundation** được thành lập – một tổ chức phi lợi nhuận độc lập nhằm đảm bảo dự án luôn hoàn toàn miễn phí và mã nguồn mở dưới giấy phép GNU GPL v2.

---

## 4. Kết quả và Tác động
Cuộc phân nhánh này đã làm thay đổi diện mạo của hệ sinh thái cơ sở dữ liệu:
- **Sự chuyển dịch của cộng đồng:** Hàng loạt hệ điều hành Linux lớn như Red Hat Enterprise Linux, Debian, Arch Linux và CentOS đã quyết định loại bỏ MySQL để chọn MariaDB làm cơ sở dữ liệu mặc định. Các nền tảng lớn như Wikipedia cũng chuyển sang dùng MariaDB.
- **Sự phân hóa kỹ thuật:** Ban đầu hai dự án rất giống nhau. Tuy nhiên qua thời gian, MariaDB đã bổ sung nhiều engine lưu trữ mới (Aria, ColumnStore, Spider), tối ưu hóa hiệu năng và cung cấp nhiều tính năng miễn phí mà MySQL bắt trả phí. Ngược lại, MySQL dưới sự dẫn dắt của Oracle phát triển phiên bản MySQL 8.0 với các công cụ nâng cao về JSON và Group Replication.

---

## 5. Bài học rút ra
Trường hợp MySQL và MariaDB mang lại những bài học đắt giá cho ngành công nghiệp phần mềm:
1. **Sức mạnh của cơ chế mã nguồn mở:** Giấy phép mã nguồn mở (như GPL) là tấm lá chắn bảo vệ người dùng. Khi một công ty muốn "thâu tóm" dự án, cộng đồng luôn có quyền tạo ra một bản rẽ nhánh để duy trì sự tự do.
2. **Tầm quan trọng của mô hình quản trị:** Sự thành công của MariaDB cho thấy tính minh bạch và sự tham gia của cộng đồng là chìa khóa giúp phần mềm mã nguồn mở phát triển bền vững.

---

## DANH MỤC TÀI LIỆU THAM KHẢO

1. **MariaDB Foundation.** *About MariaDB & History of MariaDB Corporation/Foundation.*  
   Website: [https://mariadb.org/about/](https://mariadb.org/about/)
2. **Oracle Corporation.** *Oracle and MySQL.*  
   Tài liệu thông cáo báo chí thương vụ thâu tóm Sun Microsystems (2009–2010).
3. **Widenius, M. (2009).** *Help Save MySQL!*  
   Bài viết kêu gọi bảo vệ dự án mã nguồn mở của nhà sáng lập MySQL.
4. **Free Software Foundation (FSF).** *GNU General Public License, version 2 (GPLv2).*  
   Cơ sở pháp lý cho phép thực hiện rẽ nhánh (forking) từ mã nguồn gốc.
5. **Red Hat & Debian Engineering Logs (2013).** *Migration from MySQL to MariaDB.*  
   Nhật ký kỹ thuật về việc chuyển đổi hệ quản trị CSDL mặc định trên các bản phân phối Linux.
