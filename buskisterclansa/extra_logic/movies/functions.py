from django.db.models import Q, Model
from django.core.exceptions import ObjectDoesNotExist

def get_dependant_object_if_it_exist(indie_object: Model, dependant_object_value, dependant_object_query):
    try:
        return indie_object.get(Q( (dependant_object_query, dependant_object_value) ))
    except ObjectDoesNotExist:
        return None