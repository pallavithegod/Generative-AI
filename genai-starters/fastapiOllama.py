# PROGRAM TO RUN MODELS LOCALLY - http://127.0.0.1:8000/docs

from fastapi import FastAPI, Body
from ollama import Client

app = FastAPI(title="My AI Chat API", version="1.0")
client = Client(
    host = "http://localhost:11434"
)

@app.get("/")
# tells FastAPI: "If someone makes HTTP GET request to root URL (/), run the below fxn.
def read_root():
    return {"Hello": "World"}

# automatic data validation - http://127.0.0.1:8000/items/5?q=i%20love%20you
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = "pinpong"):    # Type Hinting
    return {"item_id": item_id, "q": q}

@app.post("/chat")
def chat(
        message: str= Body(..., description = "The Message")
        # extract data from incoming HTTP requests
        # ... => "This field is strictly required"
    ):
    response = client.chat(model = "gemma:latest", messages=[
        {"role" : "user", "content" : message}
    ])
    # an api call - talking to ollama locally

    return {"response" : response.message.content}

# terminal run - fastapi dev fastapiOllama.py
# USUAL PRACTICE TO NAME THE FILE = main.py (fastapi entry point)