Ever wanted to limit how many db queries a certain function or view can make? 
You're in luck!

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