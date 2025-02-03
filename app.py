from src.utils.functions import getConfig, validateJson
from src.pipelines.pipeline import CompletePipeline
from pywebio.platform.flask import start_server
from pywebio.output import *
from pywebio.input import *
from pywebio import config
import json
import os

@config(title="AutoDataAnalyzer")
def main():
    """
    Main function to run the AutoDataAnalyzer application, handle user inputs, and interact with the pipeline.

    Facilitates file uploads, processes user queries, and displays responses using the CompletePipeline.
    The application runs interactively until the user inputs "exit".
    """
    pipeline = CompletePipeline()

    # File upload and domain input
    inputData = input_group("Data Upload", 
                            inputs=[
                                file_upload(name="files", label="Upload Files", accept=".csv", multiple=True, placeholder="Drop your CSV files here"),
                                input(name="domain", label="Enter the Domain of your dataset")
                            ])

    # Load data into the pipeline
    with put_loading().style("position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); text-align: center;"):
        put_text("Generating metadata... This may take a moment.")
        pipeline.loadData(inputData=inputData["files"], domainContext=inputData["domain"])

    metadata = textarea(
        label = "Generated Metadata:",
        code = {
            "language": "yaml",
            "theme": "dracula"
        },
        value = json.dumps(pipeline.metadata, indent = 3),
        validate = validateJson,
        rows = 50
    )
    pipeline.metadata = json.loads(metadata)

    # Interactive question loop
    while True:
        question = input(label="Enter your question")
        if question.lower() == "exit":
            break
        else:
            with put_loading().style("position: absolute; left: 50%;"):
                success = False
                for attempt in range(5):
                    try:
                        filename, code = pipeline.generateGraph(query=question)
                        print(code)
                    except Exception as e:
                        continue
                    message = pipeline.pythonRepl.run(code)
                    if message == "":
                        success = True
                        break
                    else:
                        pass

            # Handle result or failure
            if success == False:
                put_table([
                    ["Query: ", question],
                    ["Response: ", put_text(f"Encountered error after 5 tries: {message}")]
                ])
            else:
                put_table([
                    ["Query: ", question],
                    ["Response: ", put_html(open(filename, "r").read())]
                ])
                os.remove(filename)

if __name__ == "__main__":
    config = getConfig("config.ini")
    port = config.getint("APPLICATION", "port")
    host = config.get("APPLICATION", "host")
    start_server(main, port=port, host=host)
