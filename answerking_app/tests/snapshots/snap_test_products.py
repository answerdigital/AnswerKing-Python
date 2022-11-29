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
    'type': 'http://testserver/problems/not_found/'
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
    'type': 'http://testserver/problems/not_found/'
}

snapshots['PostTests::test_post_invalid_data_returns_bad_request_1_invalid_id_json 1'] = {
    'detail': 'Not Found',
    'status': 404,
    'title': 'Resource not found',
    'type': 'http://testserver/problems/not_found/'
}

snapshots['PostTests::test_post_invalid_data_returns_bad_request_2_invalid_name_json 1'] = {
    'detail': 'Not Found',
    'status': 404,
    'title': 'Resource not found',
    'type': 'http://testserver/problems/not_found/'
}

snapshots['PostTests::test_post_invalid_data_returns_bad_request_3_invalid_calories_json 1'] = {
    'detail': 'Not Found',
    'status': 404,
    'title': 'Resource not found',
    'type': 'http://testserver/problems/not_found/'
}

snapshots['PostTests::test_post_invalid_data_returns_bad_request_4_invalid_description_json 1'] = {
    'detail': 'Not Found',
    'status': 404,
    'title': 'Resource not found',
    'type': 'http://testserver/problems/not_found/'
}

snapshots['PostTests::test_post_invalid_data_returns_bad_request_5_invalid_retired_json 1'] = {
    'detail': 'Not Found',
    'status': 404,
    'title': 'Resource not found',
    'type': 'http://testserver/problems/not_found/'
}

snapshots['PostTests::test_post_invalid_data_returns_bad_request_6_invalid_stock_json 1'] = {
    'detail': 'Not Found',
    'status': 404,
    'title': 'Resource not found',
    'type': 'http://testserver/problems/not_found/'
}

snapshots['PostTests::test_post_invalid_data_returns_bad_request_7_invalid_missing_fields_1_json 1'] = {
    'detail': 'Not Found',
    'status': 404,
    'title': 'Resource not found',
    'type': 'http://testserver/problems/not_found/'
}

snapshots['PostTests::test_post_invalid_data_returns_bad_request_8_invalid_missing_fields_2_json 1'] = {
    'detail': 'Not Found',
    'status': 404,
    'title': 'Resource not found',
    'type': 'http://testserver/problems/not_found/'
}

snapshots['PostTests::test_post_invalid_data_returns_bad_request_9_invalid_missing_fields_3_json 1'] = {
    'detail': 'Not Found',
    'status': 404,
    'title': 'Resource not found',
    'type': 'http://testserver/problems/not_found/'
}

snapshots['PostTests::test_post_invalid_json_returns_bad_request 1'] = {
    'detail': 'Not Found',
    'status': 404,
    'title': 'Resource not found',
    'type': 'http://testserver/problems/not_found/'
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
    'type': 'http://testserver/problems/not_found/'
}

snapshots['PutTests::test_put_non_existent_id_returns_not_found 1'] = {
    'detail': 'Not Found',
    'status': 404,
    'title': 'Resource not found',
    'type': 'http://testserver/problems/not_found/'
}
