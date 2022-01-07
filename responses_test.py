import responses
from openapi_core.validation.request.datatypes import OpenAPIRequest, RequestParameters
from openapi_core.validation.response.datatypes import OpenAPIResponse
from requests import get
from openapi_core import create_spec

from werkzeug.datastructures import Headers

spec_dict = get('https://petstore3.swagger.io/api/v3/openapi.json').json()

spec = create_spec(spec_dict)

resp = responses.Response(
    responses.GET,
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
from openapi_core.validation.request.validators import RequestValidator

validator = RequestValidator(spec)


class ResponsesOpenAPIRequestFactory:
    @classmethod
    def create(cls, responses_response: responses.Response):
        return OpenAPIRequest(
            full_url_pattern=responses_response.url,
            method=responses_response.method.lower(),
            body='',
            mimetype='',
            parameters=RequestParameters(),
        )


class ResponsesOpenAPIResponseFactory:
    @classmethod
    def create(cls, responses_response: responses.Response):
        return OpenAPIResponse(
            data=responses_response.body,
            status_code=responses_response.status,
            mimetype=responses_response.content_type,
            headers=Headers(responses_response.headers),
        )


openapi_request = ResponsesOpenAPIRequestFactory.create(resp)
result = validator.validate(openapi_request)

# raise errors if request invalid
result.raise_for_errors()

# get list of errors
errors = result.errors

# get parameters object with path, query, cookies and headers parameters
validated_params = result.parameters
# or specific location parameters
validated_path_params = result.parameters.path

# get body
validated_body = result.body

# get security data
validated_security = result.security

from openapi_core.validation.response.validators import ResponseValidator

validator = ResponseValidator(spec)
openapi_response = ResponsesOpenAPIResponseFactory.create(resp)
result = validator.validate(openapi_request, openapi_response)

# raise errors if response invalid
result.raise_for_errors()

# get list of errors
errors = result.errors

# get headers
validated_headers = result.headers

# get data
validated_data = result.data
