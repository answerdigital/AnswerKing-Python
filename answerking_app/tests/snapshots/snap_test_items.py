# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['DeleteTests::test_delete_invalid_id_returns_not_found 1'] = {
    'detail': 'Not Found',
    'status': 404,
    'title': 'Resource not found',
    'type': 'http://testserver/problems/not_found/'
}

snapshots['DeleteTests::test_delete_non_existent_id_returns_not_found 1'] = {
    'detail': 'Not Found',
    'status': 404,
    'title': 'Resource not found',
    'type': 'http://testserver/problems/error/'
}

snapshots['GetTests::test_get_invalid_id_returns_not_found 1'] = {
    'detail': 'Not Found',
    'status': 404,
    'title': 'Resource not found',
    'type': 'http://testserver/problems/not_found/'
}

snapshots['GetTests::test_get_non_existent_id_returns_not_found 1'] = {
    'detail': 'Not Found',
    'status': 404,
    'title': 'Resource not found',
    'type': 'http://testserver/problems/error/'
}

snapshots['PostTests::test_post_duplicated_name_returns_400 1'] = {
    'detail': 'This name already exists',
    'status': 400,
    'title': 'A server error occurred.',
    'type': 'http://testserver/problems/error/'
}

snapshots['PostTests::test_post_invalid_data_returns_bad_request_1_invalid_id_item_json 1'] = {
    'detail': 'Validation Error',
    'errors': {
        'id': [
            'A valid integer is required.'
        ]
    },
    'status': 400,
    'title': 'Invalid input.',
    'type': 'http://testserver/problems/error/'
}

snapshots['PostTests::test_post_invalid_data_returns_bad_request_2_invalid_name_item_json 1'] = {
    'detail': 'Validation Error',
    'errors': {
        'name': [
            'Enter a valid value.',
            'Ensure this field has no more than 50 characters.'
        ]
    },
    'status': 400,
    'title': 'Invalid input.',
    'type': 'http://testserver/problems/error/'
}

snapshots['PostTests::test_post_invalid_data_returns_bad_request_3_invalid_calories_item_json 1'] = {
    'detail': 'Validation Error',
    'errors': {
        'calories': [
            'A valid integer is required.'
        ]
    },
    'status': 400,
    'title': 'Invalid input.',
    'type': 'http://testserver/problems/error/'
}

snapshots['PostTests::test_post_invalid_data_returns_bad_request_4_invalid_description_item_json 1'] = {
    'detail': 'Validation Error',
    'errors': {
        'description': [
            'Enter a valid value.',
            'Ensure this field has no more than 200 characters.'
        ]
    },
    'status': 400,
    'title': 'Invalid input.',
    'type': 'http://testserver/problems/error/'
}

snapshots['PostTests::test_post_invalid_data_returns_bad_request_5_invalid_retired_item_json 1'] = {
    'detail': 'Validation Error',
    'errors': {
        'retired': [
            'Must be a valid boolean.'
        ]
    },
    'status': 400,
    'title': 'Invalid input.',
    'type': 'http://testserver/problems/error/'
}

snapshots['PostTests::test_post_invalid_data_returns_bad_request_6_invalid_stock_item_json 1'] = {
    'detail': 'Validation Error',
    'errors': {
        'stock': [
            'A valid integer is required.'
        ]
    },
    'status': 400,
    'title': 'Invalid input.',
    'type': 'http://testserver/problems/error/'
}

snapshots['PostTests::test_post_invalid_data_returns_bad_request_7_invalid_item_missing_fields_1_json 1'] = {
    'detail': 'Validation Error',
    'errors': {
        'name': [
            'This field is required.'
        ],
        'price': [
            'This field is required.'
        ]
    },
    'status': 400,
    'title': 'Invalid input.',
    'type': 'http://testserver/problems/error/'
}

snapshots['PostTests::test_post_invalid_data_returns_bad_request_8_invalid_item_missing_fields_2_json 1'] = {
    'detail': 'Validation Error',
    'errors': {
        'description': [
            'This field is required.'
        ],
        'stock': [
            'This field is required.'
        ]
    },
    'status': 400,
    'title': 'Invalid input.',
    'type': 'http://testserver/problems/error/'
}

snapshots['PostTests::test_post_invalid_data_returns_bad_request_9_invalid_item_missing_fields_3_json 1'] = {
    'detail': 'Validation Error',
    'errors': {
        'calories': [
            'This field is required.'
        ]
    },
    'status': 400,
    'title': 'Invalid input.',
    'type': 'http://testserver/problems/error/'
}

snapshots['PostTests::test_post_invalid_json_returns_bad_request 1'] = {
    'detail': 'Parsing JSON Error',
    'errors': 'JSON parse error - Expecting value: line 1 column 13 (char 12)',
    'status': 400,
    'title': 'Invalid input json.',
    'type': 'http://testserver/problems/error/'
}

snapshots['PutTests::test_put_duplicated_name_returns_400 1'] = {
    'detail': 'This name already exists',
    'status': 400,
    'title': 'A server error occurred.',
    'type': 'http://testserver/problems/error/'
}

snapshots['PutTests::test_put_invalid_data_returns_bad_request_1_invalid_id_item_json 1'] = {
    'detail': 'Validation Error',
    'errors': {
        'id': [
            'A valid integer is required.'
        ]
    },
    'status': 400,
    'title': 'Invalid input.',
    'type': 'http://testserver/problems/error/'
}

snapshots['PutTests::test_put_invalid_data_returns_bad_request_2_invalid_name_item_json 1'] = {
    'detail': 'Validation Error',
    'errors': {
        'name': [
            'Enter a valid value.',
            'Ensure this field has no more than 50 characters.'
        ]
    },
    'status': 400,
    'title': 'Invalid input.',
    'type': 'http://testserver/problems/error/'
}

snapshots['PutTests::test_put_invalid_data_returns_bad_request_3_invalid_calories_item_json 1'] = {
    'detail': 'Validation Error',
    'errors': {
        'calories': [
            'A valid integer is required.'
        ]
    },
    'status': 400,
    'title': 'Invalid input.',
    'type': 'http://testserver/problems/error/'
}

snapshots['PutTests::test_put_invalid_data_returns_bad_request_4_invalid_description_item_json 1'] = {
    'detail': 'Validation Error',
    'errors': {
        'description': [
            'Enter a valid value.',
            'Ensure this field has no more than 200 characters.'
        ]
    },
    'status': 400,
    'title': 'Invalid input.',
    'type': 'http://testserver/problems/error/'
}

snapshots['PutTests::test_put_invalid_data_returns_bad_request_5_invalid_retired_item_json 1'] = {
    'detail': 'Validation Error',
    'errors': {
        'retired': [
            'Must be a valid boolean.'
        ]
    },
    'status': 400,
    'title': 'Invalid input.',
    'type': 'http://testserver/problems/error/'
}

snapshots['PutTests::test_put_invalid_data_returns_bad_request_6_invalid_stock_item_json 1'] = {
    'detail': 'Validation Error',
    'errors': {
        'stock': [
            'A valid integer is required.'
        ]
    },
    'status': 400,
    'title': 'Invalid input.',
    'type': 'http://testserver/problems/error/'
}

snapshots['PutTests::test_put_invalid_data_returns_bad_request_7_invalid_item_missing_fields_1_json 1'] = {
    'detail': 'Validation Error',
    'errors': {
        'name': [
            'This field is required.'
        ],
        'price': [
            'This field is required.'
        ]
    },
    'status': 400,
    'title': 'Invalid input.',
    'type': 'http://testserver/problems/error/'
}

snapshots['PutTests::test_put_invalid_data_returns_bad_request_8_invalid_item_missing_fields_2_json 1'] = {
    'detail': 'Validation Error',
    'errors': {
        'description': [
            'This field is required.'
        ],
        'stock': [
            'This field is required.'
        ]
    },
    'status': 400,
    'title': 'Invalid input.',
    'type': 'http://testserver/problems/error/'
}

snapshots['PutTests::test_put_invalid_data_returns_bad_request_9_invalid_item_missing_fields_3_json 1'] = {
    'detail': 'Validation Error',
    'errors': {
        'calories': [
            'This field is required.'
        ]
    },
    'status': 400,
    'title': 'Invalid input.',
    'type': 'http://testserver/problems/error/'
}

snapshots['PutTests::test_put_invalid_id_returns_not_found 1'] = {
    'detail': 'Not Found',
    'status': 404,
    'title': 'Resource not found',
    'type': 'http://testserver/problems/not_found/'
}

snapshots['PutTests::test_put_invalid_json_returns_bad_request 1'] = {
    'detail': 'Not Found',
    'status': 404,
    'title': 'Resource not found',
    'type': 'http://testserver/problems/error/'
}

snapshots['PutTests::test_put_non_existent_id_returns_not_found 1'] = {
    'detail': 'Not Found',
    'status': 404,
    'title': 'Resource not found',
    'type': 'http://testserver/problems/error/'
}
