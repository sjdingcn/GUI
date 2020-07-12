import json
import shutil
from pathlib import Path

from PyQt5.QtWidgets import QDialog, QFileDialog, QButtonGroup

from create_project_scene import Ui_Dialog
from utils import gui_root, warning_msg_box


class CreateProjectDialog(QDialog, Ui_Dialog):

    def __init__(self):
        super(CreateProjectDialog, self).__init__()
        self.setupUi(self)
        self.line_edit_location.setText('/path/to/untitled/')
        self.tool_button_location.clicked.connect(self.project_location_handler)
        self.radio_button_group = QButtonGroup(self.group_box)
        self.radio_button_group.setExclusive(True)
        self.radio_button_default.setChecked(True)
        self.line_edit_virtual.setEnabled(False)
        self.radio_button_virtual.toggled.connect(lambda i: self.line_edit_virtual.setEnabled(i))

    def project_location_handler(self):
        file = str(QFileDialog.getExistingDirectory(self, "Select Base Directory"))
        self.line_edit_location.setText(file)

    def accept(self):
        try:
            if any(True for _ in Path(self.line_edit_location.text()).iterdir()):
                print("Directory is not empty")
                warning_msg_box(self, "The directory is not empty. Please select an empty directory.", "")

            else:
                project_dir = Path(self.line_edit_location.text())
                project_dir.mkdir(parents=True, exist_ok=True)
                model_dir = gui_root() / 'stock'
                model_dir.mkdir(parents=True, exist_ok=True)

                Path(project_dir, 'label').mkdir(parents=True, exist_ok=True)
                Path(project_dir, 'data').mkdir(parents=True, exist_ok=True)
                Path(project_dir, 'data', 'train').mkdir(parents=True, exist_ok=True)
                Path(project_dir, 'data', 'val').mkdir(parents=True, exist_ok=True)
                Path(project_dir, 'data', 'test').mkdir(parents=True, exist_ok=True)
                Path(project_dir, 'logs').mkdir(parents=True, exist_ok=True)
                shutil.copy2(Path(gui_root(), 'src', 'train_config.py'), project_dir)
                shutil.copy2(Path(gui_root(), 'src', 'inspect_data.ipynb'), project_dir)
                shutil.copy2(Path(gui_root(), 'src', 'inspect_model.ipynb'), project_dir)

                data = {}
                with open(Path(project_dir, 'project.json'), 'w') as outfile:
                    json.dump(data, outfile)
                from main_scene_controller import MainScene
                application = MainScene(project_dir, model_dir)
                if self.line_edit_virtual.text():
                    application.environment = self.line_edit_virtual.text()
                    with open(Path(self.project_dir, 'project.json'), 'w') as outfile:
                        self.project_json['environment'] = self.line_edit_virtual.text()
                        json.dump(self.project_json, outfile)
                application.show()
                # close the dialog.
                self.done(1)

        except FileNotFoundError:
            print("No such or directory: " + self.line_edit_location.text())
            warning_msg_box(self, "No such or directory: '" + self.line_edit_location.text() + "'",
                            "Please select an existing directory.")
