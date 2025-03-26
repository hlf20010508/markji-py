# :project: markji-py
# :author: L-ING
# :copyright: (C) 2025 L-ING <hlf01@icloud.com>
# :license: MIT, see LICENSE for more details.

import unittest
from aiohttp import ClientResponseError
from markji.types.folder import Folder, RootFolder
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
        self.addCleanup(client.delete_folder, folder.id)

        folder = await client.get_folder(folder.id)

        self.assertEqual(folder.name, folder_name)
        self.assertTrue(isinstance(folder, Folder))

        root_folder = await client.get_root_folder()
        folder = await client.get_folder(root_folder.id)

        self.assertTrue(isinstance(folder, RootFolder))

    async def test_get_root(self):
        auth = Auth(ENV.username, ENV.password)
        token = await auth.login()
        client = Markji(token)

        folder = await client.get_root_folder()
        self.assertEqual(folder.name, "root")

    async def test_list(self):
        auth = Auth(ENV.username, ENV.password)
        token = await auth.login()
        client = Markji(token)

        folder_name = "t_folder"
        folder = await client.new_folder(folder_name)
        self.addCleanup(client.delete_folder, folder.id)

        folders = await client.list_folders()
        self.assertTrue(len(folders) > 0)

    async def test_new(self):
        auth = Auth(ENV.username, ENV.password)
        token = await auth.login()
        client = Markji(token)

        folder_name = "t_folder"
        folder = await client.new_folder(folder_name)
        self.addCleanup(client.delete_folder, folder.id)
        self.assertEqual(folder.name, folder_name)

        folder_name = "t"
        with self.assertRaises(ValueError):
            await client.new_folder(folder_name)

        folder_name = "t" + "_" * 8
        with self.assertRaises(ValueError):
            await client.new_folder(folder_name)

    async def test_delete(self):
        auth = Auth(ENV.username, ENV.password)
        token = await auth.login()
        client = Markji(token)

        folder_name = "t_folder"
        folder = await client.new_folder(folder_name)

        await client.delete_folder(folder.id)

        with self.assertRaises(ClientResponseError):
            await client.get_folder(folder.id)

    async def test_rename(self):
        auth = Auth(ENV.username, ENV.password)
        token = await auth.login()
        client = Markji(token)

        folder_name = "t_folder"
        folder = await client.new_folder(folder_name)
        self.addCleanup(client.delete_folder, folder.id)

        new_folder_name = "r_folder"
        folder = await client.rename_folder(folder.id, new_folder_name)

        self.assertEqual(folder.name, new_folder_name)

        new_folder_name = "t"
        with self.assertRaises(ValueError):
            await client.rename_folder(folder.id, new_folder_name)

        new_folder_name = "t" + "_" * 8
        with self.assertRaises(ValueError):
            await client.rename_folder(folder.id, new_folder_name)

    async def test_sort(self):
        auth = Auth(ENV.username, ENV.password)
        token = await auth.login()
        client = Markji(token)

        existed_folders = await client.list_folders()
        existed_folder_ids = [i.id for i in existed_folders]

        folder_name1 = "t_f1"
        folder1 = await client.new_folder(folder_name1)
        self.addCleanup(client.delete_folder, folder1.id)
        folder_name2 = "t_f2"
        folder2 = await client.new_folder(folder_name2)
        self.addCleanup(client.delete_folder, folder2.id)

        folder_ids = [folder2.id, folder1.id]
        folder_ids.extend(existed_folder_ids)
        root_folder = await client.sort_folders(folder_ids)

        self.assertEqual([i.object_id for i in root_folder.items], folder_ids)


if __name__ == "__main__":
    unittest.main()
