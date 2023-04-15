Pipe-Utils
==========

Python but with pipes, utils, and pipe utils

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   quickstart
   pipe_objects
   it
   api

Example
-------

.. code-block::

    from pipe_utils import *

    words = "I just think pipes are neat"

    result = (
            Pipe(words)
            | str.lower
            | str.split
            | group_by(len)
            | sorted_dict
    ).get()

    print(result)
    #  {1: ['i'], 3: ['are'], 4: ['just', 'neat'], 5: ['think', 'pipes']}

Install
-------

.. code-block::

    pip install pipe-utils

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
