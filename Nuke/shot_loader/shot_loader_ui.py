try:
    from PySide2.QtGui import *
    from PySide2.QtCore import *
    from PySide2.QtWidgets import *

except ImportError:
    from PySide.QtCore import *
    from PySide.QtGui import *

import subprocess
import global_functions as gf
import sys
import os
import glob

BASE = 'D:/VFX/projects'
CMD = '"C:\Program Files\Nuke11.3v2\Nuke11.3.exe" --nukex'

PREF = os.path.join(os.path.dirname(__file__), 'pref.json')


class ShotLoader(QDialog):

    def __init__(self):
        super(ShotLoader, self).__init__(parent=QApplication.activeWindow())

        self.setLayout(self.master_layout())
        self.resize(600, 500)

        try:
            self.set_preference()
        except (IOError, ValueError):
            pass

    def splitter_1(self):
        """
        Creating the three window list widget, displaying project, shots, comp scripts...

        """

        self.project_display = QListWidget()

        _projects = list(self.get_projects())
        self.project_display.addItems(_projects)
        self.project_display.itemClicked.connect(self.get_shot_list)

        self.shots_display = QListWidget()
        self.shots_display.itemClicked.connect(self.get_comp_list)

        self.comp_scripts_display = QListWidget()
        self.comp_scripts_display.itemDoubleClicked.connect(self.open_comp_script)

        splitter = QSplitter()

        splitter.addWidget(self.project_display)
        splitter.addWidget(self.shots_display)
        splitter.addWidget(self.comp_scripts_display)
        splitter.setSizes([150, 150, 250])

        return splitter

    def master_layout(self):
        """
        Creating the master layout, which combines all layouts...

        """

        master_layout = QVBoxLayout()

        master_layout.addWidget(self.splitter_1())

        return master_layout

    def open_comp_script(self, item):
        """
        Open comp script...

        """

        comp = item.text()

        comp_file_path = os.path.abspath(os.path.join(self.comp_dir, comp))
        cmd = ' '.join([CMD, comp_file_path])

        subprocess.Popen(cmd, shell=True)
        self.save_preference()
        self.close()

        return True

    def get_comp_list(self, item):
        """
        Adds the project shot list to list widget...

        :param item:
        :return:
        """

        self.shot_code = item.text()
        self.comp_scripts_display.clear()

        self.comp_dir = gf.find('comp').next().format(project_name=self.project_name, shot_code=self.shot_code)
        self.comp_dir = os.path.join(BASE, self.comp_dir)

        for script in os.listdir(self.comp_dir):
            if not script.endswith('nk'):
                continue

            self.comp_scripts_display.addItem(script)

        return True

    def get_shot_list(self, item):
        """
        Adds the project shot list to list widget...

        :param item:
        :return:
        """

        self.project_name = item.text()
        self.shots_display.clear()

        shot_directory = gf.find('shots').next().format(project_name=self.project_name)
        shot_directory = os.path.join(BASE, shot_directory)

        for shot in os.listdir(shot_directory):
            path = os.path.join(shot_directory, shot)

            if not os.path.isdir(path):
                continue

            self.shots_display.addItem(shot)

        return True

    @staticmethod
    def get_projects():
        """
        Find project names...

        """

        glob_exp = BASE + '/*'

        for path in glob.glob(glob_exp):
            if not os.path.isdir(path):
                continue

            basename = os.path.basename(path)
            yield basename

    def save_preference(self):
        """
        Saving preferences to json file...

        """

        data = [self.project_name, self.shot_code]
        gf.json_write(PREF, data)

        return True

    def set_preference(self):
        """
        Set the shot loader preference...

        """

        project, shot_code = gf.json_read(PREF)

        item = self.project_display.findItems(project, Qt.MatchExactly)[0]
        self.project_display.setCurrentItem(item)
        self.get_shot_list(item)

        item = self.shots_display.findItems(shot_code, Qt.MatchExactly)[0]
        self.shots_display.setCurrentItem(item)
        self.get_comp_list(item)

        return True

def run():
    """
    nuke run...

    """

    for app in qApp.allWidgets():
        if type(app).__name__ == 'ShotLoader':
            app.close()

    shot_loader = ShotLoader()
    shot_loader.show()

    return True

if __name__ == '__main__':
    app = QApplication(sys.argv)
    shot_loader = ShotLoader()
    shot_loader.show()
    sys.exit(app.exec_())