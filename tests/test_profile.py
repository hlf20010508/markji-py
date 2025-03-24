# :project: markji-py
# :author: L-ING
# :copyright: (C) 2025 L-ING <hlf01@icloud.com>
# :license: MIT, see LICENSE for more details.

import unittest
from tests import AsyncTestCase, ENV
from markji import Markji
from markji.auth import Auth


class TestProfile(AsyncTestCase):
    async def test_get(self):
        auth = Auth(ENV.username, ENV.password)
        token = await auth.login()
        client = Markji(token)

        await client.get_profile()

    async def test_query(self):
        auth = Auth(ENV.username, ENV.password)
        token = await auth.login()
        client = Markji(token)

        profile = await client.get_profile()

        users = await client.query_users([profile.id])

        self.assertEqual(len(users), 1)
        self.assertEqual(users[0].id, profile.id)


if __name__ == "__main__":
    unittest.main()
