import random
import logging

logger = logging.getLogger(__name__)


def list_of_chars(spec):
    '''A function to create a list of all characters in a given encoding.'''
    list_of_chars = []
    logger.debug(f'list_of_chars={list_of_chars}')
    for i in range(2**5, 2**8):
        b = bytes([i])
        logger.debug(f'b={b}')
        try:
            c = b.decode(spec['FixedWidthEncoding'])
            # Non-printing characted in cp1252 not added to list.
            if spec['FixedWidthEncoding'] == 'windows-1252' \
               and i not in [127, 160, 173]:
                logger.debug(f'adding c={c}')
                list_of_chars.append(c)
            else:
                logger.debug(f'not adding c={c}')
                logger.info
        except UnicodeDecodeError:
            # There is a number of unassigned characters in cp1252.
            logger.info(f'No char {b} in {spec["FixedWidthEncoding"]}')
    return list_of_chars


def random_string(list_of_chars, max_len, min_len=0):
    '''
    A function to create a random string selected from the chars in
    list_of_chars of a random length between min_len and max_len.
    '''
    # We don't want short strings to be frequently empty, the probability of
    # this happening is 1/length which is, 50% for length = 1, 33% for 2, and
    # 25 % for 3. We manually fix this here.
    if min_len < 3:
        min_len = max_len
    length = random.randint(min_len, max_len)
    # We strip the strings as a hack to keep code simple.
    string = ''.join(random.choice(list_of_chars)
                     for i in range(length)).strip()
    logger.debug(f'string={string}')
    return string


def write_dummy_fixed_width(spec, file_name, n_lines):
    '''
    A function to write a random fixed width file to disk.
    And return the generating text as a list of lists.
    TODO: In future this should be implemented as a generator to deal with
    large files reasonably.
    '''
    # Read in the spec for the fixed width file.
    columns = spec['ColumnNames']
    logger.debug(f'columns={columns}')
    offsets = spec['Offsets']
    offsets = list(map(int, offsets))
    logger.debug(f'offsets={offsets}')
    encoding = spec['FixedWidthEncoding']
    logger.debug(f'encoding = {encoding}')

    # Create the printable character list.
    cp1252 = list_of_chars(spec)

    # Write the header.
    if spec['IncludeHeader'] == 'True':
        logger.info('Write header')
        string = ''.join([f'{d:<{o}}' for d, o in zip(columns, offsets)]) \
            + '\n'
        logger.debug(f'string = {string}')
        with open(file_name, 'w', encoding=encoding) as f:
            f.write(string)

    # Write random data, and create a data list of lists.
    data = []
    for i in range(n_lines):
        row = [random_string(cp1252, x-1) for x in offsets]
        logger.debug(row)
        data.append(row)
        combine = zip(row, offsets)
        strings = [f'{r:<{o}}' for r, o in combine]
        string = ''.join(strings) + '\n'
        logger.debug(string)
        with open(file_name, 'a+', encoding=encoding) as f:
            f.write(string)
    return [columns] + data


def split_string(string, offsets):
    '''
    A quick and dirty recursive function to split stings, not very efficient,
    but probably good enough for a coding test.
    '''
    if len(offsets) == 1:
        return [string.strip()]
    else:
        head = offsets.pop(0)
        return [string[:head].strip()] + split_string(string[head:], offsets)


def parse_fixed_width_file(spec, file_name):
    '''
    A function to parse a fixed width file into a list of lists.
    '''
    data = []
    encoding = spec['FixedWidthEncoding']
    with open(file_name, 'r', encoding=encoding) as f:
        for i in f:
            offsets = spec['Offsets']
            offsets = list(map(int, offsets))
            str_list = split_string(i, offsets)
            data.append(str_list)
    logger.debug(f'data={data}')
    return data


def write_to_ascii_delim(spec, from_file, to_file):
    '''
    from_file is the fixed width file from which to read the data.
    to_file is the ASCII delimited file to which to write the data.

    We use a little known ASCII delimited format which means we don't need
    to think about escaping characters when writing out.

    The full format is somewhat difficult to implement[0], but a simplified
    2 level delimited file is very straight forward.

    We again do not worry about efficiency and use a list of lists and assume
    that all second level lists have the same length.

    [0] This comes from the fact that [[a,b,c], d] and [[a,b,c], [d]] are
    equivalent for simple delimited files, e.g. in CSV both convert to:

    a,b,c
    d

    How ever for the full ASCII delimited files, with 4 separators we have:

    1). [[a,b,c], d]
    2). [[a,b,c], [d]]
    3). [[a,b,c], [[d]]]
    4). [[a,b,c], [[[d]]]]

    All being separate and unique serializations. Happy for further
    explanation in person / over the phone.

    Further reading:
    https://en.wikipedia.org/wiki/Delimiter#ASCII_delimited_text
    '''
    unit_sep = chr(31)
    record_sep = chr(30)
    data = parse_fixed_width_file(spec, from_file)
    # We use a dirty hack to remove the last deliminator from each line since
    # strings in python are immutable.
    data_and_delim = []
    for row in data:
        for item in row:
            data_and_delim += [item] + [unit_sep]
        data_and_delim[-1] = record_sep
    string = ''.join(data_and_delim[:-1])
    with open(to_file, 'w') as f:
        f.write(string)
    logger.debug(string)
    return data


def read_from_ascii_delim(spec, from_file):
    '''
    from_file is the ASCII delimited file from which to read in the data.
    A function to turn an ASCII delimited 2 level file into a list of lists.
    This is not a full parser for ASCII delimited text, which has 4 separators
    but is a quick hack for what we need here.

    Further reading:
    https://en.wikipedia.org/wiki/Delimiter#ASCII_delimited_text
    '''
    # Assume that we only have unit and record separators.
    unit_sep = chr(31)
    record_sep = chr(30)

    with open(from_file, 'r') as f:
        data = f.read()
    # Split on record separator.
    rows = data.split(record_sep)
    logger.debug(rows)
    ret_data = []
    # Split on unit separator in each row.
    for row in rows:
        ret_data.append(row.split(unit_sep))

    logger.debug(ret_data)
    return ret_data
