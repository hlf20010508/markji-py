"""
:project: markji-py
:author: L-ING
:copyright: (C) 2025 L-ING <hlf01@icloud.com>
:license: MIT, see LICENSE for more details.
"""

from aiohttp import ClientSession
from markji._const import _API_URL, _LOGIN_ROUTE
from markji.types._form import _LoginForm


class Auth:
    """
    Auth 认证登陆

    .. Example::
    .. code-block:: python
        from markji.auth import Auth

        auth = Auth("username", "password")
        token = await auth.login()
    """

    def __init__(self, username: str, password: str):
        """
        初始化Auth

        :param str username: 用户名（手机号、邮箱）
        :param str password: 密码
        """
        self._username = username
        self._password = password

    async def login(self) -> str:
        """
        登陆
        获取用户token

        :return str: 用户token
        """
        async with ClientSession(base_url=_API_URL) as session:
            response = await session.post(
                _LOGIN_ROUTE,
                json=_LoginForm(self._username, self._password).to_dict(),
            )
            if response.status != 200:
                raise Exception(f"登陆失败: {response}{await response.text()}")
            content: dict = await response.json()
            token: str = content["data"]["token"]

        return token
