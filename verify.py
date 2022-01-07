import pickle

from openapi_core import create_spec, RequestValidator, ResponseValidator
from requests import get


def generate_spec_url_candidates(full_url_pattern: str):
    full_url_pattern = full_url_pattern.removeprefix('https://')
    end = len(full_url_pattern)
    while (index := full_url_pattern.rfind('/', 0, end)) != -1:
        end = index
        yield f'https://{full_url_pattern[: index]}/openapi.json'


with open('.compliance', 'rb') as file:
    request, response = pickle.load(file)

cand = generate_spec_url_candidates(request.full_url_pattern)
spec_dict = get([c for c in cand][1]).json()
spec = create_spec(spec_dict)

request_validator = RequestValidator(spec)
response_validator = ResponseValidator(spec)

print(request_validator.validate(request).errors)
print(response_validator.validate(request, response).errors)
