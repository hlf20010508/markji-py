# :project: markji-py
# :author: L-ING
# :copyright: (C) 2025 L-ING <hlf01@icloud.com>
# :license: MIT, see LICENSE for more details.

import asyncio
import unittest
import warnings
import os
from markji import Markji
from markji.auth import Auth


class AsyncTestCase(unittest.IsolatedAsyncioTestCase):
    client: Markji

    @classmethod
    def setUpClass(cls):
        warnings.simplefilter("ignore", ResourceWarning)

        token = asyncio.run(Auth(ENV.username, ENV.password).login())
        cls.client = Markji(token)


class Env:
    def __init__(self):
        self.username: str = os.environ["MARKJI_USERNAME"]
        self.password: str = os.environ["MARKJI_PASSWORD"]


ENV = Env()
