import pytest

from app.core.security import FullPayload, create_access_token, decode_access_token

data = pytest.param([
    ({'sub': 10, 'exp': 9999}, )
])


# @pytest.mark.parametrize('data', [
#     {
#         'sub': 10,
#         'exp': 999999
#     },
# ])
def test_same_jwt_encode(data):
    data_schema = FullPayload(**data)
    assert data == data_schema.model_dump()
    assert create_access_token(data) == create_access_token(data_schema)


def test_encode_decode(data):
    token = create_access_token(data)
    decoded_data = decode_access_token(token)
    assert data == decoded_data

def test_match_payload_structure():
    with pytest.raises(TypeError, "Payload must be of type dict with filled data or Payload with filled data"):
        create_access_token()