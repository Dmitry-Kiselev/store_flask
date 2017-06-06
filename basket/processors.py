from flask_login import current_user


def basket_processor():
    try:
        count = current_user.get_basket.lines_count
    except AttributeError:
        return {}
    return {'basket_lines_count': count}
