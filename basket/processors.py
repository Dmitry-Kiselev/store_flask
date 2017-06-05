from flask_login import current_user


def basket_processor():
    count = current_user.get_basket.lines_count
    return {'basket_lines_count': count}
