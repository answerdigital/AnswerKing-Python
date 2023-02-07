# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots["DeleteTests::test_delete_already_retired_returns_gone 1"] = {
    "detail": "This object has already been retired",
    "status": 410,
    "title": "A server error occurred.",
    "type": "http://testserver/problems/error/",
}

snapshots["DeleteTests::test_delete_invalid_id_returns_bad_request 1"] = {
    "detail": "Invalid parameters",
    "status": 400,
    "title": "Request has invalid parameters",
    "type": "http://testserver/problems/error/",
}

snapshots["DeleteTests::test_delete_non_existent_id_returns_not_found 1"] = {
    "detail": "Not Found",
    "status": 404,
    "title": "Resource not found",
    "type": "http://testserver/problems/error/",
}

snapshots[
    "GetTests::test_get_all_with_products_returns_ok_1_basic_3_json 1"
] = [
    {
        "category": None,
        "description": "desc",
        "id": 1,
        "name": "Burger",
        "price": 1.2,
        "retired": False,
        "tags": [],
    },
    {
        "category": None,
        "description": "desc",
        "id": 2,
        "name": "Coke",
        "price": 1.5,
        "retired": False,
        "tags": [],
    },
    {
        "category": None,
        "description": "desc",
        "id": 3,
        "name": "Chips",
        "price": 1.5,
        "retired": False,
        "tags": [],
    },
]

snapshots[
    "GetTests::test_get_all_with_products_returns_ok_2_basic_1_list_json 1"
] = [
    {
        "category": None,
        "description": "desc",
        "id": 1,
        "name": "Burger",
        "price": 1.2,
        "retired": False,
        "tags": [],
    }
]

snapshots[
    "GetTests::test_get_all_with_products_returns_ok_3_extreme_5_json 1"
] = [
    {
        "category": None,
        "description": "desc",
        "id": 1,
        "name": "Burger",
        "price": 100000000000000.0,
        "retired": False,
        "tags": [],
    },
    {
        "category": None,
        "description": "desc",
        "id": 2,
        "name": "Coke",
        "price": 0.01,
        "retired": False,
        "tags": [],
    },
    {
        "category": None,
        "description": "200 chars - Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis lacinia dui et nunc hendrerit ullamcorper. Duis sit amet magna ac velit auctor porta. Praesent viverra vulputate lectus, a ves",
        "id": 3,
        "name": "Chips",
        "price": 1.5,
        "retired": False,
        "tags": [],
    },
    {
        "category": None,
        "description": "desc",
        "id": 4,
        "name": "50 chars - Lorem ipsum dolor sit amet, consectetur",
        "price": 1.5,
        "retired": False,
        "tags": [],
    },
    {
        "category": None,
        "description": "desc",
        "id": 5,
        "name": "Kabab",
        "price": 1.5,
        "retired": False,
        "tags": [],
    },
]

snapshots["GetTests::test_get_id_valid_returns_ok 1"] = {
    "category": None,
    "description": "desc",
    "id": 1,
    "name": "Burger",
    "price": 1.2,
    "retired": False,
    "tags": [],
}

snapshots["GetTests::test_get_id_valid_with_category_returns_ok 1"] = {
    "category": {"description": "Juicy Burgers", "id": 1, "name": "Burgers"},
    "description": "desc",
    "id": 1,
    "name": "Burger",
    "price": 1.2,
    "retired": False,
    "tags": [],
}

snapshots["GetTests::test_get_invalid_id_returns_bad_request 1"] = {
    "detail": "Invalid parameters",
    "status": 400,
    "title": "Request has invalid parameters",
    "type": "http://testserver/problems/error/",
}

snapshots["GetTests::test_get_non_existent_id_returns_not_found 1"] = {
    "detail": "Not Found",
    "status": 404,
    "title": "Resource not found",
    "type": "http://testserver/problems/error/",
}

snapshots["PostTests::test_post_duplicated_name_returns_400 1"] = {
    "detail": "This name already exists",
    "status": 400,
    "title": "A server error occurred.",
    "type": "http://testserver/problems/error/",
}

snapshots[
    "PostTests::test_post_invalid_data_returns_bad_request_1_invalid_id_json 1"
] = {
    "detail": "Validation Error",
    "errors": {"id": ["A valid integer is required."]},
    "status": 400,
    "title": "Invalid input.",
    "type": "http://testserver/problems/error/",
}

snapshots[
    "PostTests::test_post_invalid_data_returns_bad_request_2_invalid_name_"
    "json 1"
] = {
    "detail": "Validation Error",
    "errors": {
        "name": [
            "Enter a valid value.",
            "Ensure this field has no more than 50 characters.",
        ]
    },
    "status": 400,
    "title": "Invalid input.",
    "type": "http://testserver/problems/error/",
}

snapshots[
    "PostTests::test_post_invalid_data_returns_bad_request_3_invalid_"
    "description_json 1"
] = {
    "detail": "Validation Error",
    "errors": {
        "description": [
            "Enter a valid value.",
            "Ensure this field has no more than 200 characters.",
        ]
    },
    "status": 400,
    "title": "Invalid input.",
    "type": "http://testserver/problems/error/",
}

snapshots[
    "PostTests::test_post_invalid_data_returns_bad_request_4_invalid_retired"
    "_json 1"
] = {
    "detail": "Validation Error",
    "errors": {"retired": ["Must be a valid boolean."]},
    "status": 400,
    "title": "Invalid input.",
    "type": "http://testserver/problems/error/",
}

snapshots[
    "PostTests::test_post_invalid_data_returns_bad_request_5_invalid_missing"
    "_fields_1_json 1"
] = {
    "detail": "Validation Error",
    "errors": {
        "name": ["This field is required."],
        "price": ["This field is required."],
    },
    "status": 400,
    "title": "Invalid input.",
    "type": "http://testserver/problems/error/",
}

snapshots[
    "PostTests::test_post_invalid_data_returns_bad_request_6_invalid_missing"
    "_fields_2_json 1"
] = {
    "detail": "Validation Error",
    "errors": {
        "description": ["This field is required."],
        "price": ["This field is required."],
    },
    "status": 400,
    "title": "Invalid input.",
    "type": "http://testserver/problems/error/",
}

snapshots["PostTests::test_post_invalid_json_returns_bad_request 1"] = {
    "detail": "Parsing JSON Error",
    "errors": "JSON parse error - Expecting value: line 1 column 13 (char 12)",
    "status": 400,
    "title": "Invalid input json.",
    "type": "http://testserver/problems/error/",
}

snapshots[
    "PostTests::test_post_invalid_with_invalid_cat_id_returns_bad_request_1_invalid_category_id_json 1"
] = {
    "detail": "Validation Error",
    "errors": {"categoryId": ['Invalid pk "1" - object does not exist.']},
    "status": 400,
    "title": "Invalid input.",
    "type": "http://testserver/problems/error/",
}

snapshots["PostTests::test_post_valid_returns_ok_1_basic_1_json 1"] = [
    {
        "category": None,
        "description": "desc",
        "id": 1,
        "name": "Burger",
        "price": 1.2,
        "retired": False,
        "tags": [],
    }
]

snapshots["PostTests::test_post_valid_returns_ok_2_boundry_name_json 1"] = [
    {
        "category": None,
        "description": "desc",
        "id": 1,
        "name": "fifty chars Lorem ipsum dolor sit amet consectetur",
        "price": 1.2,
        "retired": False,
        "tags": [],
    }
]

snapshots[
    "PostTests::test_post_valid_returns_ok_3_boundry_description_json 1"
] = [
    {
        "category": None,
        "description": "twohundred chars Lorem ipsum dolor sit amet consectetur adipiscing elit Duis lacinia dui et nunc hendrerit ullamcorper Duis sit amet magna ac velit auctor porta Praesent viverra vulputate lectusjaue",
        "id": 1,
        "name": "Burger",
        "price": 1.2,
        "retired": False,
        "tags": [],
    }
]

snapshots["PostTests::test_post_valid_returns_ok_4_boundry_price_json 1"] = [
    {
        "category": None,
        "description": "desc",
        "id": 1,
        "name": "Burger",
        "price": 2147483647.0,
        "retired": False,
        "tags": [],
    }
]

snapshots[
    "PostTests::test_post_valid_with_cat_id_returns_ok_1_basic_1_with_"
    "category_id_json 1"
] = [
    {
        "category": {
            "description": "Juicy Burgers",
            "id": 1,
            "name": "Burgers",
        },
        "description": "desc",
        "id": 1,
        "name": "Burger",
        "price": 1.2,
        "retired": False,
        "tags": [],
    }
]

snapshots["PutTests::test_put_duplicated_name_returns_400 1"] = {
    "detail": "This name already exists",
    "status": 400,
    "title": "A server error occurred.",
    "type": "http://testserver/problems/error/",
}

snapshots[
    "PutTests::test_put_invalid_data_returns_bad_request_1_invalid_id_json 1"
] = {
    "detail": "Validation Error",
    "errors": {"id": ["A valid integer is required."]},
    "status": 400,
    "title": "Invalid input.",
    "type": "http://testserver/problems/error/",
}

snapshots[
    "PutTests::test_put_invalid_data_returns_bad_request_2_invalid_name_json 1"
] = {
    "detail": "Validation Error",
    "errors": {
        "name": [
            "Enter a valid value.",
            "Ensure this field has no more than 50 characters.",
        ]
    },
    "status": 400,
    "title": "Invalid input.",
    "type": "http://testserver/problems/error/",
}

snapshots[
    "PutTests::test_put_invalid_data_returns_bad_request_3_invalid_"
    "description_json 1"
] = {
    "detail": "Validation Error",
    "errors": {
        "description": [
            "Enter a valid value.",
            "Ensure this field has no more than 200 characters.",
        ]
    },
    "status": 400,
    "title": "Invalid input.",
    "type": "http://testserver/problems/error/",
}

snapshots[
    "PutTests::test_put_invalid_data_returns_bad_request_4_invalid_retired"
    "_json 1"
] = {
    "detail": "Validation Error",
    "errors": {"retired": ["Must be a valid boolean."]},
    "status": 400,
    "title": "Invalid input.",
    "type": "http://testserver/problems/error/",
}

snapshots[
    "PutTests::test_put_invalid_data_returns_bad_request_5_invalid_missing"
    "_fields_1_json 1"
] = {
    "detail": "Validation Error",
    "errors": {
        "name": ["This field is required."],
        "price": ["This field is required."],
    },
    "status": 400,
    "title": "Invalid input.",
    "type": "http://testserver/problems/error/",
}

snapshots[
    "PutTests::test_put_invalid_data_returns_bad_request_6_invalid_missing"
    "_fields_2_json 1"
] = {
    "detail": "Validation Error",
    "errors": {
        "description": ["This field is required."],
        "price": ["This field is required."],
    },
    "status": 400,
    "title": "Invalid input.",
    "type": "http://testserver/problems/error/",
}

snapshots["PutTests::test_put_invalid_id_returns_bad_request 1"] = {
    "detail": "Invalid parameters",
    "status": 400,
    "title": "Request has invalid parameters",
    "type": "http://testserver/problems/error/",
}

snapshots["PutTests::test_put_invalid_json_returns_bad_request 1"] = {
    "detail": "Parsing JSON Error",
    "errors": "JSON parse error - Expecting value: line 1 column 13 (char 12)",
    "status": 400,
    "title": "Invalid input json.",
    "type": "http://testserver/problems/error/",
}

snapshots["PutTests::test_put_non_existent_id_returns_not_found 1"] = {
    "detail": "Not Found",
    "status": 404,
    "title": "Resource not found",
    "type": "http://testserver/problems/error/",
}

snapshots["PutTests::test_put_retired_product_returns_gone 1"] = {
    "detail": "This object has already been retired, unretire it before updating it",
    "status": 410,
    "title": "A server error occurred.",
    "type": "http://testserver/problems/error/",
}

snapshots["PutTests::test_put_valid_returns_ok_1_basic_1_update_json 1"] = [
    {
        "category": None,
        "description": "A different desc",
        "id": 1,
        "name": "BurgerTwo",
        "price": 1.5,
        "retired": False,
        "tags": [],
    }
]

snapshots["PutTests::test_put_valid_returns_ok_2_boundry_name_json 1"] = [
    {
        "category": None,
        "description": "desc",
        "id": 1,
        "name": "fifty chars Lorem ipsum dolor sit amet consectetur",
        "price": 1.2,
        "retired": False,
        "tags": [],
    }
]

snapshots[
    "PutTests::test_put_valid_returns_ok_3_boundry_description_json 1"
] = [
    {
        "category": None,
        "description": "twohundred chars Lorem ipsum dolor sit amet consectetur adipiscing elit Duis lacinia dui et nunc hendrerit ullamcorper Duis sit amet magna ac velit auctor porta Praesent viverra vulputate lectusjaue",
        "id": 1,
        "name": "Burger",
        "price": 1.2,
        "retired": False,
        "tags": [],
    }
]

snapshots["PutTests::test_put_valid_returns_ok_4_boundry_price_json 1"] = [
    {
        "category": None,
        "description": "desc",
        "id": 1,
        "name": "Burger",
        "price": 2147483647.0,
        "retired": False,
        "tags": [],
    }
]
