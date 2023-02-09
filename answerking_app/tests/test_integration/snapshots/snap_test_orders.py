# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['GetTests::test_get_all_with_orders_returns_ok 1'] = [
    {
        'createdOn': '2022-04-01T04:02:03.000000Z',
        'id': 2,
        'lastUpdated': '2022-04-01T04:02:03.000000Z',
        'lineItems': [
            {
                'product': {
                    'description': 'desc',
                    'id': 2,
                    'name': 'Coke',
                    'price': 1.5
                },
                'quantity': 4,
                'subTotal': 6.0
            }
        ],
        'orderStatus': 'Created',
        'orderTotal': 6.0
    }
]

snapshots['GetTests::test_get_id_invalid_returns_not_found 1'] = {
    'detail': 'Invalid parameters',
    'status': 400,
    'title': 'Request has invalid parameters',
    'type': 'http://testserver/problems/error/'
}

snapshots['GetTests::test_get_id_valid_returns_ok 1'] = {
    'createdOn': '2022-04-01T04:02:03.000000Z',
    'id': 1,
    'lastUpdated': '2022-04-01T04:02:03.000000Z',
    'lineItems': [
    ],
    'orderStatus': 'Created',
    'orderTotal': 0.0
}

snapshots['GetTests::test_get_id_with_orders_with_prod_returns_ok 1'] = {
    'createdOn': '2022-04-01T04:02:03.000000Z',
    'id': 2,
    'lastUpdated': '2022-04-01T04:02:03.000000Z',
    'lineItems': [
        {
            'product': {
                'description': 'desc',
                'id': 2,
                'name': 'Coke',
                'price': 1.5
            },
            'quantity': 4,
            'subTotal': 6.0
        }
    ],
    'orderStatus': 'Created',
    'orderTotal': 6.0
}

snapshots['GetTests::test_get_non_existent_id_returns_not_found 1'] = {
    'detail': 'Not Found',
    'status': 404,
    'title': 'Resource not found',
    'type': 'http://testserver/problems/error/'
}

snapshots['PostTests::test_post_invalid_data_returns_bad_request_1_invalid_missing_quantity_json 1'] = {
    'detail': 'Validation Error',
    'errors': {
        'lineItems': [
            {
                'quantity': [
                    'This field is required.'
                ]
            }
        ]
    },
    'status': 400,
    'title': 'Invalid input.',
    'traceId': '174bd062-357c-4f84-81db-3c833d274d60',
    'type': 'http://testserver/problems/error/'
}

snapshots['PostTests::test_post_invalid_data_returns_bad_request_2_invalid_product_id_json 1'] = {
    'detail': 'Validation Error',
    'errors': {
        'lineItems': [
            {
                'product': {
                    'id': [
                        'A valid integer is required.'
                    ]
                }
            }
        ]
    },
    'status': 400,
    'title': 'Invalid input.',
    'traceId': 'd629a356-eb17-46c8-a3a0-fffa9a8c3e45',
    'type': 'http://testserver/problems/error/'
}

snapshots['PostTests::test_post_invalid_data_returns_bad_request_3_invalid_quantity_json 1'] = {
    'detail': 'Validation Error',
    'errors': {
        'lineItems': [
            {
                'quantity': [
                    'Ensure this value is greater than or equal to 0.'
                ]
            }
        ]
    },
    'status': 400,
    'title': 'Invalid input.',
    'traceId': '9a9e2c01-b221-4913-9d74-a7a25b77b6d6',
    'type': 'http://testserver/problems/error/'
}

snapshots['PostTests::test_post_invalid_data_returns_bad_request_4_invalid_quantity_2_json 1'] = {
    'detail': 'Validation Error',
    'errors': {
        'lineItems': [
            {
                'quantity': [
                    'A valid integer is required.'
                ]
            }
        ]
    },
    'status': 400,
    'title': 'Invalid input.',
    'traceId': 'cba6c00d-1f12-48ce-beb1-5410f12ef051',
    'type': 'http://testserver/problems/error/'
}

snapshots['PostTests::test_post_invalid_json_returns_bad_request 1'] = {
    'detail': 'Parsing JSON Error',
    'errors': 'JSON parse error - Expecting value: line 1 column 13 (char 12)',
    'status': 400,
    'title': 'Invalid input json.',
    'type': 'http://testserver/problems/error/'
}

snapshots['PostTests::test_post_non_existent_product_id_returns_404 1'] = {
    'detail': 'Object was not Found',
    'errors': [
        'Product matching query does not exist.'
    ],
    'status': 404,
    'title': 'Resource not found',
    'type': 'http://testserver/problems/error/'
}

snapshots['PostTests::test_post_valid_with_empty_products_returns_ok 1'] = {
    'createdOn': '2022-04-01T04:02:03.000000Z',
    'id': 4,
    'lastUpdated': '2022-04-01T04:02:03.000000Z',
    'lineItems': [
    ],
    'orderStatus': 'Created',
    'orderTotal': 0.0
}

snapshots['PostTests::test_post_valid_with_products_returns_ok_1_basic_1_with_products_json 1'] = {
    'createdOn': '2022-04-01T04:02:03.000000Z',
    'id': 5,
    'lastUpdated': '2022-04-01T04:02:03.000000Z',
    'lineItems': [
        {
            'product': {
                'description': 'desc',
                'id': 1,
                'name': 'Burger',
                'price': 1.2
            },
            'quantity': 4,
            'subTotal': 4.8
        }
    ],
    'orderStatus': 'Created',
    'orderTotal': 4.8
}

snapshots['PostTests::test_post_valid_with_products_returns_ok_2_basic_2_json 1'] = {
    'createdOn': '2022-04-01T04:02:03.000000Z',
    'id': 6,
    'lastUpdated': '2022-04-01T04:02:03.000000Z',
    'lineItems': [
        {
            'product': {
                'description': 'desc',
                'id': 2,
                'name': 'Coke',
                'price': 1.5
            },
            'quantity': 4,
            'subTotal': 6.0
        }
    ],
    'orderStatus': 'Created',
    'orderTotal': 6.0
}

snapshots['PostTests::test_post_valid_with_products_returns_ok_3_basic_3_json 1'] = {
    'createdOn': '2022-04-01T04:02:03.000000Z',
    'id': 7,
    'lastUpdated': '2022-04-01T04:02:03.000000Z',
    'lineItems': [
        {
            'product': {
                'description': 'desc',
                'id': 1,
                'name': 'Burger',
                'price': 1.2
            },
            'quantity': 3,
            'subTotal': 3.6
        },
        {
            'product': {
                'description': 'desc',
                'id': 2,
                'name': 'Coke',
                'price': 1.5
            },
            'quantity': 2,
            'subTotal': 3.0
        }
    ],
    'orderStatus': 'Created',
    'orderTotal': 6.6
}
