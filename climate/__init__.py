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

'''Some utilities for command line interfaces!'''

from .log import enable_default_logging, get_logger
from .flags import parse_args, add_mutex_arg_group, add_arg_group, \
    add_arg, add_command

logging = get_logger('climate')

def call(main, default_level='INFO'):
    '''Enable logging and start up a main method.'''
    enable_default_logging(default_level=default_level)
    from . import flags
    if flags._ARGS is None:
        import plac
        return plac.call(main)
    args, kwargs = parse_args()
    logging.debug('running with arguments:')
    for k in sorted(kwargs):
        logging.debug('--%s = %s', k, kwargs[k])
    return main(args)
