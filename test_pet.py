from jsonschema import validate
import pytest
import schemas
import api_helpers
from hamcrest import assert_that, contains_string, is_
import uuid

def create_pet(status="available", pet_type="dog"):
    pet_id = int(uuid.uuid4().int % 1_000_000_000)
    payload = {
        "id": pet_id,
        "name": f"pet-{pet_id}",
        "type": pet_type,
        "status": status
    }
    resp = api_helpers.post_api_data("/pets/", payload)
    assert resp.status_code in (200, 201)
    return payload

'''
TODO: Finish this test by...
1) Troubleshooting and fixing the test failure
The purpose of this test is to validate the response matches the expected schema defined in schemas.py
'''
def test_pet_schema():
    test_endpoint = "/pets/1"

    response = api_helpers.get_api_data(test_endpoint)

    assert response.status_code == 200

    # Validate the response schema against the defined schema in schemas.py
    validate(instance=response.json(), schema=schemas.pet)

'''
TODO: Finish this test by...
1) Extending the parameterization to include all available statuses
2) Validate the appropriate response code
3) Validate the 'status' property in the response is equal to the expected status
4) Validate the schema for each object in the response
'''
@pytest.mark.parametrize("status", ["available", "pending", "sold"])
def test_find_by_status_200(status):
    # Ensure at least one pet exists with this status
    create_pet(status=status)

    test_endpoint = "/pets/findByStatus"
    params = {"status": status}

    response = api_helpers.get_api_data(test_endpoint, params)
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)

    # Every returned pet should match the requested status + schema
    for pet in data:
        assert pet["status"] == status
        validate(instance=pet, schema=schemas.pet)


'''
TODO: Finish this test by...
1) Testing and validating the appropriate 404 response for /pets/{pet_id}
2) Parameterizing the test for any edge cases
'''
@pytest.mark.parametrize("pet_id", [999999999, 123456789, 0])  # 0 *might* exist initially; see below
def test_get_by_id_404(pet_id):
    # To guarantee 404, pick a huge id that won't exist:
    if pet_id == 0:
        pet_id = 999999999

    response = api_helpers.get_api_data(f"/pets/{pet_id}")
    assert response.status_code == 404

    msg = ""
    try:
        msg = response.json().get("message", "")
    except Exception:
        msg = response.text

    assert_that(msg, contains_string("not found"))
