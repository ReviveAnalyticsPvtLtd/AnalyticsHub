from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from src.utils.functions import readYaml, getConfig
from src.utils.exceptions import CustomException
from src.utils.logger import logger
from langchain_groq import ChatGroq
import os

class QueryChainBuilder:
    def __init__(self):
        """Initializes the QueryChainBuilder class, setting up paths and loading configurations."""
        logger.info("Initializing QueryChainBuilder.")
        self.yamlPath = os.path.join(os.getcwd(), "params.yaml")
        self.config = getConfig(os.path.join(os.getcwd(), "config.ini"))

    def getChain(self):
        """
        Constructs and returns a processing chain for handling user queries, domain context, and metadata.

        This method reads prompt parameters from a YAML file and creates a processing chain 
        using LangChain components, connecting prompt, LLM, and output parser elements.

        Returns:
            dict: The constructed chain for query processing.

        Raises:
            CustomException: If any exception occurs during chain construction.
        """
        try:
            logger.info("Constructing query processing chain.")
            prompt_template = readYaml(self.yamlPath)["codeGeneratorPrompt"]
            prompt = ChatPromptTemplate.from_template(prompt_template)
            llm = ChatGroq(
                model=self.config.get("LLM", "model"),
                temperature=self.config.getfloat("LLM", "temperature")
            )
            outputParser = StrOutputParser()
            chain = {
                "user_query": RunnableLambda(lambda x: x["user_query"]),
                "domain_context": RunnableLambda(lambda x: x["domain_context"]),
                "metadata": RunnableLambda(lambda x: x["metadata"])
            } | prompt | llm | outputParser
            logger.info("Query processing chain constructed successfully.")
            return chain
        except Exception as e:
            logger.error(f"Error constructing query processing chain: {e}")
            raise CustomException(e)

    def getMetadataChain(self):
        """
        Constructs and returns a metadata generation chain for handling attribute information.

        This method reads prompt parameters from a YAML file and creates a processing chain 
        using LangChain components, connecting prompt, LLM, and output parser elements.

        Returns:
            dict: The constructed chain for metadata generation.

        Raises:
            CustomException: If any exception occurs during chain construction.
        """
        try:
            logger.info("Constructing metadata generation chain.")
            prompt_template = readYaml(self.yamlPath)["metadataGeneratorPrompt"]
            prompt = ChatPromptTemplate.from_template(prompt_template)
            llm = ChatGroq(
                model=self.config.get("LLM", "model"),
                temperature=self.config.getfloat("LLM", "temperature")
            )
            outputParser = StrOutputParser()
            chain = {
                "metadata": RunnableLambda(lambda x: x["metadata"])
            } | prompt | llm | outputParser
            logger.info("Metadata generation chain constructed successfully.")
            return chain
        except Exception as e:
            logger.error(f"Error constructing metadata generation chain: {e}")
            raise CustomException(e)