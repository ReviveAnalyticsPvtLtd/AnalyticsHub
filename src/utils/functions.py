import yaml
import json
import configparser

def readYaml(filePath: str) -> dict:
    """
    Reads a YAML file and returns its content as a dictionary.

    Args:
        filePath (str): The path to the YAML file to be read.

    Returns:
        dict: The content of the YAML file as a dictionary.
    """
    with open(filePath, "r") as f:
        content = yaml.safe_load(f)
    return content 

def getConfig(path: str) -> dict:
    """
    Reads a configuration file and returns its content as a dictionary.

    Args:
        path (str): The path to the configuration file.

    Returns:
        dict: The content of the configuration file.
    """
    config = configparser.ConfigParser()
    config.read(path)
    return config

def validateJson(string: str) -> str:
    """
    Validates if a given string is a valid JSON.

    This function attempts to parse the input string as JSON using `json.loads()`. 
    If the string is valid JSON, the function returns `None`. If not, it returns 
    an error message indicating that the string is not valid JSON.

    Args:
        string (str): The JSON string to be validated.

    Returns:
        str: An error message ("Not a valid json") if the string is invalid JSON,
             or `None` if the string is valid JSON.
    """
    try:
        json.loads(string)
        return None
    except:
        return "Invalid Json"