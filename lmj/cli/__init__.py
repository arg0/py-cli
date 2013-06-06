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

'''Some utilities for command line interfaces !'''

from .log import enable_default_logging, get_logger


def call(main):
    '''Enable logging and start up a main method.'''
    enable_default_logging()
    if _ARGS:
        main(_ARGS.parse_args())
    else:
        import plac
        plac.call(main)


def annotate(*args, **kwargs):
    '''Return a decorator for plac-style argument annotations.'''
    import plac
    return plac.annotations(*args, **kwargs)


_ARGS = None

def get_args():
    '''Enable arguments through the Python argparse module.'''
    global _ARGS
    if not _ARGS:
        from .flags import ArgParser
        _ARGS = ArgParser()
    return _ARGS

def add_mutex_arg_group(*args, **kwargs):
    return get_args().add_mutually_exclusive_group(*args, **kwargs)

def add_arg_group(*args, **kwargs):
    return get_args().add_argument_group(*args, **kwargs)

def add_arg(*args, **kwargs):
    return get_args().add_argument(*args, **kwargs)
