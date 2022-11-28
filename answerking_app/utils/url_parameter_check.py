from rest_framework import status

from answerking_app.utils.mixins.ApiExceptions import ProblemDetails


def check_url_parameter(pk):
    try:
        if int(pk) < 1:
            raise ValueError
    except ValueError:
        raise ProblemDetails(
            status=status.HTTP_400_BAD_REQUEST,
            detail="Invalid parameters",
            title="Request has invalid parameters",
        )
