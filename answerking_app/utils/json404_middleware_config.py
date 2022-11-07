from django.http import JsonResponse


def json404_response(request):

    data = {
        "detail": "not found",
        "title": "Not found.",
        "status": 404,
        "type": "{}://{}/problems/not_found/",
    }
    data["type"] = data["type"].format(request.scheme, request.get_host())
    return JsonResponse(
        data, content_type="application/problem+json", status=404
    )
