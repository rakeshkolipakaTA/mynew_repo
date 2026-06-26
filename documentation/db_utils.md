# db_utils Module

Database utility helpers for mynew_repo.

## Functions

### get_user_by_id(user_id)

Retrieves a user record from the database by user ID.

**Parameters:**
- `user_id` (int): The ID of the user to retrieve.

**Returns:**
- Query result object from `db.execute()`.

**Example:**
```python
from db_utils import get_user_by_id

user = get_user_by_id(123)
```

## SQL Parameterization Requirement

⚠️ **Critical**: All SQL queries in this module **must use parameterized queries**. Never build SQL strings using string concatenation, f-strings, or `%` formatting. This is a hard requirement per project decision DEC-sql-1.

**Incorrect (do not do this):**
```python
query = "SELECT * FROM users WHERE id = " + str(user_id)
db.execute(query)
```

**Correct (use parameterized queries):**
```python
query = "SELECT * FROM users WHERE id = ?"
db.execute(query, (user_id,))
```

String-interpolated SQL is vulnerable to SQL injection and caused a real production incident. All contributors must follow this pattern when modifying or extending this module.

## See Also

- `.cwf/instructions.md` — Project conventions and decisions
- `memory/decisions/20260620T000000_DEC-sql-1.json` — Parameterized query requirement (DEC-sql-1)
