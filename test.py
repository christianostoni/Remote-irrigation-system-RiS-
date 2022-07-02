from time import sleep
import unittest

from database import Database

import hashlib
import base64

database = Database()
password = base64.b64encode(bytes(hashlib.sha1(b'1234').hexdigest(), 'ascii')).decode('ascii')

class TestDatabase(unittest.TestCase):
    def test01_register(self):
        self.assertEqual(database.register('nishijima', password), True)

    def test02_login(self):
        self.assertEqual(database.login('nishijima', password), True)

    def test03_token(self):
        # Generazione token
        token1 = database.gen_token('nishijima', password)
        sleep(0.1)
        token2 = database.gen_token('nishijima', password)

        self.assertEqual(len(token1) + len(token2), 128)
        self.assertEqual(token1 != token2, True)
        # Recupero token
        self.assertEqual(database.retrive_token(token2), True)

    def test04_cleanup(self):
        self.assertEqual(database.delete_account('nishijima'), True)

unittest.main()