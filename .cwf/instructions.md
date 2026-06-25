# Start from Here.

## mynew_repo

### Conventions

All database access MUST use parameterized queries — never string concatenation or
% / f-string interpolation into SQL. This is a hard rule, not a suggestion, after a
real incident (see memory/decisions/) where string-built SQL caused a production
issue.
