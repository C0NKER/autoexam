#!/usr/bin/python3
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import uic
from exam_wizard import ExamWizard
from os import mkdir, environ, chdir
from os import system as run
from os.path import join, exists, abspath
import api, jinja2

DEFAULT_PROJECT_FILENAME = '.autoexam_project'
DEFAULT_PROJECT_PATH = join(environ['HOME'], 'autoexam_projects')
DEFAULT_PROJECT_FOLDER_NAME = 'Project %d'

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.ui = uic.loadUi("./ui/main_window.ui", self)
        self.ui.clbNewExam.clicked.connect(self.newExam)
        self.ui.clbLoadExam.clicked.connect(self.loadExam)
        self.ui.tabWidget.tabCloseRequested.connect(self.ui.tabWidget.removeTab)

    def setExistingDirectory(self):
        if not exists(DEFAULT_PROJECT_PATH):
            mkdir(DEFAULT_PROJECT_PATH)

        options = QFileDialog.DontResolveSymlinks | QFileDialog.ShowDirsOnly
        directory = QFileDialog.getExistingDirectory(self,
                "Project", DEFAULT_PROJECT_PATH, options)
        return directory

    def startWizard(self):
        page = ExamWizard(self.project)

        name = self.project.name

        self.ui.tabWidget.addTab(page, name)
        self.ui.tabWidget.setCurrentWidget(page)

        finish_button = page.button(QWizard.FinishButton)
        finish_button.clicked.connect(lambda: self.ui.tabWidget.removeTab(self.ui.tabWidget.currentIndex()))


    def newExam(self):
        directory = abspath(str(self.setExistingDirectory()))
        if directory:
            # Logic + UI

            project_count = 1

            while exists(join(directory, DEFAULT_PROJECT_FOLDER_NAME%project_count)):
                project_count += 1

            name = DEFAULT_PROJECT_FOLDER_NAME%project_count

            __project_path__ = join(directory, name)

            # TODO: Fix project creation
            self.project = Project(name, 0, [], [])

            # Invoke Autoexam
            api.set_project_path(__project_path__)
            api.init(name, __project_path__)

            dump_project(self.project, '%s'%join(__project_path__, DEFAULT_PROJECT_FILENAME))

            self.startWizard()

    def loadExam(self):
        directory = str(self.setExistingDirectory())
        
        if directory:
            __project_file_path__ = join(directory, DEFAULT_PROJECT_FILENAME)
            if not exists(__project_file_path__):
                self.project = None
                # print("No project found!!")
                # TODO: QDialog
                return
            else:
                self.project = load_project(__project_file_path__)

            api.set_project_path(directory)
            self.startWizard()

def getProject():    
    t1 = Tag('t1', 3)
    a1 = Answer(True, False, 'anstxt')
    q1 = Question('a', ['t1'], 'qtxt', [a1, a1])
    p1 = Project('p1', 2, [t1], [q1, q1])
    return p1

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    win = MainWindow()

    from model import *

    win.show() #Maximized
    sys.exit(app.exec_())
