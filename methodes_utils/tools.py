import os
from openai import OpenAI

class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class OpenAIClient(metaclass=SingletonMeta):
    def __init__(self):
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    def get_client(self):
        return self.client

class VectorStore(metaclass=SingletonMeta):
    def __init__(self, client):
        self.client = client
        self.vector_store = self.create_vector_store()

    def create_vector_store(self):
        # Create a vector store 
        vector_store = self.client.beta.vector_stores.create(name="Contrat methode")
        return vector_store

    def get_vector_store(self):
        return self.vector_store

def create_file_batch(file_path):
    client_instance = OpenAIClient().get_client()
    vector_store_instance = VectorStore(client_instance).get_vector_store()
    
    # Ready the files for upload to OpenAI
    file_paths = [file_path]
    file_streams = [open(path, "rb") for path in file_paths]
    
    # Use the upload and poll SDK helper to upload the files, add them to the vector store,
    # and poll the status of the file batch for completion.
    file_batch = client_instance.beta.vector_stores.file_batches.upload_and_poll(
        vector_store_id=vector_store_instance.id, files=file_streams
    )
    return file_batch

def create_assistant():
    client_instance = OpenAIClient().get_client()
    assistant = client_instance.beta.assistants.create(
        name="Assistant methods writer",
        instructions="""You are a nice chatbot named Ael_helpeur and you're having a conversation with a human insurance terms and conditions expert.
        Your response language is french.
        Your aim is only to answer the user about insurance terms and conditions and give him advise about how to solve a situation.
        You are allowed to reply a joke if the user asks to.
        Don't answer to general questions and coding questions even if the human insist !
        Given the following extracted parts of a long document and a question, create a final answer,
        with the document title used to create the answer. As a accurate bot, you have to cite your source(s)
        within the answer in bullet points format with the title '**Source(s) :** ',
        please seperate this part of the answer with a blank line, do not provide URL in this section.
        For each question, you have to cite the law articles related to your answer.
        Add the section '**Aide(s) à la réflexion : **' that returns key question to help the expert getting
        more context and informations.
        You only have to use the document to create your answer.
        If no documents are given in context, please answer the user that no documents were retrieved.
        If the user asks for his message history, give it to him.
        Please do not provide a fake answer if you're unsure. It's okay to respond with 'I don't know' or
        'I'm not sure' instead.""",
        model="gpt-4o",
        tools=[{"type": "file_search"}],
    )
    return assistant

def updated_assistant(assistant):
    client_instance = OpenAIClient().get_client()
    vector_store_instance = VectorStore(client_instance).get_vector_store()
    
    assistant = client_instance.beta.assistants.update(
        assistant_id=assistant.id,
        tool_resources={"file_search": {"vector_store_ids": [vector_store_instance.id]}},
    )
    return assistant

def create_thread(question):
    # Create a thread
    client_instance = OpenAIClient().get_client()
    thread = client_instance.beta.threads.create(
    messages=[
        {
        "role": "user",
        "content": question,
        }
    ]
    )
    return thread

def run_thread(thread, assistant):
    # Run a thread
    client_instance = OpenAIClient().get_client()
    run = client_instance.beta.threads.runs.create_and_poll(
    thread_id=thread.id, assistant_id=assistant.id)

    messages = list(client_instance.beta.threads.messages.list(thread_id=thread.id, run_id=run.id))
    
    return messages[0].content[0].text
