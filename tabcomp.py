from __future__ import print_function

import os
import argparse


class State(object):
    PREFIX_SPACES = 1
    TEXT = 2


def main(args):
    f = open(args.source, 'rb')
    w = open(args.source + '.tc', 'wb')

    prefix = ''
    curr_line_prefix = ''

    state = State.PREFIX_SPACES
    while True:
        c = f.read(1)
        if not c: break  # reached EOF

        if state == State.PREFIX_SPACES:
            if not c.isspace():
                if prefix.startswith(curr_line_prefix):
                    diff = len(prefix) - len(curr_line_prefix)
                    if diff > 0:
                        w.write('\x7f')
                        w.write(chr(diff))
                        # w.write(str(bytes(int(x,0) for x in ['\x7f', diff])))
                        print('backing out {0} indent chars'.format(diff))

                state = State.TEXT
                w.write(c)

            elif c == '\n':
                w.write(c)
                # if there is no whitespace on a line, don't count it for the current indent level
                curr_line_prefix = ''

            else:
                curr_line_prefix += c
                if not prefix.startswith(curr_line_prefix):
                    w.write(c)

        elif state == State.TEXT:
            if c == '\n':
                state = State.PREFIX_SPACES
                prefix = curr_line_prefix
                curr_line_prefix = ''

            w.write(c)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Compress source code indentation.')
    parser.add_argument('source', help='The source file. The output will be written on source.tc.')

    args = parser.parse_args()

    main(args)

