climate
=======

This package contains some basic command line utilities for Python:

- one wrapper over ``plac`` for quick command-line argument processing
- another for ``logging`` that lets us avoid copying that same horrid
  ``logging.basicConfig(...)`` business in all of our scripts, and gives a
  sensible default logging style

Install either from this repository, or with pip::

    pip install climate

Documentation for the package is at http://pythonhosted.org/climate.

Usage
-----

At its most basic, just import the module into your script and use it to call
your main function::

    import climate
    import logging

    def main(foo=1, bar='hello'):
        logging.info('%s %s', foo, bar)

    if __name__ == '__main__':
        climate.call(main)

``plac`` wrapper
~~~~~~~~~~~~~~~~

Automagically, the logging module will be configured for you! If you'd like to
set the values for ``main`` from the command-line, just include an annotation (a
straight wrapper over ``plac`` functionality)::

    import climate
    import logging

    @climate.annotate(
        foo=('value to use', 'option', None, int),
        bar=('greeting to offer', 'option'),
    )
    def main(foo=1, bar='hello'):
        logging.info('%s %s', foo, bar)

    if __name__ == '__main__':
        climate.call(main)

``argparse`` wrapper
~~~~~~~~~~~~~~~~~~~~

Finally, if you prefer using slightly more heavy-weight command line arguments,
``climate`` provides some convenience wrappers for you::

    import climate
    import logging

    g = climate.add_group('Foo')
    g.add_argument('-a', '--alfred', type=int, default=2, help='ALFRED!')
    g.add_argument('-b', '--betty', type=int, default=3, help='BETTY!')

    def main(args):
        logging.info('%s %s', args.alfred, args.betty)

    if __name__ == '__main__':
        climate.call(main)

Then, as with using the ``plac`` wrapper, calling your script with ``-h`` or
``--help`` will give you command-line usage help for free! The usage in this
case will include a summary of the default value for each argument.

Unfortunately, at the moment if you mix the ``plac`` wrapper with the
``argparse`` one, then confusing things happen. Just use one or the other. My
recommendation is to use the ``plac`` wrapper for one-off scripts, and the
``argparse`` wrapper for anything that's likely to be turned into a library.

Argument files
~~~~~~~~~~~~~~

If you're using the ``argparse`` wrapper, ``climate`` allows you to load
command-line arguments from a file, using the ``@filename`` command-line
syntax::

    python biochem-experiment.py --alfred 201 @experiment-01.args

Inside the argument file, lines starting with ``--`` are automatically split
into multiple options, and lines not starting with ``--`` are treated as a
single option. In addition, Python-style (aka shell-style) comments are ignored,
so you can keep your command-line arguments annotated with comments as needed.

If you need to include a literal hash ``#`` character in your options for some
reason, just escape the hash by prefixing it with a backslash::

    --flavor raspberry
    --color \#f39

License
-------

The contents of ``log.py`` were mostly written by Bryan Silverthorn
<bsilvert@cs.utexas.edu> as part of the utcondor_ package.

The other files are covered by the MIT license.

.. _utcondor: http://github.com/bsilvert/utcondor
