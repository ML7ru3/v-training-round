# Impersonation

Impersonation attack là một mối đe dọa trong đó kẻ tấn công mạo danh các cá nhân hoặc tổ chức đáng tin cậy - chẳng hạn như sếp, ngân hàng hoặc một dịch vụ quen thuộc - để lừa nạn nhân cung cấp thông tin nhạy cảm, chuyển tiền hoặc cấp quyền truy cập hệ thống.

## Sự khác biệt giừa Impersonation và Phishing.


| Đặc điểm | Impersonation (Giả mạo danh tính) | Phishing (Lừa đảo) |
| :--- | :--- | :--- |
| **Định nghĩa** | Bắt chước một người/thực thể cụ thể (như CEO, nhà cung cấp) để đánh lừa người nhận. | Kẻ tấn công giả danh công ty/cá nhân để đánh cắp thông tin qua các thông điệp lừa đảo. |
| **Kỹ thuật chính** | Sử dụng **mẹo hiển thị tên** (display name trickery) hoặc các tên miền gần giống (ví dụ: `ceo@companyy.com`). | Thường sử dụng **spoofing** (giả mạo tiêu đề email) để hiển thị chính xác địa chỉ nguồn nhằm vượt qua bộ lọc. |
| **Mục tiêu chính** | Lừa nạn nhân tự nguyện giao nộp dữ liệu, tiền bạc hoặc thông tin xác thực thông qua thao túng tâm lý. | Lừa nạn nhân thực hiện hành động như **nhấp vào liên kết độc hại** hoặc tải xuống tệp chứa mã độc. |
| **Sử dụng mã độc** | Thường **không cần mã độc**; nó tấn công vào tâm lý con người. | Thường là phương thức để **phát tán phần mềm độc hại** (ransomware, virus) vào hệ thống. |
| **Độ khó phát hiện** | **Khó phát hiện hơn** vì dựa trên bối cảnh xác thực và sự thao túng tâm lý tinh vi. | Có thể phát hiện qua các giao thức kỹ thuật như **SPF, DKIM, DMARC** nếu kẻ tấn công giả mạo tiêu đề email. |

**Tóm lại:** Nếu **Phishing** là một "mẻ lưới" rộng thường kèm theo các liên kết hoặc tệp độc hại để xâm nhập kỹ thuật, thì **Impersonation** là một cuộc tấn công "nhắm mục tiêu" tập trung vào việc tạo ra một danh tính giả thuyết phục để trực tiếp lừa gạt nạn nhân mà không nhất thiết phải sử dụng mã nguồn độc hại.