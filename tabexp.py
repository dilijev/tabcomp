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

    state = State.PREFIX_SPACES
    while True:
        c = f.read(1)
        if not c: break  # reached EOF

        if state == State.PREFIX_SPACES:
            if c == '\x7f':
                diff = ord(f.read(1))
                prefix = prefix[:-diff]  # remove the last _diff_ indent characters from the prefix
                # don't change states here because this allows whitespace to be inserted after these bytes
            elif not c.isspace():
                w.write(prefix)
                w.write(c)
                state = State.TEXT
            elif c == '\n':
                w.write(c)
            else:
                prefix += c

        elif state == State.TEXT:
            if c == '\n':
                state = State.PREFIX_SPACES

            w.write(c)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Expand source code indentation.')
    parser.add_argument('source', help='The file to expand.')
    parser.add_argument('output', help='The output of this command.')

    args = parser.parse_args()

    main(args)

