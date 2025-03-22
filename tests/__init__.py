import unittest
import warnings
import os


class AsyncTestCase(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        warnings.simplefilter("ignore", ResourceWarning)


class Env:
    def __init__(self):
        self.username: str = os.environ["MARKJI_USERNAME"]
        self.password: str = os.environ["MARKJI_PASSWORD"]


ENV = Env()
