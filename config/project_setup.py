"""
Project setup
Creates the project base folder structure...
"""

import os
import re
import glob
import global_functions as gf
from pprint import pprint as pp

tasks = \
[
    'comp',
    'trk',
    'fx',
    'lgt',
    'anim',
]

shot_structure = \
    {
        '{shot_code}':
            {
                'renders': None,
                'scripts': tasks,
                'elements': None,
                'cache': None,
                'camera': None,
            }
    }

folder_config = \
    {
        '{project_name}':
            {
                'shots': shot_structure,
                'prod': None,
                'plates': None,
                'refs': None,
                'reviews': None,
                'final': None,
                'luts': None,
            }
    }


def create_shot_code_list(prefix, kwargs):
    """
    Loops through shot code scheme and creates shot code list
    :param str prefix: Project prefix
    :param dict kwargs:
    :return list:
    """

    _temp_list = []
    shot_code = '{prefix}_{:03d}_{:03d}_{:03d}'

    for key, item in kwargs.iteritems():
        for value in range(item):
            value += 1

            _shot_code = shot_code.format(101, key, value, prefix=prefix, )
            _temp_list.append(_shot_code)

    return _temp_list


if __name__ == '__main__':
    base = 'D:/VFX'
    project = 'molecules'

    shot_code_list = [
        'MC_101_001_063',
        'MC_101_001_069',
        'MC_101_001_070',
    ]

    for shot_code in shot_code_list:
        for path in gf.walk(folder_config, base):
            gf.mkdir(path.replace('\\', '/').format(project_name=project, shot_code=shot_code))