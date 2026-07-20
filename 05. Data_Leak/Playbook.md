# PLAYBOOK ỨNG PHÓ SỰ CỐ: RÒ RỈ MÃ NGUỒN TRÊN GITHUB CÁ NHÂN
**Mã tài liệu:** IR-PB-04  
**Phiên bản:** v1.0  
**Mức độ mật:** Nội bộ (Internal)  
**Áp dụng:** Đội ngũ SecOps, Dev Lead, HR, Legal  

---

## 1. PHẦN I: XÁC ĐỊNH LỘ LỌT DỮ LIỆU (DETECTION & VERIFICATION)
Mục tiêu chính của giai đoạn này là phát hiện sớm, xác minh tính chính xác của thông tin và nhanh chóng thu thập, niêm phong bằng chứng số trước khi đối tượng có hành động ẩn giấu hoặc xóa dấu vết.

### 1.1. Kênh phát hiện và Tiếp nhận nguồn tin
Sự cố rò rỉ mã nguồn trên GitHub cá nhân thường được ghi nhận qua các kênh:
*   **Hệ thống Giám sát Chủ động (Brand Monitoring / Threat Intelligence):** Cảnh báo tự động từ các công cụ quét mã nguồn công khai (như GitGuardian, Gitleaks, GitHub API monitoring) dựa trên từ khóa độc quyền, tên miền doanh nghiệp hoặc chữ ký mã nguồn đặc trưng.
*   **Báo cáo nội bộ:** Nhân viên hiện tại phát hiện thông qua tìm kiếm ngẫu nhiên hoặc thuật toán gợi ý của GitHub.
*   **Cảnh báo từ cộng đồng:** Đối tác, khách hàng hoặc các chuyên gia bảo mật độc lập (Bug Bounty) gửi email cảnh báo bảo mật.

### 1.2. Quy trình Xác minh Tính chính xác (Triage)
Khi nhận được cảnh báo, Đội ngũ SecOps phối hợp với Dev Lead thực hiện xác minh trong vòng **15–30 phút**:
1.  **Kiểm tra tính tồn tại:** Truy cập URL được báo cáo để xác nhận repository (repo) đó đang ở chế độ công khai (Public).
2.  **Xác minh quyền sở hữu:** Đối chiếu username/avatar/email của tài khoản GitHub đó với cơ sở dữ liệu nhân sự cũ để định danh chính xác cựu nhân viên.
3.  **Xác minh bản quyền mã nguồn:** Đối chiếu các cấu trúc thư mục, tên class, hàm đặc trưng hoặc các đoạn comment để khẳng định đây là mã nguồn độc quyền của doanh nghiệp, không phải mã nguồn mở hoặc project cá nhân tự viết.

### 1.3. Thu thập và Bảo tồn Chứng cứ Số (Digital Forensics)
*Tuyệt đối KHÔNG tương tác công khai (không comment, không tạo Issue, không ấn Star/Fork) trên repo của đối tượng nhằm tránh bộc lộ việc doanh nghiệp đang điều tra.*

Thực hiện lưu trữ bằng chứng số theo trình tự pháp lý:
*   **Bằng chứng hình ảnh:** Chụp ảnh màn hình toàn bộ giao diện repo bao gồm: URL rõ ràng, Tên tài khoản, Commit History (nhật ký commit thể hiện email và thời gian), danh sách file và số lượng Star/Fork hiện tại.
*   **Bằng chứng mã nguồn (Offline Clone):** Sử dụng một tài khoản ẩn danh (không liên quan đến công ty) thực hiện lệnh sao chép cục bộ toàn bộ repo đó về máy chủ phân tích của SecOps:
    ```bash
    git clone --mirror <URL_REPO_CÁ_NHÂN_NHÂN_VIÊN_CŨ>
    ```
    *Lưu ý: Thao tác `--mirror` giúp thu thập trọn vẹn toàn bộ các nhánh (branches) và lịch sử commit (commit history) cũ của repo.*
*   **Băm kiểm tra (Hashing):** Tạo mã hash (SHA-256) cho tệp tin nén chứa repo vừa tải về để đảm bảo tính toàn vẹn của bằng chứng trước pháp lý.

---

## 2. PHẦN II: PHÂN TÍCH DỮ LIỆU (DATA ANALYSIS & IMPACT ASSESSMENT)
Sau khi đã có bản sao mã nguồn, Đội ngũ SecOps phối hợp với Kiến trúc sư phần mềm (Software Architect) và Dev Lead tiến hành mổ xẻ, phân tích chuyên sâu nhằm bóc tách các thành phần nhạy cảm bị lộ.

### 2.1. Phân tích Thành phần Mã nguồn và Dữ liệu Nhạy cảm (Secret Scanning)
Sử dụng các công cụ chuyên dụng tự động (như *Gitleaks, Trufflehog*) quét toàn bộ mã nguồn vừa tải về, bao gồm cả các commit cũ trong quá khứ để tìm kiếm:
*   **Thông tin xác thực hệ thống (Credentials):** Mật khẩu quản trị, tài khoản kết nối Database (SQL Server, PostgreSQL, MySQL...).
*   **Khóa cấu hình đám mây (Cloud Infrastructure Keys):** AWS Access/Secret Key, Azure Client Secrets, Google Cloud Service Account Credentials.
*   **Khóa kết nối dịch vụ bên thứ ba (Third-party API Keys):** SendGrid API Key, Stripe Tokens, Firebase Keys, Telegram Bot Tokens, SMS Gateway Credentials.
*   **Dữ liệu nhạy cảm của doanh nghiệp & khách hàng (PII/Business Data):** 
    *   Các tệp tin cấu hình (`.env`, `appsettings.json`, `web.config`, `config.yaml`) bị commit nhầm lên code.
    *   Dữ liệu hardcode trong mã nguồn: Danh sách tài khoản thử nghiệm, thông tin định danh khách hàng (PII), thông tin thẻ cấu hình cứng.
    *   Các thuật toán cốt lõi (Core Business Logic), công thức tính toán tài chính, hoặc tài sản trí tuệ độc quyền của doanh nghiệp.

### 2.2. Đánh giá Mức độ lan truyền và Phân tích Lịch sử
*   **Lịch sử tồn tại (Exposure Window):** Dựa vào Git History, xác định repo này đã được chuyển sang chế độ Public từ bao lâu (vài ngày, vài tháng hay vài năm?). Điều này giúp ước lượng khoảng thời gian hacker có thể đã quét được thông tin.
*   **Kiểm tra Fork và Clone:** Xác định xem repo này đã có lượt **Fork** nào chưa. Nếu đã có Fork, ghi lại danh sách các tài khoản GitHub đã Fork để chuẩn bị cho quy trình gỡ bỏ diện rộng.
*   **Định vị vị trí mã nguồn trong hệ thống:** Xác định đoạn mã nguồn bị lộ thuộc về môi trường nào (Production - Môi trường thật, Staging - Môi trường thử nghiệm, hay Development/Lab). Mã nguồn thuộc môi trường Production sẽ đẩy mức độ nghiêm trọng lên cao nhất.

---

## 3. PHẦN III: BÁO CÁO ẢNH HƯỞNG (IMPACT REPORTING)
Dựa trên kết quả phân tích ở Phần II, Đội ngũ Ứng phó sự cố tiến hành lập Báo cáo ảnh hưởng (Impact Report) để trình Ban Giám đốc và làm căn cứ cho Ban Pháp chế xử lý.

### 3.1. Phân loại Mức độ Nghiêm trọng của Sự cố
Sự cố được phân loại dựa trên ma trận rủi ro sau:

| Mức độ | Tiêu chí xác định | Hành động yêu cầu |
| :--- | :--- | :--- |
| **CRITICAL (Nguy cấp)** | Lộ mã nguồn cốt lõi (Core), chứa API Key quyền Root Đám mây (AWS/Azure) hoặc Connection String của Database Production chứa dữ liệu khách hàng. | Kích hoạt tình trạng khẩn cấp toàn công ty. Thu hồi credentials trong < 1 giờ. |
| **HIGH (Nghiêm trọng)** | Lộ mã nguồn sản phẩm thương mại nhưng không chứa thông tin xác thực Production (chỉ chứa key môi trường Dev/Staging), hoặc lộ thuật toán quan trọng. | Xử lý gỡ bỏ và đổi key liên quan trong < 4 giờ. |
| **MEDIUM (Trung bình)** | Lộ mã nguồn dự án nội bộ, dự án phụ (Side project) hoặc bài tập thử việc không ảnh hưởng trực tiếp đến vận hành của hệ thống cốt lõi. | Xử lý gỡ bỏ trong vòng 12-24 giờ. |

### 3.2. Đánh giá Các Chiều Hướng Ảnh Hưởng (Impact Dimensions)
Báo cáo ảnh hưởng phải làm rõ 4 khía cạnh tổn thất:

1.  **Ảnh hưởng Kỹ thuật & Bảo mật (Technical Impact):**
    *   *Nguy cơ Tấn công mạng:* Kẻ tấn công có thể sử dụng các API Key bị lộ để chiếm quyền điều khiển hạ tầng cloud, mã hóa dữ liệu tống tiền (Ransomware), hoặc xâm nhập sâu vào hệ thống nội bộ (Lateral Movement).
    *   *Nguy cơ từ Thiết kế ngược (Reverse Engineering):* Việc lộ cấu trúc mã nguồn giúp tin tặc dễ dàng tìm ra các lỗ hổng logic (Business Logic Vulnerabilities), lỗ hổng Zero-day trong ứng dụng để khai thác.
2.  **Ảnh hưởng về Tài sản trí tuệ & Cạnh tranh (Intellectual Property Impact):**
    *   Mất lợi thế cạnh tranh nếu đối thủ thương mại tiếp cận được các thuật toán cốt lõi, kiến trúc hệ thống hoặc các tính năng độc quyền đang trong giai đoạn phát triển mật.
3.  **Ảnh hưởng Tuân thủ & Pháp lý (Legal & Compliance Impact):**
    *   Vi phạm nghiêm trọng luật an toàn thông tin hoặc các tiêu chuẩn bảo mật mà doanh nghiệp cam kết tuân thủ (ví dụ: ISO 27001, PCI-DSS - nếu lộ mã nguồn thanh toán).
    *   Rủi ro bị khách hàng kiện quyền lợi nếu dữ liệu liên quan đến dự án của họ bị công khai mà không có sự đồng ý.
4.  **Ảnh hưởng Uy tín & Thương hiệu (Reputational Impact):**
    *   Giảm uy tín của doanh nghiệp trong mắt khách hàng và đối tác khi năng lực quản trị an toàn thông tin nội bộ bị đặt dấu hỏi. Ảnh hưởng tiêu cực đến giá trị thương hiệu hoặc giá cổ phiếu (nếu có).

### 3.3. Biểu mẫu Khảo sát/Tóm tắt Ảnh hưởng (Dành cho Báo cáo nhanh)
```text
SỰ CỐ AN NINH THÔNG TIN: RÒ RỈ MÃ NGUỒN TRÊN GITHUB CÁ NHÂN
----------------------------------------------------------------------
1. THÔNG TIN CHUNG:
- Thời gian phát hiện: [Ngày/Giờ]
- Tài khoản vi phạm: GitHub.com/[Username_Cựu_Nhân_Viên]
- URL Repository: https://github.com/...
- Trạng thái Repo: [Public / Đã Fork X lượt]

2. PHẠM VI DỮ LIỆU BỊ LỘ:
- Tên dự án/Mã nguồn: [Ví dụ: Hệ thống Core Banking V2 - Module Thanh Toán]
- Môi trường ảnh hưởng: [Production / Staging / Dev]
- Danh sách Secrets phát hiện: [Ví dụ: 01 AWS Root Access Key, 02 Database Strings]

3. ĐÁNH GIÁ RỦI RO & ẢNH HƯỞNG:
- Mức độ nghiêm trọng: [CRITICAL / HIGH / MEDIUM]
- Hệ thống có nguy cơ bị xâm nhập trực tiếp: [Có / Không] (Nêu rõ hệ thống nào)
- Thiệt hại tài sản trí tuệ ước tính: [Thấp / Trung bình / Cao]

4. ĐỀ XUẤT HÀNH ĐỘNG KHẨN CẤP:
- [ ] Khóa và thu hồi ngay lập tức danh sách API Keys/Mật khẩu nêu trên.
- [ ] HR/Legal liên hệ trực tiếp nhân sự yêu cầu gỡ bỏ repo trong vòng 2 giờ.
- [ ] Chuẩn bị hồ sơ DMCA gửi GitHub hỗ trợ nếu đối tượng không hợp tác.
----------------------------------------------------------------------
```
