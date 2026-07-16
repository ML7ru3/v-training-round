# DNS & Message

> Tài liệu này được lấy nguồn từ RFC 1034 và 1035

### RFC 1034

RFC 1034 tập trung vào việc mô tả các khải niệm cơ bản và cấu trúc của hệ thống Tên miền (DNS) bao gồm:
- Mục tiêu thiết kế và Các thành phần của DNS
- Không gian tên miền (Domain Name Space)
- Bản ghi tài nguyên (Resource Records - RR): Định nghĩa về các bản ghi tài nguyên.
- Name Servers:
    - Cách thức phân chia cơ sở dữ liệu DNS thành các vùng.
    - Hoạt động nội bộ của máy chủ tên
    - Việc bảo trì và chuyển vùng (zone transfers) giữa các máy chủ.
- Trình giải quyết tene (Resovlers): Mô tả giao diện giữa khách hàng và trình giải quyết, các thuật toán nội bộ và cách thức hoạt động của các trình giải quyết rút gọn (stub resolvers).


### RFC 1035

RFC 1035 tập trung vào các quy chuẩn kỹ thuật chính xác để các lập trình veien có thể xây dựng máy chủ và trình giải quyết tên miền.
- Định nghĩa chia tiết về Bản ghi tài nguyên (RR)
- Định dạng thông điệp (Messages)
- Giao thức truyền tải.
- Tệp tin chủ (Master Files)
- Triển khai máy chủ và trình giải quyết (Implementation): Hướng dẫn về kiến trúc cơ sở dữ liệu và thuật toán xử lý truy vấn chuẩn cho máy chủ.


