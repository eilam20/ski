from django import template

register = template.Library()

@register.filter
def add_attrs(field, attrs):
    """Adds HTML attributes to a Django form field."""
    if not hasattr(field, 'field'):
        return field
    # Convert the string to a dictionary
    attrs_dict = dict(item.split(":") for item in attrs.split(","))
    field.field.widget.attrs.update(attrs_dict)
    return field
