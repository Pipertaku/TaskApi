
from app.schemes.users_scheme import ResponseUsers

def test_userresponse(client):
    # Correctly structure the JSON data as a dictionary with key-value pairs
    res = client.post("/users", json={
        "firstname": "Nashel",
        "lastname": "Mashumba",
        "age": 20,
        "sex":"male",
        "password": "123456",
        "email": "nashelmashumba32@gmail.com"
    })
    assert res.status_code == 201

    new_user = ResponseUsers(**res.json())
    assert new_user.email == "nashelmashumba32@gmail.com"



