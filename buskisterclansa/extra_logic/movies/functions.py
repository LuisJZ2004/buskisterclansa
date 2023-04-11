from django.db.models import Q, Model
from django.core.exceptions import ObjectDoesNotExist

def get_dependant_object_if_it_exist(indie_object: Model, dependant_object_value, dependant_object_query):
    """
    returns an dependant object if it exits, if not returns None
    """
    try:
        return indie_object.get(Q( (dependant_object_query, dependant_object_value) ))
    except ObjectDoesNotExist:
        return None
    
def like_dislike(request, action_to_do, action_to_delete):
    """
    Makes like or dislike depending on the action. 

    action_to_do and action_to_delete must be either like or dislike objects to make the actions.

    the goal is to be able to use the same code, either we want to like or dislike, so D.R.Y

    """
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