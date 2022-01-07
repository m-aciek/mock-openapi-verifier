from requests import Request, get
from openapi_core import create_spec

spec_dict = get('https://petstore3.swagger.io/api/v3/openapi.json').json()

spec = create_spec(spec_dict)

requests_request = Request(method='GET', url='https://petstore3.swagger.io/api/v3/pet/1')

from openapi_core.validation.request.validators import RequestValidator
from openapi_core.contrib.requests import RequestsOpenAPIRequest

openapi_request = RequestsOpenAPIRequest(requests_request)
validator = RequestValidator(spec)
result = validator.validate(openapi_request)

# raise errors if request invalid
result.raise_for_errors()

# get list of errors
errors = result.errors

print(result, errors)
