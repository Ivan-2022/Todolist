import pytest
from rest_framework import status

from goals.serializers import GoalCategorySerializer


@pytest.mark.django_db
def test_retrieve_category(auth_client, category, board_participant):
    response = auth_client.get(f"/goals/goal_category/{category.id}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == GoalCategorySerializer(category).data


@pytest.mark.django_db
def test_unauthorized(client, category):

    response = client.get(f"/goals/goal_category/{category.pk}")

    assert response.status_code == status.HTTP_403_FORBIDDEN
