from django import template

register = template.Library()

@register.filter(name="has_voted")
def has_voted(user, voters):# this function is checking if the loged in user is part of the voters
    return any(user.id== voter.id for voter in voters)