import os
import sys
import json
from time import localtime, strftime
import logging

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QAction,
    QLabel,
    QLineEdit,
    QMessageBox,
    QGridLayout,
    QSpinBox,
    QDoubleSpinBox,
    QMessageBox)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

from prepy.util import load_json_parameters
from prepy.config import PARAMETER_PATH
from prepy.stimulate.stimulate import raspberry_pi_stimulation


class PrePy(QWidget):
    """GUI for PrePy."""

    title = 'PrePy Software'

    def __init__(self):
        super().__init__()

        logging.basicConfig(
            level=logging.INFO,
            format='%(name)s - %(levelname)s - %(message)s')
        self.logger = logging
        self.parameters = self.get_initial_parameters(PARAMETER_PATH)

        self.left = 50
        self.top = 50
        self.width = 300
        self.height = 300

        self.grid = QGridLayout()
        self.grid.setSpacing(2)

        self.init_ui()

    def init_ui(self):
        """Init UI."""
        # main window setup
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # inputs and buttons
        self.create_inputs()
        self.create_buttons()
        self.setLayout(self.grid)

        # show the window
        self.show()

    @pyqtSlot()
    def on_stimulate(self):
        """Register on click events."""
        self.logger.info(
            f'Starting experiment for user=[{self.user_textbox.text()}]'
            f' with trials=[{self.trial_number_input.text()}]')
        self.stimulate()

    def stimulate(self):
        """Stimuluate."""
        self.write_sessions()
        qm = QMessageBox
        qm.question(self, 'PrePy Start Stimulation', 'Ready to start?', qm.Yes | qm.No)
        if qm.Yes:
            raspberry_pi_stimulation(self.parameters, self.logger)
            self.logger.info('Stimulate not registered')
        else:
            self.logger.info('No Stimulation')

    def write_sessions(self):
        """Write Sessions.

        TODO: write parameters
        """
        self.compile_parameters()

        user_information = self.user_textbox.text()
        save_folder_name = f'data/{user_information}/'

        save_directory = save_folder_name + user_information + '_' + strftime(
            '%a_%d_%b_%Y_%Hhr%Mmin%Ssec_%z', localtime())

        try:
            # make the directory
            os.makedirs(save_directory)

            # save the parameters
            with open(f'{save_directory}/parameters.json', 'w') as parameter_file:
                json.dump(self.parameters, parameter_file)
        except FileExistsError:
            pass

    def compile_parameters(self):
        """Compile Parameters."""
        self.parameters['user_id'] = self.user_textbox.text()
        self.parameters['number_of_trials'] = self.trial_number_input.text()
        self.parameters['inter_trial_period'] = self.inter_trial_input.text()
        self.parameters['number_of_blocks'] = self.block_number_input.text()
        self.parameters['rest_period'] = self.rest_period_input.text()

    def get_initial_parameters(self, path):
        """Get Initial Parameters."""
        return load_json_parameters(path, value_cast=True)

    def create_buttons(self):
        """Create Buttons."""
        self.start_button = QPushButton('Begin Stimulation', self)
        self.start_button.clicked.connect(self.on_stimulate)

        self.grid.addWidget(self.start_button)

    def create_inputs(self):
        """Create Text Boxes."""
        label = QLabel('User ID', self)
        self.user_textbox = QLineEdit(self)
        self.user_textbox.setText(self.parameters['user_id'])
        self.user_textbox.resize(100, 25)
        self.grid.addWidget(self.user_textbox, 1, 0)
        self.grid.addWidget(label, 1, 1)

        label = QLabel('Number of Trials', self)
        self.trial_number_input = QSpinBox(self)
        self.trial_number_input.setValue(self.parameters['number_of_trials'])
        self.trial_number_input.resize(100, 25)
        self.grid.addWidget(self.trial_number_input, 2, 0)
        self.grid.addWidget(label, 2, 1)

        label = QLabel('Inter-Trial Period', self)
        self.inter_trial_input = QDoubleSpinBox(self)
        self.inter_trial_input.setValue(self.parameters['inter_trial_period'])
        self.inter_trial_input.resize(100, 25)
        self.grid.addWidget(self.inter_trial_input, 3, 0)
        self.grid.addWidget(label, 3, 1)

        label = QLabel('Number of Blocks', self)
        self.block_number_input = QSpinBox(self)
        self.block_number_input.setValue(self.parameters['number_of_blocks'])
        self.block_number_input.resize(100, 25)
        self.grid.addWidget(self.block_number_input, 4, 0)
        self.grid.addWidget(label, 4, 1)


        label = QLabel('Rest Period', self)
        self.rest_period_input = QDoubleSpinBox(self)
        self.rest_period_input.setValue(self.parameters['rest_period'])
        self.rest_period_input.resize(100, 25)
        self.grid.addWidget(self.rest_period_input, 5, 0)
        self.grid.addWidget(label, 5, 1)


def app(args):
    """Main app registry. Passes args from main and intilizes the app"""
    return QApplication(args)
