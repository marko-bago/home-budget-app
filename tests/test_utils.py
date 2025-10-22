from src.auth.schemas import UserCreate
from src.expenses.schemas import ExpenseCreate
from src.categories.schemas import CategoryCreate
from datetime import datetime


def create_test_resource(
    client,
    endpoint: str,
    model_class,
    token: str | None = None,
    timestamp_field: str | None = None,
    **data
):
    """
    Generic helper to create any test resource via POST.
    """
    payload = model_class(**data).model_dump()

    if timestamp_field:
        ts = datetime.now()
        payload[timestamp_field] = ts.strftime("%d-%m-%Y %H:%M")

    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    response = client.post(endpoint, headers=headers, json=payload)
    return response

def create_test_user(client, **kwargs):
    return create_test_resource(client, "/api/v1/auth/register", UserCreate, **kwargs)

def create_test_expense(client, **kwargs):
    return create_test_resource(client, "/api/v1/expenses", ExpenseCreate, **kwargs)

def create_test_category(client, **kwargs):
    return create_test_resource(client, "/api/v1/categories", CategoryCreate, **kwargs)