# Attack Surface

Bề mặt tấn công (Attack Surface) là tổng hợp tất cả các điểm (hay còn gọi là các vector tấn công) mà một ng dùng không được phép có thể sử dụng để truy cập vào hệ thống và lấy cắp dữ liệu. Hiểu một cách đơn giản, bề mặt tấn công càng lớn thì hệ thống càng khó bảo vệ.

## Phân loại Bề mặt tấn công

Bề mặt tấn công được chia thành hai danh mục chính:

- Bề mặt tấn công kỹ thuật số (Digital Attack Surface): Bao gồm tất cả phần cứng và phần mềm kết nối với mạng tổ chức. Các thành phần bao gồm ứng dụng, mã nguồn, các cổng (ports), máy chủ, trang web và cả Shadow IT (các thiết bị hoặc ứng dụng chưa được phê duyệt mà người dùng tự ý sử dụng).
- Bề mặt tấn công vật lý (Physical Attack Surface): Bao gồm tất cả các thiết bị đầu cuối mà kẻ tán công có thể tiếp cận trực tiếp như máy tính để bàn, ổ cứng, máy tính xách tay, điện thoại di động và ổ USB.

## Các Vector tấn công phổ biến

Vector tấn công phổ biến là phương thức mà tội phạm mạng sử dụng để xâm nhập. Bề mặt tấn công càng mở rộng thì rủi ro từ các vector này càng tăng:
- Phishing (tấn công giả mạo): Gửi các thông điệp giả mạo nguồn tin đáng tin cậy để lừa người dùng cung cấp thông tin hoặc nhấp vào liên kết độc hại
- Malware (mã độc): bao gồm ransomware, trojan và virus giúp tin tặc chiếm quyền điều khiển thiết bị hoặc gây hư hại dữ liệu.
- Mật khẩu bị thỏa hiệp: Do người dùng sử dụng mật khẩu yếu hoặc dùng lại mật khẩu cũ
- Phần mềm chưa được vá lỗi (Unpatched software): Tin tặc tích cực tìm kiếm các lỗ hổng chưa được vá trong hệ điều hành và ứng dụng để làm "cửa ngõ" xâm nhập.
- Vấn đề mã hóa: Sử dụng các giao thức mã hóa dẫn đến dữ liệu bị lộ dưới dạng văn bản thuần túy (plaintext) khi bị đánh chặn.

## Threat Actor 

Tác nhân đe dọa (Threat Actor), còn được gọi là tác nhân gây hại, là những cá nhân hoặc nhóm ngưòi có hành vi cố ý gây hại cho các thiết bị hoặc hệ thống kỹ thuật số. Họ loịw dụng các lỗ hổng trong hệ thống máy tính, mạng và phầm mềm để thực hiện các cuộc tấn công mạng nhằm đạt được những mục tiêu cụ thể.

### Các loại tác nhân đe dọa phổ biến

- Tội phạm mạng (Cybercriminals): Đây là nhóm phổ biến nhất, hoạt động chủ yếu vì lợi nhuận tài chính. 
- Tác nhân quốc gia (Nation-state actors): Được các chính phủ tài trợ để thực hiện hành động gián điệp, đánh cắp bí mật quốc gia hoặc phá hoại cơ sở hạ tầng trọng yếu của đối phương.
- Tin tặc vì mục tiêu chính trị (Hacktivists): Những người này sử dụng kỹ thuật tấn công mạng để thúc đẩy các chương trình nghị sự chính trị hoặc xã hội
- Người tìm kiếm sự phấn khích (Thrill seekers): Họ tấn công hệ thống chủ yếu để giải trí, thách thức bản thân hoặc thể hiện kỹ năng.
- Mối đe dọa nội bộ (Insider Threat): NHững người bên trong tổ chức (nhân viên, đối tác) có quyền truy cập hệ thống.
- Khủng bố mạng (Cyberterorists): Thực hiện các cuộc tấn công vì mục tiêu ý thức hệ hoặc tôn giáo nhằm gaya ra sự sợ hãi hoặc bạo lực.

> Note: Hacker là người có kỹ năng kỹ thuật để xâm nhập hệ thống. Một "ethical hacker" có thể dùng kỹ năng để giúp tổ chức vá lỗ hổng. Threat Acor là thuật ngữ rộng hơn, bao gồm bất kỳ ai gây ra mối đe dọa, ngay cả khi họ không có kỹ năng kỹ thuật cao, vdu như một nhân viên vô tình làm mất USB chứa dữ liệu quan trọng.


## Campain

Champain (chiến dịch) được định nghĩa là một nhóm có hoạt động xâm nhập được thực hiện trong một khoảng thời gian cụ thể với mục tiêu và đối tượng tấn công chung.

## Quy trình quản lý Bề mặt tấn công

Việc quản lý giúp tổ chức có cái nhìn tổng thể và chủ dộng phòng thủ:

- Định nghĩa và mapping: Xác định các điểm yếu, đánh giá lỗ hổng và xác định vai trò, quyền hạn của người dùng.
- Mô hình hóa mối đe dọa (Threat Modeling): Đánh giá một cách hệ thổng các đờng dẫn tấn công và ưu tiên rủi ro trên kiến trúc hệ thống.
- Phân loại vị trí lưu trữ dữ liệu: Chia dữ liệu thành các khu vực như đám mây (cloud), thiết bị đàu cuối và hệ thống tại chỗ (on-premises).

## 5 bước giảm thiểu Bề mặt tấn công

Để hạn chế cơ hội của tội phạm mạng, tổ chức cần thực hiện:

1. Triển khai chính sách Zero-Trust: Chỉ cấp quyền truy cập đúng mức cho đúng người vào đúng thời điểm.
2. Loại bỏ sự phức tạp: Vô hiệu hóa các thiết bị và phần mềm không sử dụng để đơn giản hóa mạng lưới.
3. Quét lỗ hổng định kì: Phải có khả năng hiển htij đày đủ bề mặt tấn công đẻ phát hiện sớm các vấn đề trên cả đám mây và mạng nội bộ.
4. Phân đoạn mạng (Network Segmentation): Sử dụng tường lửa và vi phân đoạn (microsegmentation) đẻ tạo ra các rào cản ngăn chặn kẻ tấn công di chuyển ngang trong hệ thống.
5. Đào tạo nhân viên: Nâng cao nhận thức để họ nhận biết được các dấu hiệu của tấn công giả mạo và kỹ thuật xã hội (social engineering).

<!-- TODO: Add thêm hình ảnh cho nó đẹp hơn và recommend -->
