import global_functions as gf
import os
import glob

shot_code = 'AD_101_007_015'

project = 'ambers_descent'
project_dir = 'D:/vfx/projects'

comp_dir, plates_dir = list(gf.find('comp', 'plates'))
script_name = shot_code + '_comp_v001.nk'

comp_script_name = os.path.join(project_dir, comp_dir.format(project_name=project, shot_code=shot_code),
                                script_name).replace('\\', '/')
plates_dir = os.path.join(project_dir, plates_dir.format(project_name=project), '{}*'.format(shot_code))

for path in glob.glob(plates_dir):
    read = nuke.nodes.Read()
    read['file'].fromUserText(path)

format = nuke.addFormat('3840 1640 AD')
nuke.Root()['format'].setValue(format)

nuke.Root()['fps'].setValue(23.97)

nuke.scriptSaveAs(comp_script_name)