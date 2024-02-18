from contextlib import ExitStack, contextmanager
from dataclasses import dataclass
from datetime import timedelta
from time import perf_counter

from django.db import connections

from .exceptions import AmountExceeded, IndividualTimeExceeded, TotalTimeExceeded
from .query import Query

DISABLED = False
DEFAULT_DB_CONNECTIONS = None


@dataclass
class QueryLimiter:
    amount: int | None = None
    individual_max_time: timedelta | None = None
    total_max_time: timedelta | None = None
    queries: list[Query] = None

    def __post_init__(self):
        if self.amount is None and self.individual_max_time is None and self.total_max_time is None:
            raise ValueError("At least one of amount, individual_max_time, or total_max_time must be set.")

        self.queries = []
        self.elapsed_time_in_queries: timedelta = timedelta(0)

    def __call__(self, execute, sql, params, many, context):
        query = Query(sql, params)

        if self.amount is not None and len(self.queries) >= self.amount:
            raise AmountExceeded(self.queries + [query], self.amount)

        start = perf_counter()
        result = execute(sql, params, many, context)
        query.time_taken = timedelta(seconds=perf_counter() - start)
        self.elapsed_time_in_queries += query.time_taken

        self.queries.append(query)

        if self.individual_max_time is not None and query.time_taken > self.individual_max_time:
            raise IndividualTimeExceeded(self.queries, self.individual_max_time, query.time_taken)

        if self.total_max_time is not None and self.elapsed_time_in_queries > self.total_max_time:
            raise TotalTimeExceeded(self.queries, self.total_max_time, self.elapsed_time_in_queries)

        return result


@contextmanager
def limit_queries(
    amount: int | None = None,
    individual_max_time: timedelta | None = None,
    total_max_time: timedelta | None = None,
    db_connections: list[str] | None = None
):
    if DISABLED:
        yield
        return

    db_connections = [
        connections[connection_name]
        for connection_name in (db_connections or DEFAULT_DB_CONNECTIONS or list(connections))
    ]

    limiter = QueryLimiter(amount=amount, individual_max_time=individual_max_time, total_max_time=total_max_time)

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
