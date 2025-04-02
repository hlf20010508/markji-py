# :project: markji-py
# :author: L-ING
# :copyright: (C) 2025 L-ING <hlf01@icloud.com>
# :license: MIT, see LICENSE for more details.

import unittest
import warnings

from markji.auth import Auth
from tests import ENV, AsyncTestCase


class TestAuth(AsyncTestCase):
    @classmethod
    def setUpClass(cls):
        warnings.simplefilter("ignore", ResourceWarning)

    async def test_login(self):
        auth = Auth(ENV.username, ENV.password)
        await auth.login()


if __name__ == "__main__":
    unittest.main()
