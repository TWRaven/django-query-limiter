Ever wanted to limit how many db queries a certain function or view can make? 
You're in luck!

Get it from [PyPi](https://pypi.org/project/django-query-limiter/0.0.1/):
```shell
pip install django-query-limiter==0.0.1
```

Usage:
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

@limit_queries(10, databases=['default'])
def my_view(request):
    return Model.objects.first()
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