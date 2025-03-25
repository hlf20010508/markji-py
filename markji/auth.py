# :project: markji-py
# :author: L-ING
# :copyright: (C) 2025 L-ING <hlf01@icloud.com>
# :license: MIT, see LICENSE for more details.

from aiohttp import ClientSession
from markji._response import _ResponseWrapper
from markji._const import _API_URL, _LOGIN_ROUTE
from markji.types._form import _LoginForm


class Auth:
    """
    登陆认证
    """

    def __init__(self, username: str, password: str):
        """
        登陆认证

        :param str username: 用户名（手机号、邮箱）
        :param str password: 密码

        .. code-block:: python

            from markji.auth import Auth

            auth = Auth("username", "password")
            token = await auth.login()
        """
        self._username = username
        self._password = password

    async def login(self) -> str:
        """
        登陆

        获取用户token

        :return: 用户token
        :rtype: str
        :raises aiohttp.ClientResponseError: 登陆失败
        """
        async with ClientSession(base_url=_API_URL) as session:
            async with session.post(
                _LOGIN_ROUTE,
                json=_LoginForm(self._username, self._password).to_dict(),
            ) as response:
                response = _ResponseWrapper(response)
                await response.raise_for_status()
                content: dict = await response.json()
                token: str = content["data"]["token"]

        return token
