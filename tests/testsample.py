# import pytest
# from MyAPI_Project.Testing_calculation import add, sub

# ## To run the pytest -> On command line run pytest -v -s

# @pytest.mark.parametrize("num1, num2, expected", [
#         (3, 2, 5),
#         (2, 6, 8),
#         (7, 2, 9)
# ])


# def test_add(num1, num2, expected):
#     assert add(num1 , num2) == expected


import pytest
from fastapi.testclient import TestClient
from MyAPI_Project.main_V2_SQLAlchemy import app

client = TestClient(app)

def test_root():
    res = client.get("/")
    print(res.json().get('message'))
