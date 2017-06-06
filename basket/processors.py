from flask_login import current_user

from extensions import cache


def basket_processor():
    if not current_user.is_authenticated():
        return {}
    try:
        key = current_user.get_basket.id
        count = cache.get('basket_{}'.format(key))
    except (AttributeError, ConnectionError) as e:
        count = current_user.get_basket.lines_count
    else:
        cache.set('basket_{}'.format(key), count, None)

    return {
        'basket_lines_count': count or 'empty'}
