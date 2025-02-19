from src.components.queryChainBuilder import QueryChainBuilder
from langchain_experimental.utilities import PythonREPL
from src.components.codeGenerator import CodeGenerator
from src.components.dataIngestion import DataIngestion
from src.utils.exceptions import CustomException
from src.utils.logger import logger
import json

class CompletePipeline:
    def __init__(self):
        """Initializes the CompletePipeline class, setting up components for data ingestion, query handling, and code generation."""
        logger.info("Initializing CompletePipeline components.")
        self.pythonRepl = PythonREPL()
        self.dataIngestion = DataIngestion()
        self.queryChainBuilder = QueryChainBuilder()
        self.codeGenerator = CodeGenerator()

    def loadData(self, inputData: list[dict[str, str]], domainContext: str) -> None:
        """
        Loads data from the provided input, processes it, and initializes the query processing chain.

        Args:
            inputData (list[dict[str, str]]): A list of dictionaries containing input data files.
            domainContext (str): The context for the domain in which the data is applied.

        Raises:
            CustomException: If an error occurs during data loading or processing.
        """
        try:
            logger.info("Loading data and initializing pipeline.")
            codeString = self.dataIngestion.dataLoadString(files=inputData)
            replOutput = self.pythonRepl.run(codeString)

            if replOutput:
                raise CustomException(e)
            logger.info("Data loaded successfully.")

            attributeInfo = self.dataIngestion.getAttributeInfo(files=inputData)
            self.domainContext = domainContext
            self.chain = self.queryChainBuilder.getChain()
            metadata = self.queryChainBuilder.getMetadataChain().invoke({"metadata": attributeInfo})
            metadataParts = metadata.split("```")
            metadata = metadataParts[-2]
            metadata = "\n".join(metadata.split("\n")[1:]) 
            self.metadata = json.loads(metadata)
            logger.info("Pipeline initialized successfully.")
        except Exception as e:
            logger.error(f"Error during loadData: {e}")
            raise CustomException(e)

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
        try:
            logger.info(f"Generating graph for query: {query}")
            code = self.codeGenerator.generateCode(
                chain=self.chain,
                userQuery=query,
                domainContext=self.domainContext,
                metadata=self.metadata
            )
            filename, refinedCode = self.codeGenerator.codeRefiner(codeBlock=code)
            logger.info(f"Graph generated successfully. File saved as {filename}.")
            return filename, refinedCode
        except Exception as e:
            logger.error(f"Error during generateGraph: {e}")
            raise CustomException(e)