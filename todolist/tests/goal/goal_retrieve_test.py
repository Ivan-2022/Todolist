import pytest
from rest_framework import status

from goals.serializers import GoalSerializer


@pytest.mark.django_db
def test_retrieve_goal(auth_client, goal, board_participant):
    response = auth_client.get(f"/goals/goal/{goal.id}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == GoalSerializer(goal).data


@pytest.mark.django_db
def test_unauthorized(client, goal):

    response = client.get(f"/goals/goal/{goal.pk}")

    assert response.status_code == status.HTTP_403_FORBIDDEN
