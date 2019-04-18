Getting started
===============

.. toctree::

Install
-------

1. Download executable of `latest release`_.
2. Extract archive
3. Add folder with extracted files to PATH_

.. _PATH: https://en.wikipedia.org/wiki/PATH_(variable)
.. _`latest release`: https://github.com/pniedzwiedzinski/pseudo/releases/latest

If you're on macOs or Linux you probably have python3 installed. Then it will be easier to install it with Pip_.

Install from source
-------------------

Pip
~~~

You need to have python3.6 or greater. You can install pseudo with::

    python3 -m pip install git+https://github.com/pniedzwiedzinski/pseudo.git

Docker
~~~~~~

Download docker and follow instructions::

    docker pull pniedzwiedzinski/pseudo

    # Create alias
    alias pdc='docker run -it --rm -v $(pwd):/home pseudo'

Usage
-----

You can now use pseudo as::

    pdc test.pdc
