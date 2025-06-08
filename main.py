from fastapi import FastAPI
from typing import List
import numpy as np
from sklearn.metrics.pairwise import cosine_simularity


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Foo bar"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.post("/analyze/{project}")
async def analyze():
