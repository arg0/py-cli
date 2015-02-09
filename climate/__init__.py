'''Some utilities for command line interfaces!'''

from .log import *
from .flags import *

import plac

logging = get_logger(__name__)


def annotate(*args, **kwargs):
    '''Return a decorator for plac-style argument annotations.'''
    return plac.annotations(*args, **kwargs)


def call(main, default_level='INFO'):
    '''Enable logging and start up a main method.'''
    enable_default_logging(default_level=default_level)
    from . import flags
    if flags.PARSER is None:
        return plac.call(main)
    args, rest = parse_known_args()
    if rest:
        logging.debug('unknown arguments: %s', rest)
    logging.debug('running with arguments:')
    kwargs = vars(args)
    for k in sorted(kwargs):
        logging.debug('--%s = %s', k, kwargs[k])
    return main(args)
