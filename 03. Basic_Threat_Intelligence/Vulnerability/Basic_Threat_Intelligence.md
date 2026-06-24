# Threat Intelligence

Tri thức về mối đe dọa mạng (Cyber Threat Intelligence - CTI) là việc thu thập, xử lý và phân tích để hiểu rõ về động cơ, mục tiêu và phương thức tấn công của các tác nhân gây hại. Thay vì chỉ phỏng thủ thụ động, CTI giúp các tổ chức cung cấp các thông tin dựa trên bằng chứng về mối đe dọa hiện hữu hoặc mới nổi.

## Vòng đời của Threat Intelligence (Lifecycle)

CTI không phải là  một tập dữ liệu tĩnh mà là một quy trình liên tục gồm 6 bước để biến dữ liệu thô thành tri thức có thể hành động được:

![](../assets/CTI-lifecycle.png)

- Yêu cầu (Requirements/Planning): Xác định mục tiêu và phương pháp luận phù hợp với nhu cầu của các bên liên quan, chẳng hạn như hiểu động cơ cảu kẻ tấn công hoặc xác định bề mặt tấn công
- Thu thập (Collection): Ghi lại thông tin từ các nguồn như nhật ký lưu lượng mạng (logs), dữ liệu công khai, diễn đàn, mạng xã hội và các chuyên gia.
- Xử lý (Processing): Làm sạch và tổ chực lại dữ liệu thô (giải mã tệp, dịch thuật, định dạng lại) để sẵn sàng cho việc phân tích.
- Phân tích (Analysis): Đánh giá dữ liệu đã xử lý để đưa ra các nhận định và khuyến nghị thực tế.
- Phổ biến (Dissemination): Trình bày kết quá dưới dạng báo cáo hoặc tài liệu phù hợp với từng đối tượng (lãnh đạo hoặc kỹ thuật).
- Phản hồi (Feedback): thu thập ý kiến từ các bên liên quan để điều chỉnh và cải thiện quy trình cho các chu kì tiếp theo.

## Ba loại hình Threat Intelligence chính

Tùy vào độ phức tạp và mục tiêu sử dụng, CTI được chia làm 3 cấp độ:

![](../assets/types-of-TI.png)

- Tatical (Chiến thuật): tập trung vào các chi tiết kỹ thuật ngắn hạn. Nó chủ yếu xử lý các **Chỉ số thỏa hiệp** (Indicators of Compromise - IOCs) như địa chỉ IP đọc hại, URLs, mã băm tệp (hashes) và tên miền. Loại này thường được tự động hóa và tích hợp trức tiếp và các công cụ bảo mật như tường lửa.
- Operational (Vận hành): Đi sâu vào các câu hỏi *"ai", "tại sao" và "như thế nào"*. Nó tập trung vào TTPs (Tactics, Technique, and Procedures) - các chiến thuật và kỹ thuạt mà kẻ tấn công sử dụng. Loại này đòi hỏi sự phân tích của ocn người và có giá trị lâu dài hơn vì kẻ tấn công khó có thể thay đổi phương thức hoạt động nhanh chỏng như thay đổi công cụ.
- Strategic (Chiến lược): Cung cấp cái nhìn cáp cao về mối liên hệ giữa các mối đe dọa mạng với các sự kiện toàn cầu, đại chính trị và rủi ro tổ chức. Đây là thông tin quan trọng để ban lãnh đạo  (CISOs, CIOs) đưa ra các quyết định đầu tư và chiến lược bảo mật dài hạn.

## Lợi ích đối với các vai trò trong tổ chức

CTI mạng lại giá trị thực té cho nhiều bộ phận khác nhau:

- Nhân viên phân tích IT/Security: Giúp chặn các IPs, tên miền độc hại hiệu quả hơn thông qua các nguồn cấp dữ liệu (feeds).
- Trung tâm vận hành bảo mật (SOC): Giúp ưu tiên các sự cố dựa trên mức độ rủi ro và tác động thực tế.
- Nhóm ứng phó sự cố (CSIRT): Đẩy nhanh quá tình điều tra bằng cách cung cấp ngữ cảnh về kẻ tấn công và phân tích nguyên nhân gốc rễ.
- Ban lãnh đạo: Đưa ra các quyết định đàu tư thông minh hơn dựa trên bức tranh tổng thể về rủi ro mạng.