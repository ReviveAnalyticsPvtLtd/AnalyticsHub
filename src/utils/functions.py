import yaml
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