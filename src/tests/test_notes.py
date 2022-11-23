import json

import pytest

from app.api import crud


def test_create_note(test_app, monkeypatch):
    test_data = {"title": "something", "description": "something else", "id": 1}

    def mock_post(db_session, payload):
        return test_data

    monkeypatch.setattr(crud, "post", mock_post)

    response = test_app.post("/notes/", content=json.dumps(test_data),)
    assert response.status_code == 201
    assert response.json() == test_data


def test_create_note_invalid_json(test_app):
    response = test_app.post("/notes/", content=json.dumps({"title": "something"}))
    assert response.status_code == 422

    response = test_app.post(
        "/notes/", content=json.dumps({"title": "1", "description": "2"})
    )
    assert response.status_code == 422


def test_read_note(test_app, monkeypatch):
    test_data = {"title": "something", "description": "something else", "id": 1}

    def mock_get(db_session, id):
        return test_data

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.get("/notes/1")
    assert response.status_code == 200
    assert response.json() == test_data


def test_read_note_incorrect_id(test_app, monkeypatch):
    def mock_get(db_session, id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.get("/notes/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Note not found"

    response = test_app.get("/notes/0")
    assert response.status_code == 422


def test_read_all_notes(test_app, monkeypatch):
    test_data = [
        {"title": "something", "description": "something else", "id": 1},
        {"title": "someone", "description": "someone else", "id": 2},
    ]

    def mock_get_all(db_session):
        return test_data

    monkeypatch.setattr(crud, "get_all", mock_get_all)

    response = test_app.get("/notes/")
    assert response.status_code == 200
    assert response.json() == test_data


def test_update_note(test_app, monkeypatch):
    test_data = {"title": "something", "description": "something else", "id": 1}
    test_update_data = {"title": "someone", "description": "someone else", "id": 1}

    def mock_get(db_session, id):
        return test_data

    monkeypatch.setattr(crud, "get", mock_get)

    def mock_put(db_session, note, title, description):
        return test_update_data

    monkeypatch.setattr(crud, "put", mock_put)

    response = test_app.put("/notes/1/", content=json.dumps(test_update_data),)
    assert response.status_code == 200
    assert response.json() == test_update_data


@pytest.mark.parametrize(
    "id, payload, status_code",
    [
        [1, {}, 422],
        [1, {"description": "bar"}, 422],
        [999, {"title": "foo", "description": "bar"}, 404],
        [1, {"title": "1", "description": "bar"}, 422],
        [1, {"title": "foo", "description": "1"}, 422],
        [0, {"title": "foo", "description": "bar"}, 422],
    ],
)
def test_update_note_invalid(test_app, monkeypatch, id, payload, status_code):
    def mock_get(db_session, id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.put(f"/notes/{id}/", content=json.dumps(payload),)
    assert response.status_code == status_code


def test_remove_note(test_app, monkeypatch):
    test_data = {"title": "something", "description": "something else", "id": 1}

    def mock_get(db_session, id):
        return test_data

    monkeypatch.setattr(crud, "get", mock_get)

    def mock_delete(db_session, id):
        return test_data

    monkeypatch.setattr(crud, "delete", mock_delete)

    response = test_app.delete("/notes/1/")
    assert response.status_code == 200
    assert response.json() == test_data


def test_remove_note_incorrect_id(test_app, monkeypatch):
    def mock_get(db_session, id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.delete("/notes/999/")
    assert response.status_code == 404
    assert response.json()["detail"] == "Note not found"

    response = test_app.delete("/notes/0/")
    assert response.status_code == 422
