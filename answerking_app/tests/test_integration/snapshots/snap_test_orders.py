# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['DeleteTests::test_delete_already_retired_returns_gone 1'] = {
    'detail': 'This order has already been cancelled',
    'status': 400,
    'title': 'A server error occurred.',
    'type': 'http://testserver/problems/error/'
}

snapshots['DeleteTests::test_delete_invalid_id_returns_bad_request 1'] = {
    'detail': 'Invalid parameters',
    'status': 400,
    'title': 'Request has invalid parameters',
    'type': 'http://testserver/problems/error/'
}

snapshots['DeleteTests::test_delete_non_existent_id_returns_not_found 1'] = {
    'detail': 'Not Found',
    'status': 404,
    'title': 'Resource not found',
    'type': 'http://testserver/problems/error/'
}

snapshots['DeleteTests::test_delete_returns_ok 1'] = {
    'createdOn': '2023-02-10T13:49:20.044630Z',
    'id': 1,
    'lastUpdated': '2023-02-10T13:49:20.045130Z',
    'lineItems': [
    ],
    'orderStatus': 'Cancelled',
    'orderTotal': 0.0
}

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
    'traceId': 'dc354510-41cc-4ffc-9353-d3d0381cf28e',
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
    'traceId': '4f50ee3d-07bf-478f-ae9a-ec339944a27a',
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
    'traceId': 'cd27adb2-b969-4613-81de-a53e8a637e91',
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
    'traceId': '0939f09e-cb36-43ff-8770-83a867b8cf92',
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

snapshots['PostTests::test_post_retired_returns_gone 1'] = {
    'detail': 'This product has been retired',
    'status': 410,
    'title': 'A server error occurred.',
    'type': 'http://testserver/problems/error/'
}

snapshots['PostTests::test_post_valid_with_empty_products_returns_ok 1'] = {
    'createdOn': '2022-04-01T04:02:03.000000Z',
    'id': 3,
    'lastUpdated': '2022-04-01T04:02:03.000000Z',
    'lineItems': [
    ],
    'orderStatus': 'Created',
    'orderTotal': 0.0
}

snapshots['PostTests::test_post_valid_with_products_returns_ok_1_basic_1_with_products_json 1'] = {
    'createdOn': '2022-04-01T04:02:03.000000Z',
    'id': 4,
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
    'id': 5,
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
    'id': 6,
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

snapshots['PutTests::test_put_add_valid_products_to_order_return_ok_1_basic_1_with_products_json 1'] = {
    'createdOn': '2022-04-01T04:02:03.000000Z',
    'id': 1,
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

snapshots['PutTests::test_put_add_valid_products_to_order_return_ok_2_basic_2_json 1'] = {
    'createdOn': '2022-04-01T04:02:03.000000Z',
    'id': 1,
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

snapshots['PutTests::test_put_add_valid_products_to_order_return_ok_3_basic_3_json 1'] = {
    'createdOn': '2022-04-01T04:02:03.000000Z',
    'id': 1,
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

snapshots['PutTests::test_put_invalid_products_return_bad_request_1_invalid_missing_quantity_json 1'] = {
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
    'traceId': '5a2f8d12-5570-453b-839b-dbf445f6fca8',
    'type': 'http://testserver/problems/error/'
}

snapshots['PutTests::test_put_invalid_products_return_bad_request_2_invalid_product_id_json 1'] = {
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
    'traceId': '931556ac-77dc-44dc-a918-9c72f2bafa50',
    'type': 'http://testserver/problems/error/'
}

snapshots['PutTests::test_put_invalid_products_return_bad_request_3_invalid_quantity_json 1'] = {
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
    'traceId': '609e8563-c056-493f-9ded-2b6b88110515',
    'type': 'http://testserver/problems/error/'
}

snapshots['PutTests::test_put_invalid_products_return_bad_request_4_invalid_quantity_2_json 1'] = {
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
    'traceId': '42ee0305-8882-4a0f-92e2-c49f803aab66',
    'type': 'http://testserver/problems/error/'
}

snapshots['PutTests::test_put_non_existent_id_returns_not_found 1'] = {
    'detail': 'Not Found',
    'status': 404,
    'title': 'Resource not found',
    'type': 'http://testserver/problems/error/'
}

snapshots['PutTests::test_put_retired_returns_gone 1'] = {
    'detail': 'This product has been retired',
    'status': 410,
    'title': 'A server error occurred.',
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
