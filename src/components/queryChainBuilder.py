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
            logger.info("Constructing chain.")
            prompt = readYaml(self.yamlPath)["prompt"]
            prompt = ChatPromptTemplate.from_template(prompt)
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
            return chain
        except Exception as e:
            logger.error(CustomException(e))
            print(CustomException(e))