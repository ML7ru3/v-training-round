# Tài liệu Nghiên cứu: DNS & Message

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

RFC 1035 tập trung vào các quy chuẩn kỹ thuật chính xác để các lập trình viên có thể xây dựng máy chủ và trình giải quyết tên miền.
- Định nghĩa chia tiết về Bản ghi tài nguyên (RR)
- Định dạng thông điệp (Messages)
- Giao thức truyền tải.
- Tệp tin chủ (Master Files)
- Triển khai máy chủ và trình giải quyết (Implementation): Hướng dẫn về kiến trúc cơ sở dữ liệu và thuật toán xử lý truy vấn chuẩn cho máy chủ.

## Chi Tiết Nội Dung & Ví Dụ Minh Họa

### 1. Khái niệm & Thành phần, Cấu trúc DNS

#### A. Khái niệm
DNS (Domain Name System) là hệ thống phân giải tên miền phân tán toàn cầu, có chức năng chuyển đổi các tên miền dễ nhớ (như `google.com`) thành địa chỉ IP mà máy tính có thể hiểu được (như `142.250.190.46`).

#### B. Thành phần, Cấu trúc của DNS Message
Theo **RFC 1035**, tất cả các thông điệp DNS (cả truy vấn và phản hồi) đều sử dụng chung một cấu trúc định dạng gồm 5 phần chính:
1. **Header**: Chứa các thông tin điều khiển (ID, Flags, số lượng bản ghi trong các phần sau).
2. **Question**: Chứa câu hỏi truy vấn (Tên miền cần tra cứu, Loại bản ghi, Lớp bản ghi).
3. **Answer**: Chứa các Resource Records trả lời cho câu hỏi.
4. **Authority**: Chứa các Resource Records trỏ tới các Name Server có thẩm quyền quản lý tên miền.
5. **Additional**: Chứa các Resource Records bổ sung (ví dụ: địa chỉ IP của các Name Server ở phần Authority).

##### Ví dụ cấu trúc Header của DNS Message (12 bytes):
``` text
+---------------------+---------------------+
|    Identifier (ID)  |        Flags        |  -> Xác định session và trạng thái (QR, Opcode, AA, TC, RD, RA, RCODE)
+---------------------+---------------------+
| Total Questions     | Total Answer RRs    |  -> Số lượng câu hỏi và số lượng câu trả lời
+---------------------+---------------------+
| Total Authority RRs | Total Additional RRs|  -> Số lượng bản ghi thẩm quyền và bổ sung
+---------------------+---------------------+
```

---

### 2. Các Thuật Toán Truy Vấn DNS

Hệ thống DNS sử dụng hai cơ chế truy vấn chính để tìm kiếm địa chỉ IP:

#### A. Truy vấn Đệ quy (Recursive Query)
*   **Mô tả**: Client yêu cầu DNS Server (thường là ISP hoặc Public DNS như 8.8.8.8) tìm ra kết quả cuối cùng. DNS Server có trách nhiệm đi hỏi các server khác và chỉ trả về kết quả cuối cùng (Thành công hoặc Lỗi) cho Client.
*   **Ví dụ**: Bạn (Client) hỏi lễ tân khách sạn tìm giúp một nhà hàng ngon. Lễ tân tự đi tìm, hỏi đường, gọi điện và quay lại chỉ cho bạn địa chỉ chính xác.

#### B. Truy vấn Tương tác (Iterative Query)
*   **Mô tả**: DNS Server (Resolver) tự đi hỏi các Name Server theo cấp bậc. Nếu Server được hỏi không biết, nó sẽ phản hồi: *"Tôi không biết, nhưng hãy đi hỏi Server X này xem"*. Resolver sẽ tiếp tục mang câu hỏi đó đến Server X.
*   **Ví dụ**: 
    1. Resolver hỏi **Root Server (`.`)**: *"Địa chỉ của `example.com` ở đâu?"* -> Root Server trả về: *"Hãy hỏi TLD Server của `.com`"*.
    2. Resolver hỏi **TLD Server (`.com`)**: *"Địa chỉ của `example.com` ở đâu?"* -> TLD Server trả về: *"Hãy hỏi Authoritative Server của `example.com`"*.
    3. Resolver hỏi **Authoritative Server**: *"Địa chỉ của `example.com` ở đâu?"* -> Server trả về IP: `93.184.216.34`.

---

### 3. Tìm hiểu và Phân biệt các Bản ghi DNS (Resource Records - RR)

Dựa trên tài liệu chuyên sâu từ **[Mimecast]** và bài viết về **Reverse DNS (PTR)**, dưới đây là cách phân biệt các bản ghi quan trọng phục vụ cho vận hành Web và Email Delivery:

| Tên Bản Ghi | Ý nghĩa đầy đủ | Chức năng chính | Ví dụ thực tế |
| :--- | :--- | :--- | :--- |
| **A** | Address Record | Ánh xạ tên miền (IPv4) thành địa chỉ IP. | `google.com. IN A 142.250.190.46` |
| **AAAA** | IPv6 Address Record | Ánh xạ tên miền (IPv6) thành địa chỉ IP 128-bit. | `google.com. IN AAAA 2607:f8b0:4005:805::200e` |
| **CNAME** | Canonical Name | Tạo tên bí danh (Alias) trỏ tới một tên miền gốc khác. | `www.example.com. IN CNAME example.com.` |
| **MX** | Mail Exchange | Định tuyến email đến server nhận mail của tên miền đó (có độ ưu tiên). | `example.com. IN MX 10 mail.example.com.` |
| **TXT** | Text Record | Lưu trữ văn bản thô, thường dùng để xác thực cấu hình SPF, DKIM cho Email. | `example.com. IN TXT "v=spf1 include:mimecast.com ~all"` |
| **PTR** | Pointer Record | **Hệ thống DNS đảo ngược (Reverse DNS)**: Ánh xạ từ IP sang Tên miền. Rất quan trọng để bộ lọc Spam xác thực Mail Server hợp lệ. | `46.190.250.142.in-addr.arpa. IN PTR mail.google.com.` |
| **NS** | Name Server | Xác định máy chủ DNS nào có thẩm quyền giữ các bản ghi của tên miền này. | `example.com. IN NS ns1.hoosting.com.` |
| **SOA** | Start of Authority | Chứa thông tin quản trị cốt lõi của Zone tên miền (Serial number, Refresh rate, Email Admin). | `example.com. IN SOA ns1.ex.com. admin.ex.com. (...)` |

#### Ví dụ về Ứng dụng trong Email Delivery:
Khi một mail server gửi thư từ IP `1.2.3.4` với danh nghĩa là `sender@company.com`, hệ thống nhận sẽ kiểm tra:
1. **Kiểm tra PTR**: Tra cứu ngược IP `1.2.3.4` xem có trỏ về `mail.company.com` hay không. Nếu không có bản ghi PTR, các bộ lọc Spam (Spam Filters) sẽ đánh dấu thư này là Spam hoặc từ chối nhận.
2. **Kiểm tra TXT (SPF)**: Tra cứu bản ghi `TXT` của `company.com` xem IP `1.2.3.4` có nằm trong danh sách các IP được phép gửi mail hay không.

---

### 4. An ninh DNS: DNS Cache Poisoning & DNS Tunneling

#### A. DNS Cache Poisoning (Nhiễm độc bộ nhớ đệm / DNS Spoofing)
*   **Khái niệm**: Kẻ tấn công chèn dữ liệu DNS giả mạo vào bộ nhớ đệm (cache) của một DNS Resolver (ví dụ: DNS của nhà mạng). Kết quả là người dùng khi gõ tên miền hợp pháp sẽ bị chuyển hướng đến website lừa đảo của kẻ tấn công.
*   **Ví dụ**: 
    *   Người dùng muốn vào `mybank.com`.
    *   DNS Resolver chưa có sẵn cache liền đi hỏi Authoritative Server.
    *   Kẻ tấn công nhanh tay gửi một phản hồi giả mạo (Fake Response) chứa IP của máy chủ lừa đảo trước khi Server thật kịp trả lời.
    *   DNS Resolver tin tưởng lưu lại IP giả này vào Cache. Từ đó, toàn bộ người dùng dùng DNS này truy cập `mybank.com` đều bị đưa tới trang web giả mạo để lấy cắp thông tin tài khoản.

#### B. DNS Tunneling (Đường hầm DNS)
*   **Khái niệm**: Là kỹ thuật lợi dụng giao thức DNS (thường chạy cổng 53 UDP công khai và ít bị tường lửa chặn) để truyền tải lén lút các dữ liệu phi DNS (như dữ liệu HTTP, SSH, Malware Command & Control). Kẻ tấn công sử dụng các truy vấn DNS đối với các sub-domain để giấu dữ liệu mã hóa bên trong.
*   **Ví dụ**: 
    *   Một máy tính trong mạng nội bộ bị nhiễm mã độc và muốn gửi dữ liệu nhạy cảm `SotaiKhoan12345` ra ngoài, nhưng tường lửa đã chặn toàn bộ cổng HTTP/HTTPS đi ra ngoài internet.
    *   Mã độc tiến hành mã hóa dữ liệu thành chuỗi Base64: `U290YWlLaG9hbjEyMzQ1`.
    *   Nó gửi một yêu cầu DNS truy vấn tên miền: `U290YWlLaG9hbjEyMzQ1.attacker-domain.com`.
    *   Yêu cầu này đi qua hệ thống DNS nội bộ hợp lệ để đến được Authoritative Server của kẻ tấn công (`attacker-domain.com`). 
    *   Tại máy chủ của kẻ tấn công, nó sẽ trích xuất phần sub-domain ra và giải mã để lấy lại chuỗi `SotaiKhoan12345`. Dữ liệu đã được đánh cắp thành công mà không làm kích hoạt cảnh báo của tường lửa truyền thống.
