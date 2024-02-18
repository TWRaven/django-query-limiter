Ever wanted to limit how many db queries a certain function or view can make? 
You're in luck!

Get it from [PyPi](https://pypi.org/project/django-query-limiter/):
```shell
pip install django-query-limiter[formatting]
```

## Basic usage

```python
from your_django_models import Model
from query_limiter import limit_queries

with limit_queries(1):
    print(Model.objects.first()) # Prints your model's first object

with limit_queries(1):
    print(Model.objects.first()) # Prints your model's first object
    print(Model.objects.first()) # Raises QueryLimitError
```

It can also be used as a function decorator, and can limit queries on a per-database level:
```python
from your_django_models import Model
from query_limiter import limit_queries

@limit_queries(10, db_connections=['default'])
def my_view(request):
    return Model.objects.first()
```

Multiple limits can be specified, and the first one to be reached will raise a `QueryLimitExceeded` exception:
```python
from your_django_models import Model
from query_limiter import limit_queries
from datetime import timedelta

@limit_queries(
    amount=2, 
    individual_max_time=timedelta(milliseconds=100), 
    total_max_time=timedelta(seconds=1),
)
def my_view(request):
    Model.objects.first() # if this query takes more than 100ms -> QueryLimitExceeded
    Model.objects.first() # if the total time of all queries takes more than 1s -> QueryLimitExceeded
    Model.objects.first() # if this query is reached -> QueryLimitExceeded
```

You can globally disable the query limiter:
```python
from your_django_models import Model
from query_limiter import limit_queries, disable_query_limiter

if settings.ENVIROMENT == 'production':
    disable_query_limiter()

with limit_queries(1):
    print(Model.objects.first())  # Prints your model's first object
    print(Model.objects.first())  # Prints your model's first object
```

The default behaviour is to limit the connections to all databases. This can be globally overwriten like so:
```python
from query_limiter import set_default_databases

set_default_databases(['your_database_name', 'another_database_name'])
```
Unless the db connections are specified in the `limit_queries` decorator, these databases will be used.



### Formatting

The `formatting` extra:
 - humanizes all timedelta outputs
 - uses `sqlparse` to format the queries to be more human readable
