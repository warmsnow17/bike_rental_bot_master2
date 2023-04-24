from fastapi import Depends, Form
from starlette.requests import Request

from fastapi_admin.depends import get_current_admin, get_resources
from fastapi_admin.models import AbstractAdmin
from fastapi_admin.providers.login import UsernamePasswordProvider


class LoginProvider(UsernamePasswordProvider):
    pass
