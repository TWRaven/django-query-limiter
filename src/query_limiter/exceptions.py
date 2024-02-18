from datetime import timedelta

from .formatting import humanize
from .query import Query


class QueryLimitExceeded(Exception):
    def __init__(self, message: str, queries: list[Query]):
        self.queries = queries
        formatted_queries = "\n\n".join(f"{i}: {query}" for i, query in enumerate(queries))
        super().__init__(f"{message}\nQueries:\n{formatted_queries}")


class AmountExceeded(QueryLimitExceeded):
    def __init__(self, queries: list[Query], limit: int):
        self.limit = limit

        super().__init__(f"Query limit of {limit} exceeded. {len(queries)} queries were executed", queries)


class IndividualTimeExceeded(QueryLimitExceeded):
    def __init__(self, queries: list[Query], individual_time_limit: timedelta, time_taken: timedelta):
        self.individual_time_limit = individual_time_limit
        super().__init__(f"Individual query time limit of {humanize(individual_time_limit)} exceeded. The query took {humanize(time_taken)}", queries)


class TotalTimeExceeded(QueryLimitExceeded):
    def __init__(self, queries: list[Query], total_time_limit: timedelta, elapsed_time: timedelta):
        self.total_time_limit = total_time_limit
        self.elapsed_time = elapsed_time

        super().__init__(f"Total query time limit of {humanize(total_time_limit)} exceeded. The queries took {humanize(elapsed_time)}", queries)