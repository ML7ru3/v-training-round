# Tầng giao vận (Transport Layer)

Tầng giao vận (Transport Layer), là tầng thứ 4 trong mô hình OSI, đóng vai trò cung cấp dịch vụ giao tiếp logic giữa các tiến trình ứng dụng chạy trên máy chủ khác nhau. Khác vơi staanfg mạng cung cấp giao tiếp giữa các máy chủ (host-to-host), tầng giao vận mở rộng dịch vụ này thành giao tiếp giữa các tiến trình (process-to-process).

## Các chức năng cốt lõi

- Đa hợp và Giải đa hợp (Multiplexing/Demultiplexing): Đây là chức năng cơ bản nhất, sử dụng các số cổng  (port numbers) để thu nhập dữ liệu từ nhiều tiến trình khác nhau tại bên gửi và phân phối chính xcas đến các socket tương ứng tại bên nhận.

- Truyền dữ liệu tin cậy (Reliable Data Transfer): Đảm bảo dữ liệu được chuyển giao mà không bị lỗi bit, không bị mất gói tin và đúng thứ tự thông qua các cơ chế như mã kiểm tra lỗi (checksum), số thứ tự (sequence numbers), và truyền lại (retransmission).

- Điều khiển luồng  (Flow Control): Cơ chế giúp bên gửi điều chỉnh tốc độ truyền dữ liueej sao cho phù hợp với khả năng xử lý cảu bên nhận, tránh làm tràn bộ đệm của bên nhận.

- Điều khiển tắc nghẽn (Congestion Control): Ngăn chặn việc các máy chủ gửi quá nhiều dữ liệu vào mạng lưới, làm quá tải các bộ định tuyến và liên kết trung gian.

## Hai giao thức Internet chính

Internet cung cấp hai giao thức tầng giao vận chính cho lớp ứng dụng

- TCP (Transmission Control Protocol): là giao thức hướng kết nối, cung cấp dịch vụ truyền dữ liệu tin cậy, đảm bảo dữ liệu đúng thứ tự và đẩy đủ. TCP sử dụng cơ chế "bắt tay 3 bước" (3-way handshake) để thiết lập kết nối trước khi truyền dữ liệu thực tế.

- UDP (User Datagram Protocol): Là giao thức không kết nối, cung cấp dịch vụ "nỗ lực tối đa" nhưng không tin cậy. UDP không có các cơ chế kiểm soát phức tạp như TCP nên có độ trễ thấp h ơn, phù hợp cho các ứng dụng thời gian thực như truyền phát video hoặc DNS.

## Vị trí triển khai và đóng gói

## Các cơ chế truyền lỗi phổ biến



