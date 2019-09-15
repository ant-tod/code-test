'''
A module that creates a random fixed width file file_fw, reads the contents
and outputs them to an ASCII delimited file file_ad.

Or reads a given fixed width file file_fw and outputs it to a ASCII delimited
file file_ad.
'''
from .helper import *
import logging


logger = logging.getLogger(__name__)


def app(spec, file_fw, file_ad, random=True):
    if random == 'random':
        data = write_dummy_fixed_width(spec, file_fw, 10)
        logging.info(data)
    elif random != 'file':
        raise Exception('Only random or file accepted as 3rd cl option.')
    data_new = parse_fixed_width_file(spec, file_fw)
    logging.info(data_new)
    ascii_data = write_to_ascii_delim(spec, file_fw, file_ad)
    logging.info(ascii_data)
    ascii_data_read = read_from_ascii_delim(spec, file_ad)
    logging.info(ascii_data_read)
