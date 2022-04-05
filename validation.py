from database import commands as c


def register_user_validation(username, password):
    data = c.select(c.GET_USER_BY_USERNAME, (username,))
    if len(data) != 0:
        return f"user already registered"
    if len(password) < 6:
        return f"password must be at least 6 character"
    return 'success'


def login_user_validation(username, password):
    user = c.select(c.GET_USER_BY_USERNAME, (username,))
    if len(user) == 0:
        return f"this username is not exist"
    user = user[0]
    if user[2] != password:
        return f"username and password are not same"
    return 'success'
