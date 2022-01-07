import httpx
from openapi_core.validation.request.datatypes import OpenAPIRequest, RequestParameters
from openapi_core.validation.response.datatypes import OpenAPIResponse
from werkzeug.datastructures import Headers


class HttpxOpenAPIRequestFactory:
    @classmethod
    def create(cls, httpx_request: httpx.Request):
        return OpenAPIRequest(
            full_url_pattern=str(httpx_request.url),
            method=httpx_request.method.lower(),
            body=httpx_request.content.decode(),
            mimetype='',
            parameters=RequestParameters(),
        )


class HttpxOpenAPIResponseFactory:
    @classmethod
    def create(cls, httpx_response: httpx.Response):
        return OpenAPIResponse(
            data=httpx_response.content.decode(),
            status_code=httpx_response.status_code,
            mimetype='',
            headers=Headers(httpx_response.headers),
        )
