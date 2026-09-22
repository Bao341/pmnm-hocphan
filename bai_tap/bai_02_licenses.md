

|Name|Version|License|
|-|-|-|
|Django|5.2.17|BSD-3-Clause|
|Flask|3.1.3|BSD-3-Clause|
|Jinja2|3.1.6|BSD License|
|MarkupSafe|3.0.3|BSD-3-Clause|
|PyQt5|5.15.11|GPL v3|
|PyQt5-Qt5|5.15.2|LGPL v3|
|PyQt5\_sip|12.19.0|BSD-2-Clause|
|Werkzeug|3.1.8|BSD-3-Clause|
|amqp|5.4.0|BSD License|
|asgiref|3.12.1|BSD License|
|billiard|4.3.0|BSD License|
|blinker|1.9.0|MIT License|
|celery|5.6.3|BSD-3-Clause|
|certifi|2026.7.22|Mozilla Public License 2.0 (MPL 2.0)|
|charset-normalizer|3.5.1|MIT|
|click|8.5.0|BSD-3-Clause|
|click-didyoumean|0.3.1|MIT License|
|click-plugins|1.1.1.2|BSD License|
|click-repl|0.4.0|MIT|
|contourpy|1.3.3|BSD License|
|cycler|0.12.1|BSD License|
|fonttools|4.65.0|MIT|
|gunicorn|26.2.0|MIT|
|idna|3.20|BSD-3-Clause|
|itsdangerous|2.2.0|BSD License|
|kiwisolver|1.5.1|BSD License|
|kombu|5.6.2|BSD-3-Clause|
|matplotlib|3.11.2|Python Software Foundation License|
|mpmath|1.3.0|BSD License|
|numpy|2.4.6|BSD-3-Clause AND 0BSD AND MIT AND Zlib AND CC0-1.0|
|packaging|26.3|Apache-2.0 OR BSD-2-Clause|
|pandas|3.0.6|BSD License|
|pillow|12.3.0|MIT-CMU|
|prompt\_toolkit|3.0.53|BSD License|
|pyparsing|3.3.3|MIT|
|python-dateutil|2.9.0.post0|Apache Software License; BSD License|
|requests|2.34.2|Apache Software License|
|six|1.17.0|MIT License|
|sqlparse|0.6.0|BSD License|
|sympy|1.14.0|BSD License|
|typing\_extensions|4.16.0|PSF-2.0|
|tzdata|2026.4|Apache-2.0|
|tzlocal|5.4.4|MIT|
|urllib3|2.8.0|MIT|
|vine|5.1.0|BSD License|



\---



\## PHÂN TÍCH NGHĨA VỤ PHÁT SINH CHO DỰ ÁN THƯƠNG MẠI ĐÓNG NGUỒN



\### 1. Xác định các gói thuộc nhóm Copyleft mạnh (Strong Copyleft)

Qua bảng kiểm tra trên, gói \*\*PyQt5\*\* (hoặc các thư viện tương tự như \*GPL-Readline\*) sử dụng giấy phép \*\*GNU General Public License v3 (GPL v3)\*\*. Đây là giấy phép thuộc nhóm \*\*Copyleft mạnh\*\*.



\### 2. Phân tích nghĩa vụ phát sinh đối với dự án thương mại đóng nguồn

Nếu dự án của chúng ta là phần mềm thương mại đóng nguồn (Proprietary Software), việc tích hợp các thư viện trên phát sinh các nghĩa vụ pháp lý quan trọng:



\* \*\*Đối với các gói nhóm Permissive (MIT, BSD, Apache 2.0):\*\*

&#x20; - \*\*Nghĩa vụ:\*\* Rất linh hoạt, chỉ cần giữ lại thông báo bản quyền (Copyright Notice) và bản văn giấy phép gốc trong tài liệu đi kèm.

&#x20; - \*\*Quyền hạn:\*\* Được phép giữ kín mã nguồn thương mại của dự án.



\* \*\*Đối với gói Copyleft mạnh (PyQt5 - GPL v3):\*\*

&#x20; - \*\*Hiệu ứng lan truyền (Virality Effect):\*\* Nếu dự án đóng nguồn liên kết (link) hoặc tích hợp trực tiếp với thư viện GPL v3 và phân phối đến tay người dùng, toàn bộ mã nguồn của dự án thương mại sẽ bị coi là "sản phẩm phái sinh" (Derivative Work).

&#x20; - \*\*Bắt buộc mở mã nguồn:\*\* Chúng ta \*\*bắt buộc phải công khai toàn bộ mã nguồn\*\* của sản phẩm thương mại dưới giấy phép GPL v3 cho khách hàng/cộng đồng.

&#x20; - \*\*Mâu thuẫn:\*\* Nghĩa vụ này triệt hạ hoàn toàn mô hình kinh doanh phần mềm thương mại đóng nguồn độc quyền.



\### 3. Giải pháp khuyến nghị

\- \*\*Thay thế thư viện:\*\* Chuyển từ `PyQt5` (GPL v3) sang `PySide6` (sử dụng giấy phép LGPL - dẻo hơn cho phần mềm thương mại) hoặc dùng giao diện Web (Flask/FastAPI).

\- \*\*Tách biệt kiến trúc:\*\* Nếu bắt buộc dùng gói GPL, phải tách thành một dịch vụ độc lập (Microservice/Process riêng) và giao tiếp qua mạng (HTTP API) thay vì import trực tiếp.

