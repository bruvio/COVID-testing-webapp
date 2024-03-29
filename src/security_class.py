from src.models.user import UserModel
from werkzeug.security import safe_str_cmp


def authenticate(username, password):
    user = UserModel.find_by_username(
        username
    )  # if there is not a username with username will return None
    if user and safe_str_cmp(user.password, password):
        return user


def identity(payload):
    user_id = payload["identity"]
    return UserModel.find_by_id(user_id)
