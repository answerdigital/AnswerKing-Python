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

snapshots['GetTests::test_get_id_invalid_returns_Invalid 1'] = {
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
    'traceId': '4c5e4256-4ce7-4c58-9445-185393d9ae70',
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
    'traceId': '32ed1f64-9d4f-4fbd-9ff6-ab3e15494677',
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
    'traceId': '300e1e06-1c81-4850-acbb-66f0ab6a6b2d',
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
    'traceId': '0041b0fd-032b-4d99-9e04-41bef373e346',
    'type': 'http://testserver/problems/error/'
}

snapshots['PostTests::test_post_invalid_json_returns_bad_request 1'] = {
    'detail': 'Parsing JSON Error',
    'errors': 'JSON parse error - Expecting value: line 1 column 13 (char 12)',
    'status': 400,
    'title': 'Invalid input json.',
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
    ],
    'orderStatus': 'Created',
    'orderTotal': 0.0
}

snapshots['PostTests::test_post_valid_with_products_returns_ok_2_basic_2_json 1'] = {
    'createdOn': '2022-04-01T04:02:03.000000Z',
    'id': 6,
    'lastUpdated': '2022-04-01T04:02:03.000000Z',
    'lineItems': [
    ],
    'orderStatus': 'Created',
    'orderTotal': 0.0
}

snapshots['PostTests::test_post_valid_with_products_returns_ok_3_basic_3_json 1'] = {
    'createdOn': '2022-04-01T04:02:03.000000Z',
    'id': 7,
    'lastUpdated': '2022-04-01T04:02:03.000000Z',
    'lineItems': [
    ],
    'orderStatus': 'Created',
    'orderTotal': 0.0
}

snapshots['PutTests::test_put_add_valid_products_to_order_return_ok_1_basic_1_with_products_json 1'] = {
    'createdOn': '2022-04-01T04:02:03.000000Z',
    'id': 1,
    'lastUpdated': '2022-04-01T04:02:03.000000Z',
    'lineItems': [
    ],
    'orderStatus': 'Created',
    'orderTotal': 0.0
}

snapshots['PutTests::test_put_add_valid_products_to_order_return_ok_2_basic_2_json 1'] = {
    'createdOn': '2022-04-01T04:02:03.000000Z',
    'id': 1,
    'lastUpdated': '2022-04-01T04:02:03.000000Z',
    'lineItems': [
    ],
    'orderStatus': 'Created',
    'orderTotal': 0.0
}

snapshots['PutTests::test_put_add_valid_products_to_order_return_ok_3_basic_3_json 1'] = {
    'createdOn': '2022-04-01T04:02:03.000000Z',
    'id': 1,
    'lastUpdated': '2022-04-01T04:02:03.000000Z',
    'lineItems': [
    ],
    'orderStatus': 'Created',
    'orderTotal': 0.0
}

snapshots['PutTests::test_put_invalid_id_returns_bad_request 1'] = {
    'detail': 'Invalid parameters',
    'status': 400,
    'title': 'Request has invalid parameters',
    'type': 'http://testserver/problems/error/'
}

snapshots['PutTests::test_put_invalid_json_returns_bad_request 1'] = {
    'detail': 'Parsing JSON Error',
    'errors': 'JSON parse error - Expecting value: line 1 column 13 (char 12)',
    'status': 400,
    'title': 'Invalid input json.',
    'type': 'http://testserver/problems/error/'
}

snapshots['PutTests::test_put_invalid_products_return_empty_order_1_invalid_missing_quantity_json 1'] = {
    'createdOn': '2023-02-09T15:30:36.176856Z',
    'id': 2,
    'lastUpdated': '2023-02-09T15:30:36.176856Z',
    'lineItems': [
    ],
    'orderStatus': 'Created',
    'orderTotal': 0.0
}

snapshots['PutTests::test_put_invalid_products_return_empty_order_2_invalid_product_id_json 1'] = {
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
    'traceId': 'c82e88f4-cec0-4d2e-bcc5-69770bf56cd0',
    'type': 'http://testserver/problems/error/'
}

snapshots['PutTests::test_put_invalid_products_return_empty_order_3_invalid_quantity_json 1'] = {
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
    'traceId': 'e439d9ad-89bf-4a15-89b4-08a198d25d9e',
    'type': 'http://testserver/problems/error/'
}

snapshots['PutTests::test_put_invalid_products_return_empty_order_4_invalid_quantity_2_json 1'] = {
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
    'traceId': 'bea94db3-e010-437a-b4dd-de2288875aaa',
    'type': 'http://testserver/problems/error/'
}

snapshots['PutTests::test_put_non_existent_id_returns_not_found 1'] = {
    'detail': 'Not Found',
    'status': 404,
    'title': 'Resource not found',
    'type': 'http://testserver/problems/error/'
}

snapshots['PutTests::test_put_update_quantity_to_zero_return_empty_line_items 1'] = {
    'createdOn': '2022-04-01T04:02:03.000000Z',
    'id': 2,
    'lastUpdated': '2022-04-01T04:02:03.000000Z',
    'lineItems': [
    ],
    'orderStatus': 'Created',
    'orderTotal': 0.0
}
