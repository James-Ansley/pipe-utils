# Pipe Utils

Python with pipes, utils, and pipe utils.

> Note: pipe-utils is in alpha and significant API changes are expected

```python
from pipe_utils import Pipe
from pipe_utils.iterables import *

words = "I just think pipes are neat"

data = (
        Pipe(words)
        | str.lower
        | str.split
        | sorted_by(len)
        | group_by(len)
        | dict
).get()

print(data)
#  {1: ['i'], 3: ['are'], 4: ['just', 'neat'], 5: ['think', 'pipes']}
```

## Install

```
pip install pipe-utils
```
