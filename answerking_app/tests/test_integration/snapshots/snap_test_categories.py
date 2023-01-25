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
