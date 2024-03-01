import json

def str2bool(str_: str) -> bool:
    """
    Convert a string to a boolean value by parsing it to lower case and using the json.loads function.
    
    :param str_: The input string to be converted to a boolean.
    :return: The boolean value parsed from the input string.
    """
    
    return  json.loads(str_.lower())
