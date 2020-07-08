from pytheas.data.users import User


def get_usernames():
    return [u.username for u in User.objects()]
