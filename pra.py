from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def name():
    return "Prajwal Kamble"

@app.get("/education")
def edu():
    return "Bachelor of Technology"