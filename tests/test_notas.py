from fastapi import FastAPI

from fastapi.testclient import TestClient

app = FastAPI()

client = TestClient(app)

def test_read_index_notas():

    resp = client.get("/notas")

    assert resp.status_code == 200

    assert resp.json() == {
        "status": "Success",
        "data": []
    }


def test_create_notas():
    resp = client.post(
        "/notas/",
        headers={"X-Token": "A"},
        json={
            "id": 1,
            "value": 10,
        }
    )

    assert resp.status_code == 200

    assert resp.json() == {
        "id": 1,
        "value": 10
    }

def test_read_notas():
    resp = client.get(
        "/notas/1/",
        headers={"X-Token": "A"}
    )

    assert resp.status_code == 200

    assert resp.json() == {
        "id": 1,
        "value": 10
    }