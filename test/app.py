from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/items")
def read_items():
    return {"items": ["item 1", "items 2", "item 3"]}

@app.post("items")
def create_items(name: str, price: float):
    return {"item_name": name, "item_price":price}

@app.put("/items/{item_id}")
def update_items(item_id: int, name: str, price: float):
    return {"item_id": item_id, "item_name": name, "item_price":price}


@app.delete("items/{item_id}")
def delete_items(item_id: int):
    return {"message" f"Item{item_id} deleted"}