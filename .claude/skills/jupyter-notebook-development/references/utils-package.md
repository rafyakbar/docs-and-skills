# Utils Package Pattern

When `utils.py` exceeds ~200 lines, refactor into a package:

```
utils/
├── __init__.py       # re-exports everything
├── helpers.py        # full_url, normalize, safe_filename
├── parsing.py        # parse_something, extract_items
└── model.py          # build_model, train_model
```

### `__init__.py`:

```python
from .helpers import BASE_URL, full_url, normalize
from .parsing import parse_data
from .model import build_model, train_model
```

### Notebook import (unchanged):

```python
import utils as u
# u.parse_data(...), u.normalize(...), etc.
```
