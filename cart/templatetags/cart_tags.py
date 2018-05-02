from django import template
from ..models import Cart


register = template.Library()


@register.simple_tag
def get_cart_count(user_id):
    if user_id != '':
        cart_records = Cart.objects.filter(user_id=user_id)
        count = cart_records.count()
        return count
    else:
        return 0
