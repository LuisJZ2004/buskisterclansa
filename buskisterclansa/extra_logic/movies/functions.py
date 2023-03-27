from django.db.models import Q, Model
from django.core.exceptions import ObjectDoesNotExist

def get_dependant_object_if_it_exist(indie_object: Model, dependant_object_value, dependant_object_query):
    try:
        return indie_object.get(Q( (dependant_object_query, dependant_object_value) ))
    except ObjectDoesNotExist:
        return None
    
def like_dislike(request, action_to_do, action_to_delete):
    try:
        action = action_to_do.get(user__pk=request.user.pk)
        action.delete()
    except ObjectDoesNotExist:
        try:
            contrary_action = action_to_delete.get(user__pk=request.user.pk)
            contrary_action.delete()
        except ObjectDoesNotExist:
            pass
        action_to_do.create(user=request.user)