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
    'traceId': 'b38f694a-046c-4fa9-ac05-4e7a1e4d225a',
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
    'traceId': '9190435b-b8eb-4e00-b209-31e0f77d78df',
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
    'traceId': '93e39530-ac69-4a7d-aef1-2c15b089bf7c',
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
    'traceId': '60e20c9d-7c05-461f-915e-a1991459327e',
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

snapshots['PutTests::test_put_invalid_products_return_empty_order_1_invalid_missing_quantity_json 1'] = {
    'createdOn': '2023-02-09T16:41:08.781465Z',
    'id': 2,
    'lastUpdated': '2023-02-09T16:41:08.793888Z',
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
    'traceId': '49f14503-5ed1-433a-8f7e-a90f636cb732',
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
    'traceId': 'd5af3921-1944-460e-a64c-f33c7fe6a3a2',
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
    'traceId': '4af19165-d859-418a-9809-79e988e15819',
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
