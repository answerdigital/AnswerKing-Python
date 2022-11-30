# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['CategoryTests::test_get_all_with_categories_returns_ok_1_basic_1_json 1'] = {
    'description': 'desc',
    'id': 1,
    'name': 'Burgers',
    'products': [
    ],
    'retired': False
}

snapshots['CategoryTests::test_get_all_with_categories_returns_ok_2_basic_2_json 1'] = {
    'description': 'desc',
    'id': 1,
    'name': 'Burgers',
    'products': [
    ],
    'retired': False
}

snapshots['CategoryTests::test_get_all_with_categories_returns_ok_2_basic_2_json 2'] = {
    'description': 'desc',
    'id': 2,
    'name': 'Sides',
    'products': [
    ],
    'retired': False
}
