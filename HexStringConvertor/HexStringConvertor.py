#coding:utf-8
import sys, getopt


def ToString(endianness, hexdata):

    bigendiandata = ''

    datalen = len(hexdata)
    counter = 0
    while counter+4 <= datalen:
        bigendiandata = bigendiandata + '\u'
        bigendiandata = bigendiandata + hexdata[counter+2:counter+4]
        bigendiandata = bigendiandata + hexdata[counter:counter+2]
        counter += 4
    if counter < datalen:
        bigendiandata = bigendiandata + hexdata[counter:datalen]

    return bigendiandata


if __name__ == '__main__':

    endiannes = 'little-endian'
    method = 'ToString'

    if len(sys.argv) >= 2:
        prompt = '-h: help\n'
        prompt += '--endianness: little-endian or big-endian\n'
        prompt += '--method: ToHex Or ToString\n'

        opts, args = getopt.getopt(sys.argv[1:], 'h', ['endianness=', 'method='])
        for opt, value in opts:
            if opt == '-h':
                print prompt
                sys.exit(0)
            else:
                if opt == '--endianness':
                    endiannes = value
                elif opt == '--method':
                    method = value

    while True:
        data = raw_input("raw_input: ")
        data = data.replace(' ', '')

        if method == 'ToString':
            print ToString(endiannes, data)






