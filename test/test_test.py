'''
To test that tests run in the docker container.
'''
import pytest


def test_test():
    '''Passing test.'''
    assert True


@pytest.mark.skip(reason='test skip')
def test_skip():
    '''Skipping test.'''
    assert False


@pytest.mark.xfail
def test_fail():
    '''Failing test.'''
    assert False
