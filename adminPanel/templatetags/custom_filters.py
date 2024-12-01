from django import template

register = template.Library()

@register.filter
def has_rooms_with_topic(rooms, topic):
    return rooms.filter(topic=topic).exists()
