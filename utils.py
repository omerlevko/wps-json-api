import json
from constants import Constants

def parse_description(description):
    """
    Parses a description object as a json
    :param description: wps process description object
    :return: a json describing the process(its metadata)
    """
    # Deletes the property _root from the description obj,
    # for some reason the serialization fails because of it
    delattr(description, "_root")
    description_json = json.dumps(description, default=lambda o: o.__dict__)
    return json.loads(description_json)


def parse_outputs(outputs):
    """
    Parses the process outputs
    :param outputs: the process outputs
    :return: json represents the process outputs
    """
    res = {}
    for out in outputs:
        if out.dataType == Constants.COMPLEX_DATA_TYPE:
            res[out.identifier] = json.loads(out.data[0])
        else:
            res[out.identifier] = out.data[0]
    return res
