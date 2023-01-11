import pytest
from rest_framework import status

from goals.models import BoardParticipant, Board

URL = '/goals/goal_category/list'


@pytest.mark.django_db
def test_no_categories(auth_client):
    response = auth_client.get(URL)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


@pytest.mark.django_db
def test_not_participant(auth_client, user, board):
    assert BoardParticipant.objects.filter(user_id=user.pk).count() == 0
    assert Board.objects.count() == 1

    response = auth_client.get(URL)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


@pytest.mark.django_db
@pytest.mark.parametrize("board_participant__role", [BoardParticipant.Role.owner, BoardParticipant.Role.writer,
                            BoardParticipant.Role.reader],
                            ids=['owner', 'writer', 'reader'])
def test_board_participant(auth_client, category, board_participant):
    response = auth_client.get(URL)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]['id'] == category.id
    assert data[0]['is_deleted'] == False
    assert data[0]['title'] == category.title
