# CVE Analysis

Chọn một CVE bất kì để phân tích hành vi và làm PoC cho nó.

Ví dụ: CVE-2025-24813, CVE-2025-46604, CVE-2025-2481, CVE-2024-45216,..

## Yêu cầu

- Dựng lại môi trường cho lỗ hổng.
- Viết mã khai thác.
- Viết rule phát hiện khai thác.
- Dấu hiệu nhận biết khai thác.
- Cách khắc phục lỗ hổng.
- Viết báo cáo tổng hợp chi tiết.


## Những CVE mà có thể dùng được sau này

- **CVE-2026-9848**: The **WP Ticket plugin** for WordPress is vulnerable to **SQL Injection** via the WordPress search query parameters (`s`) in versions up to, and including, 6.0.4, CNA: Wordfence. (khá là dễ bởi vì nó chỉ đơn thuần là SQL Injection...)
- **CVE-2026-45416**: **Netty** is a network application framework for developement of protocol servser and clients. When a 16 MiB request exceeds the default pooled chunk size and becomes a huge/unpooled allocation performed immediately. The buffer is retained in the handler until the channel closes. Prior to versions 4.1.135.Final and 4.2.12.Final.
- **CVE-2026-45156**: **Nexcloud** is an open source content collaboration platform. From version 0.3.0 to before 3.1.0, 5.0.0, a **missing signature verification** in User OIDC allowed a malicious ID4me authority to identify as any user.
- **CVE-2024-9902**: A flaw was found in **Ansible**. The ansible-core `user` module ccan allow an unpriviledged user to silently create or repalce the contents of any file on any system path and take ownership of it when a priviledged usedr excutes the `user` modeul against the unpriviledged user's home directory. If the unpriviledged user has traversal permissions on the directory containing the exploited target file, tehy retain full control over the content of the file as its owner.
- **CVE-2023-46604**: The **Java OpenWire protocol marshaller** (or Apache ActiveMQ's OpenWire protocol) is vulnerable to **Remote Code Execution**. This vulnerability may allow a remote attack with network access to either a Java-based OpenWire broker or client to run arbitraery shell commands by manipulating serialized class types in the OpenWire protocol to cause either the client or the broker to instanntiate any class on the claspath. **Version**: before **5.15.16**. (nếu mà mấy cái trên không được thì sẽ chọn cái này)