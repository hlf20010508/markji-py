"""
:project: markji-py
:author: L-ING
:copyright: (C) 2025 L-ING <hlf01@icloud.com>
:license: MIT, see LICENSE for more details.
"""

import unittest
from tests import AsyncTestCase, ENV
from markji.auth import Auth


class TestFolder(AsyncTestCase):
    async def test_folder_rename(self):
        auth = Auth(ENV.username, ENV.password)
        user = await auth.login()

        folder_name = "t_folder"
        folder = await user.new_folder(folder_name)

        new_folder_name = "r_folder"
        await folder.rename(new_folder_name)

        self.assertEqual(folder.name, new_folder_name)

        new_folder_name = "t_folder" + "_" * 8
        with self.assertRaises(ValueError):
            await folder.rename(new_folder_name)

        await folder.delete()


if __name__ == "__main__":
    unittest.main()
