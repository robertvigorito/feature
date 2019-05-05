from shot_loader_ui import run
import nuke

m = nuke.menu('Nuke').addMenu('VFX Tools')
m.addCommand('Shot Loader', 'shot_loader.run() ', 'f1')

