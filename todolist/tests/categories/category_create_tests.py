from rest_framework import status

import pytest


@pytest.mark.django_db
def test_success(auth_client, category, board_participant):

    data = {
        "title": category.title,
        "board": board_participant.board.pk,
        "user": board_participant.user_id
    }

    response = auth_client.post(
        "/goals/goal_category/create",
        data=data
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["title"] == category.title
