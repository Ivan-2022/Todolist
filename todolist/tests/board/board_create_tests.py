from rest_framework import status

import pytest


@pytest.mark.django_db
def test_success(auth_client, board):

    data = {
        "title": board.title,
    }

    response = auth_client.post(
        "/goals/board/create",
        data=data
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["title"] == board.title


@pytest.mark.django_db
def test_unauthorized(client, board):

    data = {
        "title": board.title,
    }

    response = client.post(
        "/goals/board/create",
        data=data
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
