# Pipe Utils

Python with pipes, utils, and pipe utils.

```python
from pipe_utils import Pipe
from pipe_utils.iterables import *
from pipe_utils.mappings import *

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
```

## Install

```
pip install pipe-utils
```


## Docs

https://pipe-utils.rtfd.io
