from jsonschema import validate
import pytest
import schemas
import api_helpers
from hamcrest import assert_that, contains_string, is_
import uuid

'''
TODO: Finish this test by...
1) Creating a function to test the PATCH request /store/order/{order_id}
2) *Optional* Consider using @pytest.fixture to create unique test data for each run
2) *Optional* Consider creating an 'Order' model in schemas.py and validating it in the test
3) Validate the response codes and values
4) Validate the response message "Order and pet status updated successfully"
'''
def create_pet(status="available", pet_type="cat"):
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

def test_patch_order_by_id():
    # 1) Create a new available pet so ordering always works
    pet = create_pet(status="available", pet_type="dog")

    # 2) Place an order
    create_order_payload = {"pet_id": pet["id"]}
    create_resp = api_helpers.post_api_data("/store/order", create_order_payload)
    assert create_resp.status_code in (200, 201)

    order = create_resp.json()
    assert "id" in order
    assert order["pet_id"] == pet["id"]

    # Optional schema validation if you added schemas.order
    # validate(instance=order, schema=schemas.order)

    order_id = order["id"]

    # 3) PATCH the order status
    patch_payload = {"status": "sold"}
    patch_resp = api_helpers.patch_api_data(f"/store/order/{order_id}", patch_payload)
    assert patch_resp.status_code == 200

    patch_json = patch_resp.json()
    assert_that(patch_json["message"], is_("Order and pet status updated successfully"))

    # 4) Verify pet status updated too
    pet_resp = api_helpers.get_api_data(f"/pets/{pet['id']}")
    assert pet_resp.status_code == 200
    assert pet_resp.json()["status"] == "sold"
