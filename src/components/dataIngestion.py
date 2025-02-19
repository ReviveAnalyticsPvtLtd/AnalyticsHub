from src.utils.exceptions import CustomException
from src.utils.logger import logger
import datatable as dt
import io

class DataIngestion:
    def __init__(self):
        """Initializes the DataIngestion class."""
        logger.info("Initialized DataIngestion class.")

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
            logger.info("Starting code generation for reading CSV files.")
            codeString = "import datatable as dt\nimport io\n\n"
            for file in files:
                dataframeName = file["filename"][:-4]  # Remove file extension
                codeString += f"""{dataframeName} = dt.fread(io.BytesIO({file["content"]})).to_pandas()\n"""
            logger.info("Code generation for CSV files completed successfully.")
            return codeString
        except Exception as e:
            logger.error(f"Error while generating code for CSV files: {e}")
            raise CustomException(e)

    def getAttributeInfo(self, files: list[dict[str, str]]) -> str:
        """
        Extracts metadata and sample data information from the provided files.

        Args:
            files (list[dict[str, str]]): A list of dictionaries where each dictionary contains:
                - "filename" (str): The name of the file.
                - "content" (str): The file content in bytes format.

        Returns:
            str: The extracted metadata and sample data information.

        Raises:
            CustomException: If any exception occurs during metadata extraction.
        """
        try:
            logger.info("Starting attribute extraction from files.")
            attributeInfo = ""
            for file in files:
                logger.debug(f"Processing file: {file['filename']}")
                data = dt.fread(io.BytesIO(file["content"])).to_pandas()
                attributeInfo += "DATAFRAME NAME: " + file["filename"][:-4] + "\n"
                for col in data.columns:
                    attributeInfo += f"- {col} ({data[col].dtype.name}) \n"
                attributeInfo += "Shape: \n" + str(data.shape) + "\n"
                attributeInfo += "Sample row: \n" + data.head(1).to_string() + "\n\n"
            logger.info("Attribute extraction completed successfully.")
            return attributeInfo
        except Exception as e:
            logger.error(f"Error while extracting attributes: {e}")
            raise CustomException(e)