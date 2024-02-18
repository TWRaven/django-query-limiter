from dataclasses import dataclass
from datetime import timedelta

from .formatting import humanize, format_sql


@dataclass
class Query:
    sql: str
    params: tuple[str]
    time_taken: timedelta | None = None

    def __str__(self):
        message = format_sql(self.sql, self.params)

        if not self.time_taken:
            return message

        return f"{message}\n(executed in {humanize(self.time_taken)})"
