import datetime
import hashlib

import requests_cache

from opengrokfs.opengrok import OpenGrok, File, Result

requests_cache.install_cache('test')


def test_get():
    og = OpenGrok('http://androidxref.com/7.1.1_r6/')
    page = og.get('/bionic/libc/stdlib/atexit.h')
    assert hashlib.md5(page.encode('utf-8')).hexdigest() == '3e38e9bad82e09ca41db364123009271'


def test_list():
    og = OpenGrok('http://androidxref.com/7.1.1_r6/')
    assert og.list('/bionic/libc/stdlib/') == [
        File(name='..', date=datetime.datetime(2016, 12, 20, 0, 0), size=4198, dir=True),
        File(name='atexit.c', date=datetime.datetime(2016, 12, 20, 0, 0), size=5734, dir=False),
        File(name='atexit.h', date=datetime.datetime(2016, 12, 20, 0, 0), size=1638, dir=False),
        File(name='exit.c', date=datetime.datetime(2016, 12, 20, 0, 0), size=2662, dir=False),
    ]


def test_list_long():
    og = OpenGrok('http://androidxref.com/7.1.1_r6/')
    assert len(og.list('external/kernel-headers/original/uapi/linux/')) == 473


def test_search_defs():
    og = OpenGrok('http://androidxref.com/7.1.1_r6/', projects=['bionic'])
    assert og.search({'defs': 'O_LARGEFILE'}) == [
        Result(path='/bionic/libc/kernel/uapi/asm-arm/asm/fcntl.h',
               line=25,
               text='#define O_LARGEFILE 0400000'),
        Result(path='/bionic/libc/kernel/uapi/asm-arm64/asm/fcntl.h',
               line=25,
               text='#define O_LARGEFILE 0400000'),
        Result(path='/bionic/libc/kernel/uapi/asm-mips/asm/fcntl.h',
               line=32,
               text='#define O_LARGEFILE 0x2000'),
        Result(path='/bionic/libc/kernel/uapi/asm-generic/fcntl.h',
               line=61,
               text='#ifndef O_LARGEFILE'),
        Result(path='/bionic/libc/kernel/uapi/asm-generic/fcntl.h',
               line=62,
               text='#define O_LARGEFILE 00100000'),
    ]


def test_search_path():
    og = OpenGrok('http://androidxref.com/7.1.1_r6/', projects=['bionic'])
    assert og.search({'path': '__reboot'}) == [
        Result(path='/bionic/libc/arch-arm/syscalls/__reboot.S'),
        Result(path='/bionic/libc/arch-arm64/syscalls/__reboot.S'),
        Result(path='/bionic/libc/arch-mips/syscalls/__reboot.S'),
        Result(path='/bionic/libc/arch-mips64/syscalls/__reboot.S'),
        Result(path='/bionic/libc/arch-x86/syscalls/__reboot.S'),
        Result(path='/bionic/libc/arch-x86_64/syscalls/__reboot.S'),
    ]
