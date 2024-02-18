from datetime import timedelta

try:
    import sqlparse
except ImportError:
    sqlparse = None


try:
    from humanize import naturaldelta
except ImportError:
    naturaldelta = None


def format_sql(sql: str, params: tuple[str] | None) -> str:
    interpolated = sql % (params or [])

    if not sqlparse:
        return interpolated

    return sqlparse.format(interpolated, reindent=True)


def humanize(time: timedelta) -> str:
    if not naturaldelta:
        return str(time)

    return naturaldelta(time, minimum_unit='microseconds')
