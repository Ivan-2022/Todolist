import pytest
from rest_framework import status

from goals.serializers import BoardSerializer


@pytest.mark.django_db
def test_retrieve_board(auth_client, board, board_participant):

    response = auth_client.get(f"/goals/board/{board.pk}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == BoardSerializer(board).data


@pytest.mark.django_db
def test_unauthorized(client, board):

    response = client.get(f"/goals/board/{board.pk}")

    assert response.status_code == status.HTTP_403_FORBIDDEN
