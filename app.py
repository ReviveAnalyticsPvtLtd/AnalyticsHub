from src.pipelines.pipeline import CompletePipeline
from pywebio.platform.flask import start_server
from src.utils.functions import getConfig
from pywebio.output import *
from pywebio.input import *
from pywebio import config
import os

@config(title = "AutoDataAnalyzer")
def main():
    """
    Main function to run the application, handle user inputs, and interact with the pipeline.
    
    This function facilitates file uploads, processes user queries, and displays responses
    using the CompletePipeline. The application continues to run until the user inputs "exit".
    """
    pipeline = CompletePipeline()
    
    inputData = input_group("Data Upload", 
                            inputs=[
                                file_upload(name="files", label="Upload Files", accept=".csv", multiple=True, placeholder="Drop your CSV files here"),
                                file_upload(name="metadata", label="Upload Metadata", accept=".json", multiple=False, placeholder="Drop your metadata.json here"),
                                input(name="domain", label="Enter the Domain of your dataset")
                            ])

    with put_loading().style("position: absolute; left: 50%"):
        pipeline.loadData(inputData=inputData["files"], metadata=inputData["metadata"]["content"], domainContext=inputData["domain"])

    while True:
        question = input(label="Enter your question")
        if question == "exit":
            break
        else:
            with put_loading().style("position: absolute; left: 50%"):
                flag = 0
                for i in range(5):
                    try:
                        filename, code = pipeline.generateGraph(query=question)
                    except: 
                        continue
                    message = pipeline.pythonRepl.run(code)
                    if message == "":
                        flag = 1
                        break
                    else:
                        pass

            if flag == 0:
                put_table([
                    ["Query: ", question],
                    ["Response: ", put_text(f"Encountered error in 5 tries, says: {message}")]
                ])
            else:
                put_table([
                    ["Query: ", question],
                    ["Response: ", put_html(open(filename, "r").read())]
                ])
            os.remove(filename)

if __name__ == "__main__":
    config = getConfig("config.ini")
    start_server(main, port=config.getint("APPLICATION", "port"), host=config.get("APPLICATION", "host"))