from fastapi import FastAPI
import random
import time

app = FastAPI()

@app.get('/health')
def health():
    return {'status': 'ok'}

@app.get('/orders')
def get_orders():
    time.sleep(random.uniform(0, 0.3))
    return {'orders': [1, 2, 3]}

@app.get('/checkout')
def checkout():
    if random.random() < 0.1:
        raise Exception('Simulated checkout failure')
    return {'status': 'confirmed'}