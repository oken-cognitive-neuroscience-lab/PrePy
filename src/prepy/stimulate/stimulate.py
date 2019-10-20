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
        self.dual_stim = parameters['dual_stim']
        self.inter_stim_period = parameters['inter_stim_period']
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

        # keep track of blocks/trials
        num_blocks = self.blocks - 1
        num_trials = self.trials - 1

        # Loop over blocks [trials + rest period]
        for block in range(self.blocks):

            # Loop over trials [audio pre stim (optional) + trigger]
            for trial in range(self.trials):
                # make sure pin is off
                GPIO.output(RASPBERRY_GPIO_PIN, False)

                # play pre-stim
                if self.audio_stim:
                    self.logger.debug('Playing audio pre stim')
                    mixer.music.play()

                    self.logger.debug('Sleeping for intra trial period {}'.format(self.intra_trial_period))
                    # sleep for intra trial period
                    time.sleep(self.intra_trial_period)

                # set pins to output trigger
                GPIO.output(RASPBERRY_GPIO_PIN, True)

                if self.dual_stim:
                    GPIO.output(RASPBERRY_GPIO_PIN, False)

                    self.logger.debug('Sleeping for inter stimuli period {}'.format(self.inter_stim_period))
                    time.sleep(self.inter_stim_period)
                    
                    GPIO.output(RASPBERRY_GPIO_PIN, True)

                self.logger.debug('Sleeping for inter trial period {}'.format(self.inter_trial_period))
                
                # If this is not the last trial, sleep for the inter trial period
                if trial != num_trials:
                    time.sleep(self.inter_trial_period)

            # If this is not the last block, sleep for the rest period
            if block != num_blocks:
                self.logger.debug('Trail Complete: sleeping for rest period {}'.format(self.rest_period))
                time.sleep(self.rest_period)
        self.logger.info('Finished raspberry pi stimulation')


class MockGPIO:
    """Mock GPIO.

    For testing when GPIO module cannot be installed.
    """

    def __init__(self, logger):
        self.logger = logger

    def output(self, pin, value):
        if value:
            self.logger.debug('Setting [{}] pin to true'.format(pin))
        else:
            self.logger.debug('Setting [{}] pin to false'.format(pin))
