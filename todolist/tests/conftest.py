import pytest
from pytest_factoryboy import register

import factories


register(factories.UserFactory)
register(factories.BoardFactory)
register(factories.BoardParticipantFactory)
register(factories.CategoryFactory)
register(factories.GoalFactory)


@pytest.fixture
@pytest.mark.django_db
def auth_client(client, user):
    client.force_login(user)
    return client
