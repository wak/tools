import config
import unittest

class TestStringMethods(unittest.TestCase):
    def test_undefined_key_load(self):
        self.assertEqual(config.load('dummy'), None)
        self.assertEqual(config.load('dummy', 'testtest'), 'testtest')

    def test_save(self):
        config.save('test01', 'hello')
        self.assertEqual(config.load('test01'), 'hello')

        config.save('test01', 'hello overwrite')
        self.assertEqual(config.load('test01'), 'hello overwrite')

unittest.main()
