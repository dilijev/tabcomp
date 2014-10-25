from __future__ import print_function

import os
import argparse


class State(object):
    PREFIX_SPACES = 1
    TEXT = 2


def main(args):
    f = open(args.source, 'rb')
    w = open(args.output, 'wb')

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
                        if args.verbose:
                            print('backing out {0} indent chars'.format(diff))

                state = State.TEXT
                w.write(c)

            elif c == '\n':
                w.write(c)
                # if there is no whitespace on a line, don't count it for the current indent level
                # TODO make this so that if there is nothing besides /\s\+/ on a line, don't count it
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
    parser.add_argument('output', nargs='?', help='The file the output will be written to.',
            default=None)
    parser.add_argument('-v', '--verbose', action='store_true')

    args = parser.parse_args()
    if not args.output:
        args.output = args.source + ".tc"

    if args.verbose:
        print('Reading "{0}" and writing output to "{1}"'.format(args.source, args.output))

    main(args)

