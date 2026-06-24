# CVE

## Vòng đời của CVE (CVE life cycles)

CVE (Commnon Vulnerabilities and Exposures) là mã đinh danh duy nahts cho một lỗ hổng bảo mật đã được xác định. Quy trình từ khi phát hiện đến khi quản lý lỗ hổng diễn ra qua các giai đoạn sau:

- Phát hiện và Định danh: Các nhà nghiên cứu, nhà cugn cấp hoặc thợ săn tiền thưởng lỗ hổng phát hiện ra một bug, Nếu bug đó có thể bị lợi dụng để xâm nhập hệ thống, nó được tổ chức MITRE đăng ký và cấp mã CVE ID.

![](../assets/cve-life-cycles.png)

- Vòng đời quản lý lỗ hỏng (Vulnerability Management Lifecycle): Đây là một quy trình vận hành liên tục gồm 6 pha chính:

    1. Phát hiện tài sản (Asset Discovery): Lập danh mục tất cả phần cứng và phần mềm trong mạng để biết cái gì cần để bảo vệ.
    2. Đánh giá lỗ hổng (Vulnerability Assessment): Sử dụng các công cụ quét để so sánh môi trường hiện tại với cơ sở dữ liệu lỗ hổng đã biết.
    3. Đánh giá rủi ro và Ưu tiên (Prioritization): Sử dụng điểm CVSS kết hợp với cá ngữ cảnh thực tế (như dữ liệu nhạy cảm, quyền truy cập) để xác định lỗ hổng nào cần xử lý trước.
    4. Xử lý và Phản ứng (Remediation): Thực hiện vá lỗi (patching), thay thế tài ngueyen hoặc cấu hình lại hệ thống để loại bỏ lỗ hổng.
    5. Xác minh (Verification): Quét alilj để dảm bảo việc vá lỗi thanfhcoong vafk hông gây ra lỗi hệ thống khác.
    6. Báo cáo và Cải tiến: Tổng hợp dữ liệu để đưa ra các quyết định đầu từ bảo mật chiến lược.

##  Vector CVSS v3.1 (Common Vulnerability Scoring System)

![](../assets/cvss.png)


CVSS là hệ thống tiêu chuẩn để đánh gái mực độ nghiêm trọng của lỗ hổng trên thang điểm từ 0 -> 10. Một vector String trong CVSS v3.1 là một chuỗi ký tự đại diện cho các giá trị đo lường cụ thể.

- Exploitability (Khả năng khai thác) bao gồm:
    - Attack Vector (AV) 
    - Attack Complexity (AX) (độ khó của cuộc tấn công)
    - Privileges Required (PR) (quyền hạn cần thiết)
    - User Interaction (UI) (có cần người dùng tương tác gì không?)
    - Scope (S) (Khả nwang ảnh hưởng sang các thành phần khác)
- Impact (Tác động): Đánh giá ảnh hưởng đến tính bảo CIA (bảo mật, toàn vẹn, sẵn sàng).
- Nhóm chỉ số thời gian (Temporal Scỏe Metrics): Phản anh trạng thái hiện tại của lỗ hổng, bao gồm:
    - Exploit Code Maturity (E): mức độ sẵn có của mã khai thác.
    - Remediation Level (RL): tính trạng có bản vá hay chưa.
    - Report Confidence (RC): mực độ tin cậy của báo cáo lỗi.

## Cơ sở dữ liệu NVD (National Vulnerability Database)

NVD là kho lưu trữ dữ liệu quản lý lỗ hổng dựa trên các tiêu chuẩn của chính phủ Hoa Kỳ.

- Vai trò: NVD đồng bộ hóa dữ liệu với danh sách CVE của MITRE và thực hiện phân tích chuyên sâu.
- Chức năng: NVD cung cacsd các phân tích kỹ thuật, gán điểm CVSS cho các mã CVE, liên kết với các danh mục của phẩn (CPE) và cung cấp các công cụ tìm kiếm, thống kê lỗ hổng theo thời gian thực.

![](../assets/nvd-example.png)

=> Đây là nguồn tài liệu tham khảo chính cho các giải pháp quản lý lỗ hổng trên toàn thế giới

## KEV (Known Exploited Vulnerabilities)

KEV là danh mục lỗ hổng **đã biết bị khai thác trong thực tế**, do Cơ quan An ninh Cơ sở hạ tầng và An ninh mạng hoa Kỳ (CISA) quản lý.

- Sự khác biệt cốt lõi: Trong khi CVE chỉ cho biết "lỗ hổng tồn tại" và CVSS ước tính "tác động lý thuyết", thì KEV khẳng định lỗ hổng đó đang bị tin tặc sử dụng tích cực trong các chiến dịch tấn công thực tế (như ransomware, đánh cắp dữ liệu).
- Vai trò trong ưu tiên: Trong quản lý rủi ro hiện đại, trạng thai KEV quan trọng hơn điểm số CVSS khi quyết định lỗ hổng nào cần vá trước. Nếu một lỗ hổng nằm trong KEV, nó đòi hòi cần phải được vá khẩn cấp (trong vài giờ hoặc vài ngày) thay vì theo chu kỳ hàng tháng thông thường.
- Ứng dụng: Các tổ chức sử dụng KEV để lọc ra nhóm nhỏ các lỗ hổng thực sự nguy hiểm trong hàng ngàn mã CVE được công bố mỗi năm, giúp tôi ưu hóa nguồn lực phòng thủ.

![](../assets/kev-example.png)