import time
from pygame import mixer


RASPBERRY_GPIO_PIN = 12


class Stimulator:

    def __init__(self, parameters, logger):
        
        self.logger = logger
        self.blocks = parameters['number_of_blocks']
        self.rest_period = parameters['rest_period']
        self.trials = parameters['number_of_trials']

        self.stim_type = parameters['stim_type']
        self.audio_stim = parameters['audio_prestim']

        if self.audio_stim:
            mixer.init()
            mixer.music.load(parameters['audio_path'])
            self.audio_path = parameters['audio_path']
    
    def stimulate(self):
        if self.stim_type == 1:
            self.raspberry_pi_stimulation()



    def raspberry_pi_stimulation(self):
        """Raspberry PI Stimulation."""

        try:
            import RPi.GPIO as GPIO

            # setup the board and pin
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(RASPBERRY_GPIO_PIN, GPIO.OUT)
        except ImportError:
            GPIO = MockGPIO(self.logger)
            self.logger.debug('RPi.GPIO not installed')

        self.logger.info('Starting raspberry pi stimulation')
        for _ in range(self.blocks):
            for _ in range(self.trials):
                # make sure pin is off
                GPIO.output(RASPBERRY_GPIO_PIN, False)

                # play pre-stim
                if self.audio_stim:
                    mixer.music.play()
                
                # time.sleep() todo.. this wait should not be blocking

                # set pins to output trigger
                GPIO.output(RASPBERRY_GPIO_PIN, True)
            time.sleep(self.rest_period)
        self.logger.info('Finished raspberry pi stimulation')


class MockGPIO:

    def __init__(self, logger):
        self.logger = logger

    def output(self, pin, value):
        self.logger.info('output on pin {} with value {}'.format(pin, value))
