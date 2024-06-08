Pipe-Utils
==========

Python but with pipes, utils, and pipe utils

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   quickstart
   pipe_objects
   it_and_obj
   curry
   api

Examples
-------

.. code-block::

    from pipe_utils import *

    words = "I just think pipes are neat!"

    result = (
          Pipe(words)
          | obj.lower()
          | obj.replace("!", "")
          | obj.split()
          | group_by(len)
          | sorted_dict()
          | unwrap
    )

    print(result)
    #  {1: ['i'], 3: ['are'], 4: ['just', 'neat'], 5: ['think', 'pipes']}

.. code-block::

    from pipe_utils.override import *

    data = [[1, -3, 4], [1, 2, 3], [2, 3, 4], [5, -1, 4]]

    result = (
          Pipe(data)
          | filter(all(it >= 0))
          | map(sum_by(it * it))
          | unwrap(as_list)
    )

    print(result)  # [14, 29]

.. code-block::

    from pipe_utils.override import *

    data = [[1, -3, 4], [1, 2, 3], [2, 3, 4], [5, -1, 4]]

    result = (
          Pipe >> data
          | filter >> all(it >= 0)
          | map >> sum_by(it * it)
          | unwrap >> as_list
    )

    print(result)  # [14, 29]

Install
-------

.. code-block::

    pip install pipe-utils

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
