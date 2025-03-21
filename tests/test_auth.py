"""
:project: markji-py
:author: L-ING
:copyright: (C) 2025 L-ING <hlf01@icloud.com>
:license: MIT, see LICENSE for more details.
"""

import unittest
from tests.utils import ENV
from markji.auth import Auth


class TestAuth(unittest.IsolatedAsyncioTestCase):
    async def test_login(self):
        auth = Auth(ENV.username, ENV.password)
        await auth.login()

        self.assertTrue(auth.token is not None)


if __name__ == "__main__":
    unittest.main()
