from codecs import open as codecsopen
from json import load as jsonload

def _cast_parameters(parameters: dict) -> dict:
    """Cast to Value.

    Take in a parameters dictionary and coverts to a dictionary with type converted
        and extranous information removed.
    """
    new_parameters = {}
    for key, value in parameters.items():
        new_parameters[key] = cast_value(value)

    return new_parameters


def cast_value(value):
    """Cast Value.

    Takes in a value with a desired type and attempts to cast it to that type.
    """
    actual_value = str(value['value'])
    actual_type = value['type']

    try:
        if actual_type == 'int':
            new_value = int(actual_value)
        elif actual_type == 'float':
            new_value = float(actual_value)
        elif actual_type == 'bool':
            new_value = True if actual_value == 'true' else False
        elif actual_type == 'str' or 'path' in actual_type:
            new_value = str(actual_value)
        else:
            raise ValueError('Unrecognized value type')

    except Exception:
        raise ValueError('Could not cast {} to {}'.format(actual_value, actual_type))

    return new_value


def load_json_parameters(path: str, value_cast: bool=False) -> dict:
    """Load JSON Parameters.

    Given a path to a json of parameters, convert to a dictionary and optionally
        cast the type.

    Expects the following format:
    "fake_data": {
        "value": "true",
        "section": "bci_config",
        "readableName": "Fake Data Sessions",
        "helpTip": "If true, fake data server used",
        "recommended_values": "",
        "type": "bool"
        }

    PARAMETERS
    ----------
    :param: path: string path to the parameters file.
    :param: value_case: True/False cast values to specified type.
    """
    # loads in json parameters and turns it into a dictionary
    try:
        with codecsopen(path, 'r', encoding='utf-8') as f:
            parameters = []
            try:
                parameters = jsonload(f)

                if value_cast:
                    parameters = _cast_parameters(parameters)
            except ValueError:
                raise ValueError(
                    "Parameters file is formatted incorrectly!")

        f.close()

    except IOError:
        raise IOError("Incorrect path to parameters given! Please try again.")

    return parameters
