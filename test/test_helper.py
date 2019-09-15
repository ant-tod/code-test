'''
Testing for the helper module.
'''
import pytest
import random
from src.helper import list_of_chars, random_string, write_dummy_fixed_width, \
    parse_fixed_width_file, write_to_ascii_delim, read_from_ascii_delim
from src.spec import spec


def test_list_of_chars():
    '''Test that the right number of printable characters is returned.'''
    assert 216 == len(list_of_chars(spec))


def test_random_string():
    '''Test the random string generator works as expected with a given seed.'''
    random.seed(977)
    list_of_chars = ['a', 'b', 'c']
    assert random_string(list_of_chars, 10) == 'ccbbccacac'


def test_generate_parse():
    '''
    Use the generator and parse function to test each other.
    Really you should use a random seed again to test the generator against a
    known text file first, then test it against the parse,
    but time constraints.
    '''
    data = write_dummy_fixed_width(spec, 'tmp', 10)
    new_data = parse_fixed_width_file(spec, 'tmp')
    assert data == new_data


@pytest.mark.skip
def test_split_string():
    '''
    This test should check that strings are split on the given offsets.
    However this is tedious to code and I can use that to show skipping tests
    in pytest instead.
    '''
    assert False


@pytest.fixture
def create_fw_file():
    '''Crate a fixture for a dummy fixed width file.'''
    data = write_dummy_fixed_width(spec, 'tmp.fw', 10)
    return data


def test_ascii(create_fw_file):
    '''
    Use the ASCII parser and writer to test each other.
    Again a file should be tested against a known file, but with time
    constraints testing the two files against each other is a trade off.
    '''
    data = create_fw_file  # Assign the output of the fixture to data.
    ascii_data = write_to_ascii_delim(spec, 'tmp.fw', 'tmp.da')
    ascii_data_read = read_from_ascii_delim(spec, 'tmp.da')
    assert ascii_data == ascii_data_read
    assert data == ascii_data
    assert data == ascii_data_read
