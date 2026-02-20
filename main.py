from fastapi import FastAPI


app = FastAPI()

origins = [
    "http://localhost:3000",
    "localhost:3000",
]