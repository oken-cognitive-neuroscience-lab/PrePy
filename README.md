# PrePy

For use with Digitimer and Raspberry Pi. Can be used to stimulate 5V TTL pulses via Raspberry Pi. 

## Install and Local Usage

Create and activate a python3.6 virtualenv: 

```bash
python3 -m venv prepy_venv
source prepy_venv/bin/activate # for unix/linux
prepy_venv/Scripts/activate # for pc
```

Install requirements in virtualenv: `pip install -r requirements.txt`

Run PrePy:
1.`python main.py`


Please Note: for use with raspberry pi we assume the RPi.GPIO module is present. This cannot be added as a pip dependancy for local development :(
