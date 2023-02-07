# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['DeleteTests::test_delete_already_retired_returns_gone 1'] = {
    'detail': 'This object has already been retired',
    'status': 410,
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

snapshots['GetTests::test_get_all_with_tags_returns_ok_1_basic_3_json 1'] = [
    {
        'description': 'Tag identifying a product as halal.',
        'id': 1,
        'name': 'Halal',
        'products': [
        ],
        'retired': False
    },
    {
        'description': 'Tag identifying a product as vegetarian.',
        'id': 2,
        'name': 'Vegetarian',
        'products': [
        ],
        'retired': False
    },
    {
        'description': 'Tag identifying a product as vegan.',
        'id': 3,
        'name': 'Vegan',
        'products': [
        ],
        'retired': False
    }
]

snapshots['GetTests::test_get_all_with_tags_returns_ok_2_basic_1_list_json 1'] = [
    {
        'description': 'Tag identifying a product as halal.',
        'id': 1,
        'name': 'Halal',
        'products': [
        ],
        'retired': False
    }
]

snapshots['GetTests::test_get_all_with_tags_returns_ok_3_extreme_3_json 1'] = [
    {
        'description': 'Tag identifying a product as halal.',
        'id': 1,
        'name': 'fifty chars Lorem ipsum dolor sit amet consectetur',
        'products': [
        ],
        'retired': False
    },
    {
        'description': 'twohundred chars Lorem ipsum dolor sit amet consectetur adipiscing elit Duis lacinia dui et nunc hendrerit ullamcorper Duis sit amet magna ac velit auctor porta Praesent viverra vulputate lectusjaue',
        'id': 2,
        'name': 'Vegetarian',
        'products': [
        ],
        'retired': False
    },
    {
        'description': 'Tag identifying a product as vegan.',
        'id': 3,
        'name': 'Vegan',
        'products': [
        ],
        'retired': False
    }
]

snapshots['GetTests::test_get_id_valid_returns_ok 1'] = {
    'description': 'Tag identifying a product as halal.',
    'id': 1,
    'name': 'Halal',
    'products': [
    ],
    'retired': False
}

snapshots['GetTests::test_get_id_valid_with_products_returns_ok 1'] = {
    'description': 'Tag identifying a product as halal.',
    'id': 1,
    'name': 'Halal',
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

snapshots['PostTests::test_post_duplicated_name_returns_400 1'] = {
    'detail': 'This name already exists',
    'status': 400,
    'title': 'A server error occurred.',
    'type': 'http://testserver/problems/error/'
}

snapshots['PostTests::test_post_invalid_data_returns_bad_request_1_invalid_id_json 1'] = {
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

snapshots['PostTests::test_post_invalid_data_returns_bad_request_2_invalid_name_json 1'] = {
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

snapshots['PostTests::test_post_invalid_data_returns_bad_request_3_invalid_description_json 1'] = {
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

snapshots['PostTests::test_post_invalid_data_returns_bad_request_4_invalid_missing_fields_json 1'] = {
    'detail': 'Validation Error',
    'errors': {
        'name': [
            'This field is required.'
        ]
    },
    'status': 400,
    'title': 'Invalid input.',
    'type': 'http://testserver/problems/error/'
}

snapshots['PostTests::test_post_invalid_data_returns_bad_request_5_invalid_retired_json 1'] = {
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

snapshots['PostTests::test_post_invalid_json_returns_bad_request 1'] = {
    'detail': 'Parsing JSON Error',
    'errors': 'JSON parse error - Expecting value: line 1 column 13 (char 12)',
    'status': 400,
    'title': 'Invalid input json.',
    'type': 'http://testserver/problems/error/'
}

snapshots['PostTests::test_post_invalid_product_id_returns_bad_request_1_invalid_product_id_json 1'] = {
    'detail': 'Validation Error',
    'errors': {
        'products': [
            'Incorrect type. Expected pk value, received str.'
        ]
    },
    'status': 400,
    'title': 'Invalid input.',
    'type': 'http://testserver/problems/error/'
}

snapshots['PostTests::test_post_nonexistent_product_id_returns_not_found_1_basic_1_with_products_json 1'] = {
    'detail': 'Validation Error',
    'errors': {
        'products': [
            'Invalid pk "1" - object does not exist.'
        ]
    },
    'status': 400,
    'title': 'Invalid input.',
    'type': 'http://testserver/problems/error/'
}

snapshots['PostTests::test_post_valid_returns_ok_1_basic_1_post_json 1'] = [
    {
        'description': 'Tag identifying a product as halal.',
        'id': 1,
        'name': 'Halal',
        'products': [
        ],
        'retired': False
    }
]

snapshots['PostTests::test_post_valid_returns_ok_2_boundary_name_json 1'] = [
    {
        'description': 'Tag identifying a product as halal.',
        'id': 1,
        'name': 'fifty chars Lorem ipsum dolor sit amet consectetur',
        'products': [
        ],
        'retired': False
    }
]

snapshots['PostTests::test_post_valid_returns_ok_3_boundary_description_json 1'] = [
    {
        'description': 'twohundred chars Lorem ipsum dolor sit amet consectetur adipiscing elit Duis lacinia dui et nunc hendrerit ullamcorper Duis sit amet magna ac velit auctor porta Praesent viverra vulputate lectusjaue',
        'id': 1,
        'name': 'Halal',
        'products': [
        ],
        'retired': False
    }
]

snapshots['PostTests::test_post_valid_with_products_returns_ok_1_basic_1_with_products_json 1'] = [
    {
        'description': 'Tag identifying a product as halal.',
        'id': 1,
        'name': 'Halal',
        'products': [
            1,
            2,
            3
        ],
        'retired': False
    }
]

snapshots['PutTests::test_put_duplicated_name_returns_400 1'] = {
    'detail': 'This name already exists',
    'status': 400,
    'title': 'A server error occurred.',
    'type': 'http://testserver/problems/error/'
}

snapshots['PutTests::test_put_invalid_data_returns_bad_request_1_invalid_id_json 1'] = {
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

snapshots['PutTests::test_put_invalid_data_returns_bad_request_2_invalid_name_json 1'] = {
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

snapshots['PutTests::test_put_invalid_data_returns_bad_request_3_invalid_description_json 1'] = {
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

snapshots['PutTests::test_put_invalid_data_returns_bad_request_4_invalid_missing_fields_json 1'] = {
    'detail': 'Validation Error',
    'errors': {
        'name': [
            'This field is required.'
        ]
    },
    'status': 400,
    'title': 'Invalid input.',
    'type': 'http://testserver/problems/error/'
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

snapshots['PutTests::test_put_invalid_prod_data_returns_bad_request_1_basic_1_update_with_products_json 1'] = {
    'detail': 'Validation Error',
    'errors': {
        'products': [
            'Invalid pk "3" - object does not exist.'
        ]
    },
    'status': 400,
    'title': 'Invalid input.',
    'type': 'http://testserver/problems/error/'
}

snapshots['PutTests::test_put_invalid_prod_data_returns_bad_request_2_invalid_product_id_json 1'] = {
    'detail': 'Validation Error',
    'errors': {
        'products': [
            'Incorrect type. Expected pk value, received str.'
        ]
    },
    'status': 400,
    'title': 'Invalid input.',
    'type': 'http://testserver/problems/error/'
}

snapshots['PutTests::test_put_non_existent_id_returns_not_found 1'] = {
    'detail': 'Not Found',
    'status': 404,
    'title': 'Resource not found',
    'type': 'http://testserver/problems/error/'
}

snapshots['PutTests::test_put_retired_returns_gone 1'] = {
    'detail': 'This object has already been retired, unretire it before updating it',
    'status': 410,
    'title': 'A server error occurred.',
    'type': 'http://testserver/problems/error/'
}

snapshots['PutTests::test_put_valid_returns_ok_1_basic_1_update_json 1'] = [
    {
        'description': 'Tag identifying a product as halal.',
        'id': 1,
        'name': 'Halal products',
        'products': [
        ],
        'retired': False
    }
]

snapshots['PutTests::test_put_valid_returns_ok_2_boundary_name_json 1'] = [
    {
        'description': 'Tag identifying a product as halal.',
        'id': 1,
        'name': 'fifty chars Lorem ipsum dolor sit amet consectetur',
        'products': [
        ],
        'retired': False
    }
]

snapshots['PutTests::test_put_valid_returns_ok_3_boundary_description_json 1'] = [
    {
        'description': 'twohundred chars Lorem ipsum dolor sit amet consectetur adipiscing elit Duis lacinia dui et nunc hendrerit ullamcorper Duis sit amet magna ac velit auctor porta Praesent viverra vulputate lectusjaue',
        'id': 1,
        'name': 'Halal',
        'products': [
        ],
        'retired': False
    }
]

snapshots['PutTests::test_put_with_prods_valid_returns_ok_1_basic_1_update_with_products_json 1'] = [
    {
        'description': 'Tag identifying a product as halal.',
        'id': 1,
        'name': 'Halal',
        'products': [
            3
        ],
        'retired': False
    }
]
