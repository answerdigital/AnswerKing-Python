# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['GetTests::test_get_all_with_orders_returns_ok 1'] = [
    {
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
]

snapshots['GetTests::test_get_id_invalid_returns_not_found 1'] = {
    'detail': 'Invalid parameters',
    'status': 400,
    'title': 'Request has invalid parameters',
    'type': 'http://testserver/problems/error/'
}

snapshots['GetTests::test_get_id_valid_returns_ok 1'] = {
    'detail': 'Not Found',
    'status': 404,
    'title': 'Resource not found',
    'traceId': '31f10d78-230b-40e7-95cb-14b95a07a084',
    'type': 'http://testserver/problems/error/'
}

snapshots['GetTests::test_get_id_with_orders_with_prod_returns_ok 1'] = {
    'detail': 'Not Found',
    'status': 404,
    'title': 'Resource not found',
    'traceId': '45fb9487-4871-48bb-a156-234c79440a76',
    'type': 'http://testserver/problems/error/'
}

snapshots['GetTests::test_get_non_existent_id_returns_not_found 1'] = {
    'detail': 'Not Found',
    'status': 404,
    'title': 'Resource not found',
    'type': 'http://testserver/problems/error/'
}
