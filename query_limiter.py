from contextlib import ExitStack, contextmanager
from dataclasses import dataclass
from django.db import connections


class QueryLimitExceeded(Exception):
    def __init__(self, limit: int, queries: list[str]):
        self.queries = queries
        self.limit = limit

        formatted_queries = "\n".join(f"{i}: {query}" for i, query in enumerate(queries))
        super().__init__(f"Query limit of {limit} exceeded.\nQueries:\n{formatted_queries}")


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
    db_connections = [connections[connection_name] for connection_name in (db_connections or list(connections))]
    limiter = QueryLimiter(limit=limit)

    managers = [connection.execute_wrapper(limiter) for connection in db_connections]

    with ExitStack() as stack:
        for manager in managers:
            stack.enter_context(manager)
        yield
