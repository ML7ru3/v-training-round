# Tài liệu Nghiên cứu: Giao thức SMTP (Simple Mail Transfer Protocol)

---

## Bảng Tổng Quan Nội Dung và Nguồn Tham Khảo

| Nội dung cần tìm hiểu | Nguồn tài liệu cho phép tìm hiểu |
| :--- | :--- |
| **1. Giao thức SMTP: Khái niệm & Mô hình Client-Server**<br>- Khái niệm cơ bản.<br>- Vai trò của MTA, Mail Relay, và Mail Gateway.<br>- Cơ chế hoạt động chung. | RFC 5321 (Simple Mail Transfer Protocol) |
| **2. Các port tiêu chuẩn và Đánh giá bảo mật**<br>- So sánh Port 25, 465, 587.<br>- Đánh giá rủi ro an ninh mạng. | RFC 5321 & Các tài liệu Best Practice về Email Security |
| **3. SMTP Transaction & Response Codes**<br>- Quy trình bắt tay và trao đổi lệnh (HELO/EHLO, MAIL FROM, RCPT TO, DATA).<br>- Hệ thống mã phản hồi (Response Codes). | RFC 5321 (Simple Mail Transfer Protocol) |
| **4. Sự khác biệt giữa Envelope và Header**<br>- Phân biệt Mail Envelope và Mail Header.<br>- Ý nghĩa bảo mật và định tuyến. | Bài viết về "Envelope Sender vs Header Sender" |
| **5. SMTP Relay & Open Relays**<br>- Cơ chế hoạt động của SMTP Relay.<br>- Nguy cơ từ lỗ hổng Open Relay. | [Mailtrap] SMTP Relay / Open Relay explained |

---

## Chi Tiết Nội Dung & Ví Dụ Minh Họa

### 1. Khái niệm, Mô hình Client-Server & Cấu trúc Thành phần

#### A. Khái niệm & Mô hình Client-Server
SMTP (Simple Mail Transfer Protocol) là giao thức truyền tải thư điện tử tiêu chuẩn, hoạt động theo **mô hình Client-Server** ở tầng ứng dụng TCP/IP. Thiết bị gửi đóng vai trò là **SMTP Client** (bắt đầu kết nối) và thiết bị nhận đóng vai trò là **SMTP Server** (lắng nghe kết nối).

#### B. Cấu trúc và Thành phần cốt lõi (MTA, Relay, Gateway)
Theo **RFC 5321**, một email đi từ người gửi đến người nhận phải đi qua các thành phần chức năng sau:
*   **MUA (Mail User Agent)**: Ứng dụng email của người dùng (ví dụ: Outlook, Thunderbird, Webmail). MUA đóng vai trò Client gửi mail lên server.
*   **MTA (Mail Transfer Agent)**: Phần mềm máy chủ có nhiệm vụ tiếp nhận email từ MUA hoặc từ các MTA khác, xử lý định tuyến thông qua DNS (bản ghi MX) và chuyển tiếp email đi. (Ví dụ: Postfix, Exim, Sendmail).
*   **Mail Relay (SMTP Relay)**: Quá trình hoặc máy chủ trung gian nhận email từ một tổ chức/hệ thống tin cậy và chuyển tiếp nó đến một server đích khác.
*   **Mail Gateway (Secure Email Gateway)**: Máy chủ SMTP đóng vai trò như một chốt chặn ở biên mạng. Nó thường thực hiện các tác vụ lọc Spam, kiểm tra Virus, quét mã độc trước khi cho phép mail đi vào hoặc đi ra hệ thống nội bộ.

##### Ví dụ luồng hoạt động:
``` text
[Người gửi] -> MUA -> [MTA nội bộ] -> [Mail Gateway (Quét virus/Spam)] -> Internet -> [MTA đích] -> MDA -> [Hộp thư người nhận]
```

---

### 2. Các Port Tiêu Chuẩn & Đánh Giá Bảo Mật

Việc lựa chọn port kết nối ảnh hưởng rất lớn tới tính bảo mật và khả năng phân phát thư.

| Port | Tên gọi / Cơ chế | Vai trò chính | Đánh giá bảo mật |
| :--- | :--- | :--- | :--- |
| **25** | SMTP Standard | Dùng cho việc giao tiếp, truyền tải email **giữa các MTA** (Server-to-Server) với nhau trên Internet. | **Kém bảo mật**. Dữ liệu mặc định truyền dưới dạng clear-text. Hiện nay hầu hết các ISP dân dụng đều chặn port này để ngăn chặn mã độc tự phát tán Spam hàng loạt từ máy cá nhân. |
| **587** | Message Submission | Dùng cho **MUA gửi mail lên MTA** (Client-to-Server). Bắt buộc phải xác thực (Authentication) và khuyến nghị dùng **STARTTLS**. | **Bảo mật tốt**. Đây là cổng tiêu chuẩn hiện hành cho người dùng cuối cấu hình ứng dụng gửi mail. Thư được mã hóa sau khi bắt tay clear-text ban đầu bằng lệnh STARTTLS. |
| **465** | SMTPS (Implicit TLS) | Ban đầu được đề xuất cho SMTP bảo mật, sau đó bị thu hồi nhưng vẫn được dùng rộng rãi cho kết nối **Client-to-Server**. | **Bảo mật tốt**. Khác với 587 (bắt đầu bằng clear-text rồi mới nâng cấp lên TLS), port 465 thiết lập kết nối SSL/TLS ngay từ đầu (Implicit TLS). |

---

### 3. SMTP Transaction & Response Codes

#### A. Các Lệnh SMTP Tiêu Chuẩn (SMTP Transaction)
Một phiên giao dịch SMTP chuẩn tuân theo một quy trình tuần tự các lệnh văn bản thuần túy:

1.  `HELO` / `EHLO`: Khởi tạo phiên làm việc. `EHLO` (Extended SMTP) được dùng phổ biến hiện nay để hỗ trợ các tính năng nâng cao như mã hóa, xác thực.
2.  `MAIL FROM`: Khai báo email của người gửi (Envelope Sender) và bắt đầu một giao dịch gửi thư mới.
3.  `RCPT TO`: Khai báo email của người nhận (Envelope Recipient). Lệnh này có thể lặp lại nhiều lần nếu gửi cho nhiều người.
4.  `DATA`: Bắt đầu truyền nội dung thư (bao gồm Header và Body). Phiên kết thúc nội dung khi Client gửi một dòng chỉ chứa duy nhất một dấu chấm (`.`).
5.  `QUIT`: Đóng kết nối SMTP.

##### Ví dụ thực tế về một phiên SMTP Transaction (Log truyền tải):
``` text
S: 220 mail.example.com ESMTP Postfix
C: EHLO mycomputer.local
S: 250-mail.example.com Hello mycomputer.local, pleased to meet you
S: 250-STARTTLS
S: 250 PIPELINING
C: MAIL FROM:<sender@company.com>
S: 250 2.1.0 <sender@company.com>... Sender ok
C: RCPT TO:<receiver@gmail.com>
S: 250 2.1.5 <receiver@gmail.com>... Recipient ok
C: DATA
S: 354 Enter mail, end with "." on a line by itself
C: From: Sender Name <sender@company.com>
C: To: Receiver Name <receiver@gmail.com>
C: Subject: Tieu de email thu nghiem
C:
C: Day la noi dung chinh cua email (Body).
C: .
S: 250 2.0.0 OK: Message accepted for delivery
C: QUIT
S: 221 2.0.0 mail.example.com closing connection
```
*(Trong đó `C:` đại diện cho Client, `S:` đại diện cho Server)*

#### B. Hệ thống Mã Phản Hồi (SMTP Response Codes)
Server sẽ phản hồi lại mỗi lệnh của Client bằng một mã số gồm 3 chữ số:
*   **2xx (Success)**: Lệnh thực hiện thành công (Ví dụ: `250 OK`).
*   **3xx (Intermediate)**: Server đã nhận lệnh nhưng cần thêm thông tin (Ví dụ: `354 Enter mail` sau lệnh DATA).
*   **4xx (Transient Negative / Temporary Error)**: Lỗi tạm thời, Client nên thử lại sau (Ví dụ: `421 Service unavailable`, `451 Server local error`).
*   **5xx (Permanent Negative / Hard Error)**: Lỗi vĩnh viễn, không được thử lại (Ví dụ: `550 User not found`, `554 Relay denied`).

---

### 4. Sự Khác Biệt Giữa Envelope và Header

Dựa trên tài liệu chuyên sâu về **"Envelope Sender vs Header Sender"**, một email thực chất có hai tập hợp thông tin người gửi/người nhận khác nhau:

| Tiêu chí | Mail Envelope (Phong bì thư) | Mail Header (Tiêu đề thư) |
| :--- | :--- | :--- |
| **Khái niệm** | Là thông tin định tuyến thực tế được trao đổi trực tiếp giữa hai server thông qua các lệnh SMTP. | Là một phần nội dung bên trong gói dữ liệu nằm sau lệnh `DATA`. Dành cho người dùng cuối nhìn thấy khi đọc thư. |
| **Lệnh đại diện** | `MAIL FROM` (Return-Path / Envelope Sender)<br>`RCPT TO` (Envelope Recipient) | `From: ...`<br>`To: ...` |
| **Tác dụng** | Server dùng để quyết định nơi chuyển tiếp thư hoặc nơi gửi thông báo lỗi (Bounce Mail) nếu gửi thất bại. | Ứng dụng Mail (MUA) dùng để hiển thị giao diện đẹp mắt cho người đọc xem ai gửi, ai nhận. |
| **Rủi ro bảo mật** | **Rất khó làm giả** vì Mail Server nhận sẽ đối chiếu IP gửi với bản ghi SPF dựa trên tên miền của Envelope Sender này. | **Rất dễ làm giả (Email Spoofing)**. Kẻ tấn công có thể ghi bất kỳ thứ gì ở mục `From:` trong Header để đánh lừa người dùng, dù lệnh `MAIL FROM` ở Envelope là một email rác khác. |

##### Ví dụ minh họa Email Phishing (Giả mạo):
*   **Thực tế truyền tải (Envelope)**:
    `MAIL FROM:<attacker@badspammer.com>` (Hệ thống kiểm tra SPF sẽ dựa vào domain `badspammer.com`).
*   **Nội dung hiển thị (Header)**:
    `From: Chăm sóc khách hàng <support@mybank.com>` (Người dùng nhìn thấy dòng này trong Outlook và lầm tưởng thư gửi từ ngân hàng thật).

---

### 5. SMTP Relay & Open Relays

#### A. SMTP Relay là gì?
SMTP Relay là dịch vụ hoặc cơ chế cho phép một máy chủ SMTP trung gian tiếp nhận email từ một nguồn và thay mặt nguồn đó gửi tiếp sang máy chủ đích. 
*   **Cấu hình đúng chuẩn**: Một SMTP Server chỉ được phép Relay (chuyển tiếp hộ) khi:
    1. Email đó xuất phát từ dải IP nội bộ được tin cậy.
    2. Người gửi đã đăng nhập tài khoản hợp lệ (SMTP Authentication).

#### B. Lỗ hổng Open Relay (Cực kỳ nguy hiểm)
*   **Khái niệm**: Open Relay là tình trạng một SMTP Server bị cấu hình sai, cho phép **bất kỳ ai trên Internet** gửi bất kỳ email nào qua nó đến một bên thứ ba bất kỳ mà không cần xác thực hay giới hạn quyền truy cập.
*   **Hậu quả**: Kẻ phát tán thư rác (Spammers) sẽ quét và lợi dụng các Open Relay Server này để gửi hàng triệu email rác/lừa đảo. Việc này khiến cho địa chỉ IP của doanh nghiệp sở hữu Server bị liệt vào Danh sách đen toàn cầu (Blacklist), làm nghẽn băng thông hệ thống và hủy hoại uy tín tên miền.

##### Ví dụ lỗ hổng Open Relay:
Một công ty cấu hình Postfix server nhưng bật tùy chọn `mynetworks = 0.0.0.0/0`. 
*   Một Hacker tại Nga gửi lệnh tới Server này: `MAIL FROM:<hacker@spam.com>`, `RCPT TO:<victim@gmail.com>`.
*   Server chấp nhận và tự động gửi thư tới Gmail hộ hacker. Gmail thấy IP của công ty gửi thư rác nên sẽ block vĩnh viễn IP của công ty.