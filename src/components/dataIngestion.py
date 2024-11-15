from src.utils.exceptions import CustomException
from src.utils.logger import logger
import json
import io

class DataIngestion:
    def __init__(self):
        """Initializes the DataIngestion class."""
        pass

    def dataLoadString(self, files: list[dict[str, str]]) -> str:
        """
        Generates Python code as a string to read CSV files from the provided list of file information.

        Args:
            files (list[dict[str, str]]): A list of dictionaries where each dictionary contains:
                - "filename" (str): The name of the CSV file.
                - "content" (str): The CSV file content in bytes format.

        Returns:
            str: The generated Python code as a string to read the CSV files.

        Raises:
            CustomException: If any exception occurs during code generation.
        """
        try:
            logger.info("Generating code to read the input CSV files.")
            codeString = "import pandas as pd\nimport io\n\n"
            for file in files:
                dataframeName = file["filename"][:-4]  # Remove file extension
                codeString += f"""{dataframeName} = pd.read_csv(io.BytesIO({file["content"]}))\n"""
            return codeString
        except Exception as e:
            logger.error(CustomException(e))
            print(CustomException(e))

    def readMetadata(self, fileContent: bytes) -> dict:
        """
        Reads JSON metadata from the given file content in bytes.

        Args:
            fileContent (bytes): The JSON file content in bytes format.

        Returns:
            dict: The parsed metadata from the JSON file.

        Raises:
            CustomException: If any exception occurs during JSON parsing.
        """
        try:
            metadata = json.load(io.BytesIO(fileContent))
            return metadata
        except Exception as e:
            logger.error(CustomException(e))
            print(CustomException(e))