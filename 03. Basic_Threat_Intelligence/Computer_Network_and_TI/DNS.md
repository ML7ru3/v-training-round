# Domain Name System (DNS)

Hệ thống phân giải tên miền (DNS - Domain Name System) là một thành phần thiết yếu của Internet, đóng vai trò như một "danh bạ" giúp chuyển đổi các tên miền dễ nhớ (như `google.com`) thành các địa chỉ IP mà máy tính có thể hiểu được.

## Dịch vụ và Chức năng chính

Nhiệm vụ cốt lõi của DNS là phân giải tên miền thành địa chỉ IP. Ngoài ra, nó còn cungcapas các dịch vụ quan trọng khác:

- Host aliasing (Bí danh host): một máy chủ có thể có một tên miền chính và nhiều tên miền phụ dễ nhớ hơn.
- Mail server aliasing: Giúp địa chỉ email trở nên dễ nhớ hơn.
- Load distribution (Phân tải): DNS có thể thực hiện xoay vòng (DNS rotation) các địa chỉ IP của các máy chủ được nhân bản để phân phối lưu lượng truy cập.

## Cấu trúc phân tầng của DNS

DNS hoạt động theo mô hình cơ sở dữ liệu phân tán và có thứ bậc để đảm bảo khả năng mở rộng:

- Root Servers (máy chủ gốc): Tầng cao nhất trong các hệ thống, cung cấp địa chỉ IP của các máy chủ TLD.
- Top-Level Domain (TLD) Servers: Quản lý các phần mở rộng tên miền như  `.com`, `.org` và các mã quốc gia như `.vn`, `.jp`.
- Authoritive Servers (Máy chủ có thẩm quyền): Nơi lưu trữ các hố sơ DNS thực tế của một tổ chức, cung cấp ánh xạ chính xác từ tên host sang địa chỉ IP.
- Local DNS Server: Thường được ISP cung cấp, đóng vai trò như một proxy trung gian để chuyển tiếp các truy vấn của người dùng vào hệ thống phân tầng.

## Quá trình phân giải DNS (DNS Lookup)

Đây là quy trình chuyển đổi tên miền thành IP qua các loại truy vấn:

- Recursive Query (Truy vấn đệ quy): Máy khách yêu cầu trình phân giải (resolver) thực hiện toàn bộ quá trình tìm kiếm trả về kết quả cuối cùng hoặc lỗi.
- Iterative Query (Truy vấn lặp): Máy chủ DNS trả về thông tin tốt nhất mà nó có hoặc trỏ tới một máy chủ DNS khác có khả năng biết câu trả lời.
- DNS Caching: Kỹ thuật lưu trữ tạm thời kết quả phân giải để giảm thời gian phản hồi hco các yêu cầu lặp lại và giải tảm hệ thống.

## Các loại bản ghi (DNS Record Types)

Mỗi bản ghi DNS là một bộ 4 thông tin (Name, Value, Type, TTL). Các loại phổ biến bao gồm:

- Bản ghi A: Ánh xạ tên host sang địa chỉ IPv4
- Bản ghi CNAME: tạo bí danh trỏ từ tên miền này sang tên miền khác.
- Bản ghi MX: Xác định máy chủ thư điện tử chịu trách nhiệm nhận email cho tên miền
- Bản ghi TXT: Lưu trữ thông tin văn bản phục vụ xác minh và bảo mật email.
- Bản ghi NS: Xác định máy chủ DNS có thẩm quyền của một miền.

> TTL (Time-to-live): Đây là một giá trị xác định thời gian một bản ghi DNS được phép lưu lại trong bộ nhớ đệm (cache) trước khi cần phải thực hiện một truy vấn mới để cập nhật thông tin.

## Bảo mật DNS

Vì DNS là cơ sở hạ tầng quan trọng, nó thường là mục tiêu của các cuộc tấn công như **DDoS** hoặc **DNS Poisoning** (đưa thông tin sai lệch vào cache).