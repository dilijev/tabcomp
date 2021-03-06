# Tab Compression System

In source code files in virtually any format, tabs make up a huge part of the content of the files. Normal compression algorithms do a fair job of account for repeated information, like large blocks of whitespace, but they don't completely capture the structure and role of whitespace in source files. Additionally, saving source files in compressed format and then reloading them from that compressed format takes a long time and is inconvenient. Those algorithms are highly complex and for large source files will take much longer than necessary to uncompress for the amount of savings achieved.

This program will allow users to perform a quick compression of their source files by relying on the inherently repetitive nature of the whitespace at the beginning of lines.

The program will read a source file line by line and take note of the whitespace at the beginning of lines. When the amount of whitespace changes, the program will take note of the difference between the old and new indentation levels. If the indentation increases, the program will write just the whitespace difference on the output file. If the indentation decreases, the program will write a byte which indicates characters will be removed from the indentation level and then another byte which indicates how many characters should be removed.

## Usage

Given a source file, `source` and a destination file `dest` use `python tabcomp.py source dest` to tab-compress `source` and write the output to `dest`.

To de-compress the `dest` file from above back into the `source` file use `python tabexp.py dest source`.

The documentation for `tabexp.py` will use `source` to refer to the file it is reading, which is intended to be the compressed file, and which is `dest` in the above example.

See `python tabcomp.py -h` and `python tabexp.py -h` for more info on parameters.

## Warning

Behavior for decompressing a usual source file is undefined, but in practice it will end up being a heavily-indented version of itself, which in the case of a language like python will mean the output will not be a correct program anymore (will likely not run, but at least will produce incorrect results, unless there were no indents at all).
