import os
import unittest
import yaml

from utils.sql_util import MysqlFactory

HOME = os.path.abspath(os.path.dirname(os.getcwd()))


class MyTestCase(unittest.TestCase):
    def testMySql(self):
        print(HOME)
        filepath = os.path.join(HOME, 'config/config.yaml')
        f = open(filepath, 'r')
        ystr = f.read()

        aa = yaml.load(ystr, Loader=yaml.FullLoader)
        print(aa)


if __name__ == '__main__':
    unittest.main()
