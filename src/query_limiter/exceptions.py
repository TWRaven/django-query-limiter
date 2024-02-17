class QueryLimitExceeded(Exception):
    def __init__(self, limit: int, queries: list[str]):
        self.queries = queries
        self.limit = limit

        formatted_queries = "\n".join(f"{i}: {query}" for i, query in enumerate(queries))
        super().__init__(f"Query limit of {limit} exceeded.\nQueries:\n{formatted_queries}")
