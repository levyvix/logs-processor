"""
DB module

how to use:

```python
from db import Database

with Database() as db:
    db.create_table()
    db.insert_logs(("INFO", "message", "timestamp"))
```
"""

from .database import Database

__all__ = ["Database"]
