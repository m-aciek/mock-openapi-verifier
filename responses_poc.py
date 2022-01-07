import pickle

# from openapi_core import create_spec, RequestValidator, ResponseValidator
from requests import get
from responses import add as original_add
import responses
from responses_test import (
    ResponsesOpenAPIResponseFactory,
    ResponsesOpenAPIRequestFactory,
)

# spec_dict = get('https://petstore3.swagger.io/api/v3/openapi.json').json()
#
# spec = create_spec(spec_dict)
#
# request_validator = RequestValidator(spec)
# response_validator = ResponseValidator(spec)


def new_add(*args, **kwargs):
    print(args, kwargs)
    response = Response(*args, **kwargs)
    request = ResponsesOpenAPIRequestFactory.create(response)
    openapi_response = ResponsesOpenAPIResponseFactory.create(response)
    with open('.compliance', 'wb') as file:
        pickle.dump((request, openapi_response), file)
    # request_validator.validate(request).raise_for_errors()
    # response_validation = response_validator.validate(request, openapi_response)
    return original_add(*args, **kwargs)


responses.add = new_add
from responses import GET, Response, activate, add, calls


@activate
def test_simple():
    add(
        GET,
        'https://petstore3.swagger.io/api/v3/pet/10',
        json={
            "id": 10,
            "name": "doggie",
            "category": {"id": 1, "name": "Dogs"},
            "photoUrls": ["string"],
            "tags": [{"id": 0, "name": "string"}],
            "status": "available",
        },
        status=200,
    )

    resp = get('https://petstore3.swagger.io/api/v3/pet/10')

    assert resp.json() == {
        "id": 10,
        "name": "doggie",
        "category": {"id": 1, "name": "Dogs"},
        "photoUrls": ["string"],
        "tags": [{"id": 0, "name": "string"}],
        "status": "available",
    }

    assert len(calls) == 1
    assert calls[0].request.url == 'https://petstore3.swagger.io/api/v3/pet/10'
    assert calls[0].response.json() == {
        "id": 10,
        "name": "doggie",
        "category": {"id": 1, "name": "Dogs"},
        "photoUrls": ["string"],
        "tags": [{"id": 0, "name": "string"}],
        "status": "available",
    }


test_simple()
