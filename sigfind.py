#!/usr/bin/env python3

from argparse import ArgumentParser
from os import stat

parser = ArgumentParser()
parser.add_argument('-o', dest='offset', type=int, default=0,
                    help='Give offset into block where signature should exist (default 0)')
parser.add_argument('-s', dest='seek', type=int, default=0,
                    help='Seek to this block before searching (default 0)')
parser.add_argument('-m', dest='max', type=int, default=0,
                    help='Matches to find before exiting (default 0)')
parser.add_argument('-l', dest='listing', action='store_true',
                    help='Print only matching file name')
parser.add_argument('hex_signature')
parser.add_argument('file')
args = parser.parse_args()

offset = int(args.offset)
hex_signature = bytes.fromhex(args.hex_signature)

sector_size = 512
size = stat(args.file).st_size
sectors = int(size/sector_size)
slen = len(str(size))
img = open(args.file, 'rb')
img.seek(args.seek * sector_size)

last = None
matches = 0
position = (args.seek - 1) * sector_size
while position < size:
    try:
        chunk = img.read(sector_size)
    except Exception as e:
        print(e)
        break
    position += sector_size
    match = False
    if offset == -1 and chunk.find(hex_signature) >= 0:
        match = True
    if chunk[offset:offset+len(hex_signature)] == hex_signature:
        match = True
    if match:
        sector = int(position / sector_size)
        if last is None:
            distance = '-'
        else:
            distance = '+{0}'.format(sector - last)
        last = sector
        if args.listing:
            print('File: {0}'.format(args.file))
            break
        print('Sector: {0} ({1})'.format(str(sector).zfill(slen), distance))
        matches += 1
        if args.max and matches >= args.max:
            break

