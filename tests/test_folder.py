"""
:project: markji-py
:author: L-ING
:copyright: (C) 2025 L-ING <hlf01@icloud.com>
:license: MIT, see LICENSE for more details.
"""

import unittest
from tests import AsyncTestCase, ENV
from markji import Markji
from markji.auth import Auth


class TestFolder(AsyncTestCase):
    async def test_get(self):
        auth = Auth(ENV.username, ENV.password)
        token = await auth.login()
        client = Markji(token)

        folder_name = "t_folder"
        folder = await client.new_folder(folder_name)

        folder = await client.get_folder(folder.id)
        self.assertEqual(folder.name, folder_name)

        await client.delete_folder(folder.id)

    async def test_list(self):
        auth = Auth(ENV.username, ENV.password)
        token = await auth.login()
        client = Markji(token)

        folder_name = "t_folder"
        folder = await client.new_folder(folder_name)

        folders = await client.list_folders()
        self.assertTrue(len(folders) > 0)

        await client.delete_folder(folder.id)

    async def test_new(self):
        auth = Auth(ENV.username, ENV.password)
        token = await auth.login()
        client = Markji(token)

        folder_name = "t_folder"
        folder = await client.new_folder(folder_name)
        self.assertEqual(folder.name, folder_name)

        folder_name = "t"
        with self.assertRaises(ValueError):
            await client.new_folder(folder_name)

        folder_name = "t" + "_" * 8
        with self.assertRaises(ValueError):
            await client.new_folder(folder_name)

        await client.delete_folder(folder.id)

    async def test_delete(self):
        auth = Auth(ENV.username, ENV.password)
        token = await auth.login()
        client = Markji(token)

        folder_name = "t_folder"
        folder = await client.new_folder(folder_name)

        await client.delete_folder(folder.id)

        with self.assertRaises(FileNotFoundError):
            await client.get_folder(folder.id)

    async def test_rename(self):
        auth = Auth(ENV.username, ENV.password)
        token = await auth.login()
        client = Markji(token)

        folder_name = "t_folder"
        folder = await client.new_folder(folder_name)

        new_folder_name = "r_folder"
        folder = await client.rename_folder(folder.id, new_folder_name)

        self.assertEqual(folder.name, new_folder_name)

        new_folder_name = "t"
        with self.assertRaises(ValueError):
            await client.rename_folder(folder.id, new_folder_name)

        new_folder_name = "t" + "_" * 8
        with self.assertRaises(ValueError):
            await client.rename_folder(folder.id, new_folder_name)

        await client.delete_folder(folder.id)


if __name__ == "__main__":
    unittest.main()
