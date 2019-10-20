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
from prepy.stimulate.stimulate import Stimulator


class PrePy(QWidget):
    """GUI for PrePy."""

    title = 'PrePy Software'

    def __init__(self):
        super().__init__()

        logging.basicConfig(
            level=logging.DEBUG,
            format='%(name)s - %(levelname)s - %(message)s')
        self.logger = logging
        self.parameters = self.get_initial_parameters(PARAMETER_PATH)

        self.left = 50
        self.top = 50
        self.width = 400
        self.height = 400

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
            'Starting experiment for user=[{}]'
            ' with blocks=[{}]'.format(
                self.user_textbox.text(),
                self.block_number_input.text()))
        self.stimulate()

    def stimulate(self):
        """Stimulate."""
        qm = QMessageBox
        response = qm.question(self, 'PrePy Start Stimulation', 'Ready to start?', qm.Yes | qm.No)

        if response == qm.Yes:
            self.write_sessions()

            self.stimulator = Stimulator(self.parameters, self.logger)
            self.stimulator.stimulate()

            qm.information(self, 'PrePy Finished Stimulation', 'Experiment Finished!')
        else:
            self.logger.info('Not starting stimulation')

    def write_sessions(self):
        """Write Sessions.

        Compiles parameters from inputs and writes them to a session folder.
        """
        self.compile_parameters()

        user_information = self.user_textbox.text()
        save_folder_name = 'data/{}/'.format(user_information)

        save_directory = save_folder_name + user_information + '_' + strftime(
            '%a_%d_%b_%Y_%Hhr%Mmin%Ssec_%z', localtime())

        try:
            # make the directory
            os.makedirs(save_directory)

            # save the parameters
            with open('{}/parameters.json'.format(save_directory), 'w') as parameter_file:
                json.dump(self.parameters, parameter_file)
        except FileExistsError:
            pass

    def compile_parameters(self):
        """Compile Parameters.

        Retrieves and sets parameters from input fields.
        """
        self.parameters['user_id'] = self.user_textbox.text()
        self.parameters['number_of_trials'] = int(self.trial_number_input.text())
        self.parameters['inter_trial_period'] = float(self.inter_trial_input.text())
        self.parameters['intra_trial_period'] = float(self.intra_trial_input.text())
        self.parameters['number_of_blocks'] = int(self.block_number_input.text())
        self.parameters['rest_period'] = float(self.rest_period_input.text())
        self.parameters['inter_stim_period'] = float(self.inter_stim_period.text())
        self.parameters['stim_intensity'] = float(self.stim_intensity.text())

    def get_initial_parameters(self, path):
        """Get Initial Parameters.

        Load and cast parameters from json parameters path provided.
        """
        return load_json_parameters(path, value_cast=True)

    def create_buttons(self):
        """Create Buttons."""
        self.start_button = QPushButton('Begin Stimulation', self)
        self.start_button.clicked.connect(self.on_stimulate)

        self.grid.addWidget(self.start_button)

    def create_inputs(self):
        """Create Input Boxes."""
        label = QLabel('User ID', self)
        self.user_textbox = QLineEdit(self)
        self.user_textbox.setText(self.parameters['user_id'])
        self.user_textbox.resize(100, 25)
        self.grid.addWidget(self.user_textbox, 1, 0)
        self.grid.addWidget(label, 1, 1)

        label = QLabel('Blocks', self)
        self.block_number_input = QSpinBox(self)
        self.block_number_input.setValue(self.parameters['number_of_blocks'])
        self.block_number_input.resize(100, 25)
        self.grid.addWidget(self.block_number_input, 2, 0)
        self.grid.addWidget(label, 2, 1)

        label = QLabel('Trials', self)
        self.trial_number_input = QSpinBox(self)
        self.trial_number_input.setValue(self.parameters['number_of_trials'])
        self.trial_number_input.resize(100, 25)
        self.grid.addWidget(self.trial_number_input, 3, 0)
        self.grid.addWidget(label, 3, 1)

        label = QLabel('Inter-Trial Period (s)', self)
        self.inter_trial_input = QDoubleSpinBox(self)
        self.inter_trial_input.setMaximum(100000)
        self.inter_trial_input.setValue(self.parameters['inter_trial_period'])
        self.inter_trial_input.resize(100, 25)
        self.grid.addWidget(self.inter_trial_input, 4, 0)
        self.grid.addWidget(label, 4, 1)

        label = QLabel('Intra-Trial Period (s)', self)
        self.intra_trial_input = QDoubleSpinBox(self)
        self.intra_trial_input.setMaximum(100000)
        self.intra_trial_input.setValue(self.parameters['intra_trial_period'])
        self.intra_trial_input.resize(100, 25)
        self.grid.addWidget(self.intra_trial_input, 5, 0)
        self.grid.addWidget(label, 5, 1)

        label = QLabel('Rest Period (s)', self)
        self.rest_period_input = QDoubleSpinBox(self)
        self.rest_period_input.setMaximum(100000)
        self.rest_period_input.setValue(self.parameters['rest_period'])
        self.rest_period_input.resize(100, 25)
        self.grid.addWidget(self.rest_period_input, 6, 0)
        self.grid.addWidget(label, 6, 1)

        label = QLabel('Inter-Stimuli Period (s)', self)
        self.inter_stim_period = QDoubleSpinBox(self)
        self.inter_stim_period.setMaximum(100000)
        self.inter_stim_period.setValue(self.parameters['inter_stim_period'])
        self.inter_stim_period.resize(100, 25)
        self.grid.addWidget(self.inter_stim_period, 7, 0)
        self.grid.addWidget(label, 7, 1)

        label = QLabel('Stimuli Intensity (mA) *set externally', self)
        self.stim_intensity = QDoubleSpinBox(self)
        self.stim_intensity.setMaximum(100000)
        self.stim_intensity.setValue(self.parameters['stim_intensity'])
        self.stim_intensity.resize(100, 25)
        self.grid.addWidget(self.stim_intensity, 8, 0)
        self.grid.addWidget(label, 8, 1)


def app(args):
    """Main app registry.

    Passes args from main and initializes the app
    """
    return QApplication(args)
