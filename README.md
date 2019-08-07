# PrePy

For use with Digitimer and Raspberry Pi. Can be used to stimulate 5V TTL pulses via Raspberry Pi. 

## Install and Local Usage

Create and activate a python3.6 virtualenv: 

### PC
```bash
python -m venv prepy_venv
prepy_venv/Scripts/activate
```

### Linux/ Mac
```bash
python -m venv prepy_venv
source prepy_venv/bin/activate # for unix/linux
```

Install in development mode: `pip install -e .`

Run PrePy:

1.`python main.py`


Please Note: for use with raspberry pi we assume the RPi.GPIO module is present. This cannot be added as a pip dependancy for local development :(
