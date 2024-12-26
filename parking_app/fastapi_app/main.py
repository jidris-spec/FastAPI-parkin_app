from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI section of the Parking App!"}

@app.get("/check-slot/")
def check_slot(slot_number: int):
    # Dummy logic for checking a parking slot
    if slot_number % 2 == 0:
        return {"slot_number": slot_number, "status": "Available"}
    return {"slot_number": slot_number, "status": "Occupied"}
