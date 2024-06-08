# Pipe Utils

Python with pipes, utils, and pipe utils.

## Install

```
pip install pipe-utils
```

## Docs

[https://pipe-utils.rtfd.io](https://pipe-utils.rtfd.io)

## Example

```python
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
```

And, if you're feeling dangerous, override builtin functions
like `filter`, `map`, and `all` by importing from `pipe_utils.override`:

```python
from pipe_utils.override import *

data = [[1, -3, 4], [1, 2, 3], [2, 3, 4], [5, -1, 4]]

result = (
      Pipe(data)
      | filter(all(it >= 0))
      | map(sum_by(it * it))
      | unwrap(as_list)
)

print(result)  # [14, 29]
```

And, if you're feeling extra dangerous, you can use arrow syntax to clean up
some of those brackets:

```python
from pipe_utils.override import *

data = [[1, -3, 4], [1, 2, 3], [2, 3, 4], [5, -1, 4]]

result = (
      Pipe >> data
      | filter >> all(it >= 0)
      | map >> sum_by(it * it)
      | unwrap >> as_list
)

print(result)  # [14, 29]
```
