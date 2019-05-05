import os
import re
import glob
import json


def json_write(json_file_path, data):
    with open(json_file_path, 'w') as open_json_file:
        json.dump(data, open_json_file, indent=4)
    return True


def json_read(json_file_path):
    with open(json_file_path, 'r') as open_json_file:
        data = json.load(open_json_file)
    return data


def mkdir(directory):
    """
    Make folder directory...

    :param str directory:
    :return:
    """

    try:
        os.makedirs(directory)
    except WindowsError:
        pass

    return True


def split_shot_code(shot_code):
    """
    Split the shot code...

    :param str shot_code:
    :return list:
    """

    pattern = r'(?i)([a-z\d]+)'

    return re.findall(pattern=pattern, string=shot_code)


def walk(my_dict=dict, base=''):
    """
    Run through a dictionary folder scheme and return a joined path...

    :param dict my_dict:
    :param str base:
    :return generator:
    """
    for key, item in my_dict.iteritems():
        _key = os.path.join(base, key)

        yield _key

        if isinstance(item, dict):
            for v in walk(item, _key):
                yield v

        elif isinstance(item, list):
            for v in item:
                yield os.path.join(_key, v)


def find(*args):
    """
    Find the path of listed args...

    :param args:
    :return:
    """

    import config

    for path in walk(config.folder_config):
        for key in args:
            if key in path:
                yield path



if __name__ == '__main__':
    print list(find('renders', 'comp'))