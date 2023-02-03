from answerking_app.utils.model_types import (
    ProductType,
    CategoryType,
    OrderType,
    ProblemDetails,
    ProductCategoryIdType,
    ProductBodyType,
    OrderProductType,
    TagType,
    TagBodyType,
)

example_time = "2022-11-23T10:15:36.622Z"

category_product_example: int = 0

tag_product_example: list[int] = [1, 2]

product_category_example: CategoryType = {
    "id": 0,
    "name": "string",
    "description": "string",
}

tag_example: TagType = {
    "id": 0,
    "name": "string",
    "description": "string",
    "products": [0],
    "retired": False,
}

retired_tag_example: TagType = tag_example
retired_tag_example["retired"] = True

tag_body_example: TagBodyType = {
    "name": "string",
    "description": "string",
    "products": [0],
}

product_example: ProductType = {
    "id": 0,
    "name": "string",
    "price": 0,
    "description": "string",
    "category": product_category_example,
    "retired": False,
}

retired_product_example: ProductType = product_example
retired_product_example["retired"] = True

product_body_example: ProductBodyType = {
    "name": "string",
    "description": "string",
    "price": 0,
    "category": category_product_example,
}

product_categories_body_example: ProductCategoryIdType = {
    "name": "string",
    "description": "string",
    "price": 0,
    "category": category_product_example,
}

category_example: CategoryType = {
    "id": 0,
    "name": "string",
    "description": "string",
    "createdOn": example_time,
    "lastUpdated": example_time,
    "products": [0],
    "retired": False,
}

retired_category_example: CategoryType = category_example
retired_category_example["retired"] = True

category_body_example: CategoryType = {
    "name": "string",
    "description": "string",
    "products": [category_product_example],
}

category_products_body_example: CategoryType = {
    "name": "string",
    "description": "string",
    "products": [category_product_example],
}

order_product_example: ProductType = {
    "id": 0,
    "name": "string",
    "price": 0,
    "description": "string",
    "category": product_category_example,
}

line_items_example: OrderProductType = {
    "product": order_product_example,
    "quantity": 0,
    "subTotal": 0,
}

order_example: OrderType = {
    "id": 0,
    "createdOn": example_time,
    "lastUpdated": example_time,
    "orderStatus": "Created",
    "orderTotal": 0,
    "lineItems": [line_items_example],
}

order_body_example: dict = {"lineItems": [{"productId": 0, "quantity": 0}]}

problem_detail_example: ProblemDetails = {
    "errors": {"name": "The name field is required."},
    "type": "https://testserver/problems/error/",
    "title": "One or more validation errors occurred.",
    "status": 400,
    "traceID": "00-f40e09a437a87f4ebcd2f39b128bb8f3-4b2ad798ac046140-00",
    "detail": "string",
    "instance": "string",
}
