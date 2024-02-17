from contextlib import ExitStack, contextmanager
from dataclasses import dataclass
from django.db import connections

from .exceptions import QueryLimitExceeded

DISABLED = False
DEFAULT_DB_CONNECTIONS = None


@dataclass
class QueryLimiter:
    limit: int
    queries: list[str] = None

    def __call__(self, execute, sql, params, many, context):
        if not self.queries:
            self.queries = []
        self.queries.append(sql)

        if len(self.queries) > self.limit:
            raise QueryLimitExceeded(self.limit, self.queries)
        return execute(sql, params, many, context)


@contextmanager
def limit_queries(limit: int, db_connections: list[str] | None = None):
    if DISABLED:
        yield
        return

    db_connections = [
        connections[connection_name]
        for connection_name in (db_connections or DEFAULT_DB_CONNECTIONS or list(connections))
    ]

    limiter = QueryLimiter(limit=limit)

    managers = [connection.execute_wrapper(limiter) for connection in db_connections]

    with ExitStack() as stack:
        for manager in managers:
            stack.enter_context(manager)
        yield


def disable_query_limiter():
    global DISABLED
    DISABLED = True


def set_default_db_connections(db_connections: list[str]):
    global DEFAULT_DB_CONNECTIONS
    DEFAULT_DB_CONNECTIONS = db_connections
