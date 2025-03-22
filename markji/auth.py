"""
:project: markji-py
:author: L-ING
:copyright: (C) 2025 L-ING <hlf01@icloud.com>
:license: MIT, see LICENSE for more details.
"""

from aiohttp import ClientSession
from typing import Dict
from markji.const import API_URL, LOGIN_URL


class Auth:
    """
    Auth 认证登陆

    示例::
        from markji.auth import Auth

        auth = Auth("username", "password")
        token = await auth.login()
    """

    def __init__(self, username: str, password: str):
        """
        初始化Auth

        :param username: 用户名（手机号、邮箱）
        :param password: 密码
        """
        self._username = username
        self._password = password

    async def login(self) -> str:
        """
        登陆
        获取用户token

        :return: str
        """
        async with ClientSession(base_url=API_URL) as session:
            response = await session.post(
                LOGIN_URL,
                json={
                    "identity": self._username,
                    "password": self._password,
                    "nuencrypt_fields": ["password"],
                },
            )
            if response.status != 200:
                raise Exception(f"登陆失败: {response}")
            content: Dict = await response.json()
            token: str = content["data"]["token"]

        return token
