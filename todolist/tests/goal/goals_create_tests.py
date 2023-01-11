from rest_framework import status

import pytest


@pytest.mark.django_db
def test_success(auth_client, goal, category, board_participant):

    data = {
        "title": goal.title,
        "category": category.pk
    }

    response = auth_client.post(
        "/goals/goal/create",
        data=data
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["title"] == goal.title
