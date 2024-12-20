from src.utils.exceptions import CustomException
from src.utils.logger import logger
import uuid

class CodeGenerator:
    def __init__(self):
        """Initializes the CodeGenerator class."""
        logger.info("CodeGenerator initialized.")

    def generateCode(self, chain, userQuery: str, domainContext: str, metadata: str) -> str:
        """
        Invokes the provided chain with user query, domain context, and metadata to generate a code result.

        Args:
            chain: The processing chain used to generate the code based on inputs.
            userQuery (str): The user's query text.
            domainContext (str): The context for the domain in which the query applies.
            metadata (str): Additional metadata to assist in code generation.

        Returns:
            str: The result generated by invoking the chain.

        Raises:
            CustomException: If an error occurs during code generation.
        """
        try:
            logger.info("Invoking the chain for code generation.")
            inputDict = {
                "user_query": userQuery,
                "domain_context": domainContext,
                "metadata": metadata
            }
            result = chain.invoke(inputDict)
            logger.info("Code generation successful.")
            return result
        except Exception as e:
            logger.error(f"Error in code generation: {e}")
            raise CustomException(e)

    def codeRefiner(self, codeBlock: str) -> tuple[str]:
        """
        Refines and modifies the provided code block for display and saves it to an HTML file.

        Args:
            codeBlock (str): The raw code block string to be refined.

        Returns:
            tuple[str]: A tuple containing the filename and the refined code.

        Raises:
            CustomException: If an error occurs during code refinement.
        """
        try:
            logger.info("Refining the generated code block.")
            codeBlockParts = codeBlock.split("```")
            code = codeBlockParts[-2]
            code = "\n".join(code.split("\n")[1:])  # Remove the initial code fence
            codeSplit = code.split("show()")
            filename = f"{uuid.uuid4()}.html"
            config = {"displaylogo": False}
            refinedCode = (
                codeSplit[0] +
                f"write_html('{filename}', full_html = False, include_plotlyjs='require', config={config})" +
                codeSplit[1]
            )
            logger.info("Code refinement successful.")
            return (filename, refinedCode)
        except Exception as e:
            logger.error(f"Error in code refinement: {e}")
            raise CustomException(e)