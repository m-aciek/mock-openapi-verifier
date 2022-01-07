from openapi_core.validation.request.datatypes import OpenAPIRequest, RequestParameters
from openapi_core.validation.response.datatypes import OpenAPIResponse
from werkzeug.datastructures import Headers


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
