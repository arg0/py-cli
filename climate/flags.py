# Copyright (c) 2013 Leif Johnson <leif@leifjohnson.net>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import argparse

'''Useful utilities for command-line arguments.'''


class ArgParser(argparse.ArgumentParser):
    '''This class provides some sane default command-line argument behaviors.

    In particular, the help formatter includes default values, and arguments can
    be loaded from files. Files can contain arguments in two ways: one per line,
    or many-per-line. For one-per-line arguments, spaces etc. are preserved,
    while for many-per-line arguments, the line must start with a dash, and
    multiple arguments are split on whitespace. In all cases, shell-style
    comments are removed from the file before processing.
    '''

    SANE_DEFAULTS = dict(
        fromfile_prefix_chars='@',
        conflict_handler='resolve',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    def __init__(self, *args, **kwargs):
        kwargs.update(ArgParser.SANE_DEFAULTS)
        super(ArgParser, self).__init__(*args, **kwargs)

    def convert_arg_line_to_args(self, line):
        '''Remove # comments and blank lines from arg files.'''
        S = '__@__'
        line = line.replace(r'\#', S).split('#')[0].strip().replace(S, '#')
        if line:
            if line[0] == '-' and ' ' in line:
                for p in line.split():
                    yield p
            else:
                yield line
