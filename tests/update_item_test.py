import json, pytest, random

updated_item_data = {'name':'updated', 'description':'This item has been updated!', 'type': 'test',
                    'quantity':999, 'weight':100, 'gpvalue':12}

@pytest.fixture
def update_item(gateway_factory, created_item):
    gateway = gateway_factory()
    response = gateway.handle_request(method='PUT', path='/item/test-collection-guid-for-item/'+ str(created_item['id']),
                                    headers={'Content-Type':'application/json'},
                                    body=json.dumps(updated_item_data))
    return response

@pytest.fixture
def update_response_body_json(update_item):
    return json.loads(update_item['body'])

@pytest.fixture
def get_updated_item(update_response_body_json, gateway_factory):
    gateway = gateway_factory()
    itemID = update_response_body_json['result-id']
    response = gateway.handle_request(method='GET',
                                        path='/item/test-collection-guid-for-item/' + str(itemID),
                                        headers={},
                                        body='')
    return response

@pytest.fixture
def updated_item(get_updated_item):
    return json.loads(get_updated_item['body'])

class TestUpdateItem(object):
    def test_response_status_code(self, update_item):
        assert update_item['statusCode'] == 200
    def test_response_json_formatting(self, update_response_body_json, created_item):
        assert update_response_body_json['action'] == 'UPDATE'
        assert update_response_body_json['target'] == 'ITEM'
        assert update_response_body_json['success'] == True
        assert update_response_body_json['result-id'] == created_item['id']
    def test_created_item_exists(self, get_updated_item):
        assert get_updated_item['statusCode'] == 200
    def test_created_item_values(self, updated_item):
        assert updated_item['name'] == updated_item_data['name']
        assert updated_item['description'] == updated_item_data['description']
        assert updated_item['type'] == updated_item_data['type']
        assert updated_item['quantity'] == updated_item_data['quantity']
        assert updated_item['weight'] == updated_item_data['weight']
        assert updated_item['gpvalue'] == updated_item_data['gpvalue']
