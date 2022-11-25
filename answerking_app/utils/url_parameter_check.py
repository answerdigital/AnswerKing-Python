from answerking_app.utils.mixins.ApiExceptions import BadInputParameter


def check_url_parameter(pk):
    try:
        if int(pk) < 1:
            raise ValueError
    except ValueError:
        raise BadInputParameter()
