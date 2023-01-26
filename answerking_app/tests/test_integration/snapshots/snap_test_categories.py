# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['GetTests::test_get_all_with_categories_returns_ok_1_basic_3_json 1'] = [
    {
        'createdOn': '2022-01-01T01:02:03.000000Z',
        'description': 'Juicy Burgers',
        'id': 1,
        'lastUpdated': '2022-01-01T01:02:03.000000Z',
        'name': 'Burgers',
        'products': [
        ],
        'retired': False
    },
    {
        'createdOn': '2022-01-01T01:02:03.000000Z',
        'description': 'Cool drinks',
        'id': 2,
        'lastUpdated': '2022-01-01T01:02:03.000000Z',
        'name': 'Drinks',
        'products': [
        ],
        'retired': False
    },
    {
        'createdOn': '2022-01-01T01:02:03.000000Z',
        'description': 'Succulent sides',
        'id': 3,
        'lastUpdated': '2022-01-01T01:02:03.000000Z',
        'name': 'Sides',
        'products': [
        ],
        'retired': False
    }
]

snapshots['GetTests::test_get_all_with_categories_returns_ok_2_basic_1_list_json 1'] = [
    {
        'createdOn': '2022-01-01T01:02:03.000000Z',
        'description': 'Juicy Burgers',
        'id': 1,
        'lastUpdated': '2022-01-01T01:02:03.000000Z',
        'name': 'Burgers',
        'products': [
        ],
        'retired': False
    }
]

snapshots['GetTests::test_get_all_with_categories_returns_ok_3_extreme_3_json 1'] = [
    {
        'createdOn': '2022-01-01T01:02:03.000000Z',
        'description': '200 chars - Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis lacinia dui et nunc hendrerit ullamcorper. Duis sit amet magna ac velit auctor porta. Praesent viverra vulputate lectus, a ves',
        'id': 1,
        'lastUpdated': '2022-01-01T01:02:03.000000Z',
        'name': 'Burgers',
        'products': [
        ],
        'retired': False
    },
    {
        'createdOn': '2022-01-01T01:02:03.000000Z',
        'description': 'desc',
        'id': 2,
        'lastUpdated': '2022-01-01T01:02:03.000000Z',
        'name': '50 chars - Lorem ipsum dolor sit amet, consectetur',
        'products': [
        ],
        'retired': False
    },
    {
        'createdOn': '2022-01-01T01:02:03.000000Z',
        'description': 'Crispy fries',
        'id': 3,
        'lastUpdated': '2022-01-01T01:02:03.000000Z',
        'name': 'Sides',
        'products': [
        ],
        'retired': False
    }
]

snapshots['GetTests::test_get_id_valid_returns_ok 1'] = {
    'createdOn': '2022-01-01T01:02:03.000000Z',
    'description': 'Juicy Burgers',
    'id': 1,
    'lastUpdated': '2022-01-01T01:02:03.000000Z',
    'name': 'Burgers',
    'products': [
    ],
    'retired': False
}

snapshots['GetTests::test_get_id_valid_with_products_returns_ok 1'] = {
    'createdOn': '2022-01-01T01:02:03.000000Z',
    'description': 'Juicy Burgers',
    'id': 1,
    'lastUpdated': '2022-01-01T01:02:03.000000Z',
    'name': 'Burgers',
    'products': [
        1
    ],
    'retired': False
}

snapshots['GetTests::test_get_invalid_id_returns_bad_request 1'] = {
    'detail': 'Invalid parameters',
    'status': 400,
    'title': 'Request has invalid parameters',
    'type': 'http://testserver/problems/error/'
}

snapshots['GetTests::test_get_non_existent_id_returns_not_found 1'] = {
    'detail': 'Not Found',
    'status': 404,
    'title': 'Resource not found',
    'type': 'http://testserver/problems/error/'
}

snapshots['GetTests::test_get_prods_in_cat_invalid_id_returns_bad_request 1'] = {
    'detail': 'Invalid parameters',
    'status': 400,
    'title': 'Request has invalid parameters',
    'type': 'http://testserver/problems/error/'
}

snapshots['GetTests::test_get_prods_in_cat_non_existent_id_returns_not_found 1'] = {
    'detail': 'Not Found',
    'status': 404,
    'title': 'Resource not found',
    'type': 'http://testserver/problems/error/'
}

snapshots['GetTests::test_get_prods_in_cat_returns_ok 1'] = [
    {
        'categories': [
            {
                'description': 'Juicy Burgers',
                'id': 1,
                'name': 'Burgers'
            }
        ],
        'description': 'desc',
        'id': 1,
        'name': 'Burger',
        'price': 1.2,
        'retired': False
    }
]

snapshots['PostTests::test_post_valid_returns_ok_1_basic_1_post_json 1'] = [
    {
        'createdOn': '2022-01-01T01:02:03.000000Z',
        'description': 'Juicy Burgers',
        'id': 4,
        'lastUpdated': '2022-01-01T01:02:03.000000Z',
        'name': 'Burgers',
        'products': [
        ],
        'retired': False
    }
]

snapshots['PostTests::test_post_valid_returns_ok_2_boundary_name_json 1'] = [
    {
        'createdOn': '2022-01-01T01:02:03.000000Z',
        'description': 'Juicy Burgers',
        'id': 5,
        'lastUpdated': '2022-01-01T01:02:03.000000Z',
        'name': 'fifty chars Lorem ipsum dolor sit amet consectetur',
        'products': [
        ],
        'retired': False
    }
]

snapshots['PostTests::test_post_valid_returns_ok_3_boundary_description_json 1'] = [
    {
        'createdOn': '2022-01-01T01:02:03.000000Z',
        'description': 'two hundred chars Lorem ipsum dolor sit amet consectetur adipiscing elit Duis lacinia dui et nunc hendrerit ullamcorper Duis sit amet magna ac velit auctor porta Praesent viverra vulputate lectusjaue',
        'id': 6,
        'lastUpdated': '2022-01-01T01:02:03.000000Z',
        'name': 'Burgers',
        'products': [
        ],
        'retired': False
    }
]
