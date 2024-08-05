from fastapi.testclient import TestClient
from MyAPI_Project.main_V2_SQLAlchemy import app

client = TestClient(app)

@app.get("/")
def root():
    return {"message", "Hello Word"}

# def test_root():
#     res = client.get("/")
#     print(res.json().get('message'))