import sys

sys.path.append('../')

from app import github


def test_app_index():
    print github.hello_worl()
