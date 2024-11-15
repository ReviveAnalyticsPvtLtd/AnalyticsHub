from src.components.queryChainBuilder import QueryChainBuilder
from langchain_experimental.utilities import PythonREPL
from src.components.codeGenerator import CodeGenerator
from src.components.dataIngestion import DataIngestion
from src.utils.exceptions import CustomException
from src.utils.logger import logger

class CompletePipeline:
    def __init__(self):
        """Initializes the CompletePipeline class, setting up components for data ingestion, query handling, and code generation."""
        self.pythonRepl = PythonREPL()
        self.dataIngestion = DataIngestion()
        self.queryChainBuilder = QueryChainBuilder()
        self.codeGenerator = CodeGenerator()

    def loadData(self, inputData: list[dict[str, str]], metadata: bytes, domainContext: str) -> None:
        """
        Loads data from the provided input, processes it, and initializes the query processing chain.

        Args:
            inputData (list[dict[str, str]]): A list of dictionaries containing input data files.
            metadata (bytes): The metadata in bytes format.
            domainContext (str): The context for the domain in which the data is applied.

        Raises:
            CustomException: If an error occurs during data loading or processing.
        """
        try:
            codeString = self.dataIngestion.dataLoadString(files=inputData)
            message = self.pythonRepl.run(codeString)
            if message == "":
                logger.info("Data loaded successfully.")
            else:
                raise CustomException(message)
            self.domainContext = domainContext
            self.metadata = self.dataIngestion.readMetadata(fileContent=metadata)
            self.chain = self.queryChainBuilder.getChain()
        except Exception as e:
            logger.error(e)
            print(CustomException(e))

    def generateGraph(self, query: str) -> tuple[str]:
        """
        Generates a graph based on the provided query by invoking the processing chain.

        Args:
            query (str): The user's query to generate the graph.

        Returns:
            tuple[str]: A tuple containing the filename and the refined code for the graph.

        Raises:
            CustomException: If an error occurs during graph generation.
        """
        code = self.codeGenerator.generateCode(
            chain=self.chain,
            userQuery=query,
            domainContext=self.domainContext,
            metadata=self.metadata
        )
        return self.codeGenerator.codeRefiner(codeBlock=code)