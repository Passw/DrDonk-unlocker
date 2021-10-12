#!/usr/bin/env python3

import mmap
import os
import re
import sys

if sys.version_info < (3, 8):
    sys.stderr.write('You need Python 3.8 or later\n')
    sys.exit(1)


def set_bit(value, bit):
    return value | (1 << bit)


def clear_bit(value, bit):
    return value & ~(1 << bit)


def test_bit(value, bit):
    return value & bit


def patchentry(libbase, pattern):
    # Loop through each entry and set top bit
    # 0xBE --> 0xBF (WKS 12/13)
    # 0x3E --> 0x3F (WKS 14+)
    offset = 0
    while True:
        offset = libbase.find(pattern, offset)
        if offset != -1:
            print(f'GOS Entry Patched flag @: 0x{offset:0x8}')
            libbase.seek(offset + 32)
            flag = ord(libbase.read(1))
            flag = set_bit(flag, 0)
            libbase.seek(offset + 32)
            libbase.write(bytes([flag]))
            offset += 1
        else:
            break

    return


def patchbase(name):
    # Patch file
    print('GOS Table Patching: ' + name)
    f = open(name, 'r+b')

    # Memory map file
    libbase = mmap.mmap(f.fileno(), 0)

    # Entry to search for in GOS table
    # Should work for Workstation 12-15...
    pattern1 = b'\x10\x00\x00\x00[\x10|\x20]\x00\x00\x00\x012]\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    pattern2 = b'\x10\x00\x00\x00[\x10|\x20]\x00\x00\x00[\x01|\x02]\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

    print('GOS Table Patched: ' + name)

    # Tidy up
    libbase.flush()
    libbase.close()
    f.flush()
    f.close()

    return


def main():
    print('patchgos')
    print('--------')

    if len(sys.argv) >= 2:
        filename = sys.argv[1]
    else:
        print('Please pass file name!')
        return

    if os.path.isfile(filename):
        patchbase(filename)
    else:
        print('Cannot find file ' + filename)
    return


if __name__ == '__main__':
    main()
