from rest_framework.exceptions import NotFound, ValidationError
from .models import Book

def codeMapping(success,fail,total):
    if success == total:
        return 'success'
    elif fail == total:
        return 'failure'
    else:
        return 'partially_failure'
    
def translate2isbn(kwargs):
    try:
        isbn2query = kwargs['isbn']
        instance = Book.objects.get(isbn=isbn2query)
    except KeyError:
        raise ValidationError(detail='ISBN not provide')
    except Book.DoesNotExist:
        raise NotFound(detail='Book not found')
    except Exception as e:
        print(type(e).__name__)
        raise ValidationError(detail='ISBN not found')
    else:
        return instance

def sanitizedParams(queryParams,serializer):
    queryParams_keys = set(queryParams.keys())
    serializer_fields = set(serializer().fields)
    if queryParams_keys.intersection(serializer_fields):
        return {i:v for i,v in queryParams.items() if i in serializer_fields}
    else:
        return False

    
    
    