from django.db.models import QuerySet
from django.http import Http404
from django.db.models import Model, Q
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist

def make_pagination(queryset: QuerySet, page_number: int, pagination_number: int):
    """
    Paginates a queryset.

    page_number: the page number you want
    pagination_number: the number of objects you want by each page

    """
    assert page_number != 0, "you can't paginate from zero"
    return queryset[pagination_number*(page_number-1):(pagination_number*(page_number-1)+pagination_number)]

def get_pagination_numbers(queryset: list, pagination_number: int):
    """
    How many pages a queryset is divided
    """
    final_number = 0
    i = 1
    while True:
        if make_pagination(queryset, i, pagination_number):
            final_number += 1
            i += 1
        else:
            break

    return final_number

def int_or_404(value):
    """
    turns a value into an int value and returns it, if ValueError or TypeError, 404
    """
    try:
        return int(value)
    except ValueError:
        raise Http404
    except TypeError:
        raise Http404
    
def object_exist(query_str: str, value_to_query, model: Model):
    """
    returns if an object exists or not 
    """
    try:
        model.objects.get(Q( (query_str, value_to_query) ))
        return True
    except MultipleObjectsReturned:
        return True
    except ObjectDoesNotExist: 
        return False