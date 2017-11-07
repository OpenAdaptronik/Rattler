#!flask/bin/python
from coverage import coverage
cov = coverage(branch=True, omit=['flask/*', 'tests.py'])
cov.start()

import os
import unittest

from app.mod import f

class TestCase(unittest.TestCase):
    def test_avatar(self):
        assert f(0) == 1
        assert f(-1) == -1
    def test_error(self):
        assert f(1) > 1
        assert f(1) == 2

if __name__ == '__main__':
    try:
        unittest.main()
    except:
        pass
    cov.stop()
    cov.save()
    print("\n\nCoverage Report:\n")
    cov.report()
    print("HTML version: " + os.path.join(basedir, "tmp/coverage/index.html"))
    cov.html_report(directory='tmp/coverage')
    cov.erase()