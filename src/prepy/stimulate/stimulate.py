import time
from pygame import mixer


RASPBERRY_GPIO_PIN = 12


class Stimulator:
    """Stimulator.

    Main stimulation logic for PrePy. Current implemention for stimulation includes:
            - Raspberry Pi
    """

    def __init__(self, parameters, logger):
        self.logger = logger

        self.blocks = parameters['number_of_blocks']
        self.rest_period = parameters['rest_period']
        self.trials = parameters['number_of_trials']
        self.inter_trial_period = parameters['inter_trial_period']

        self.stim_type = parameters['stim_type']
        self.audio_stim = parameters['audio_prestim']
        self.intra_trial_period = parameters['intra_trial_period']

        if self.audio_stim:
            mixer.init()
            mixer.music.load(parameters['audio_path'])
            self.audio_path = parameters['audio_path']

    def stimulate(self):
        """Stimulate."""
        if self.stim_type == 1:
            self.raspberry_pi_stimulation()

    def raspberry_pi_stimulation(self):
        """Raspberry PI Stimulation."""
        try:
            import RPi.GPIO as GPIO

            # setup the board and pin
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(RASPBERRY_GPIO_PIN, GPIO.OUT)
            GPIO.output(RASPBERRY_GPIO_PIN, False)

        except ImportError:
            GPIO = MockGPIO(self.logger)
            self.logger.debug('RPi.GPIO not installed')

        self.logger.info('Starting raspberry pi stimulation')

        num_blocks = self.blocks - 1
        index = 0
        # Loop over blocks [trials + rest period]
        for block in range(self.blocks):

            # Loop over trials [audio pre stim + trigger]
            for _ in range(self.trials):
                # make sure pin is off
                self.logger.debug('Setting PIN {} to False'.format(RASPBERRY_GPIO_PIN))
                GPIO.output(RASPBERRY_GPIO_PIN, False)

                # play pre-stim
                if self.audio_stim:
                    self.logger.debug('Playing audio pre stim')
                    mixer.music.play()

                    self.logger.debug('Sleeping for intra trial period {}'.format(self.intra_trial_period))
                    # sleep for intra trial period
                    time.sleep(self.intra_trial_period)

                self.logger.debug('Setting PIN {} to TRUE'.format(RASPBERRY_GPIO_PIN))
                # set pins to output trigger
                GPIO.output(RASPBERRY_GPIO_PIN, True)

                self.logger.debug('Sleeping for inter trial period {}'.format(self.inter_trial_period))
                # sleep for inter trial period
                time.sleep(self.inter_trial_period)

            # if this is the last block, skip the rest period
            if block == num_blocks:
                pass
            else:
                self.logger.debug('Trail Complete: sleeping for rest period {}'.format(self.rest_period))
                time.sleep(self.rest_period)
                index += 1
        self.logger.info('Finished raspberry pi stimulation')


class MockGPIO:

    def __init__(self, logger):
        self.logger = logger

    def output(self, pin, value):
        pass
