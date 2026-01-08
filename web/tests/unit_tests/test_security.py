import pytest

from app.core.security import FullPayload, create_access_token, decode_access_token

data_parametrize = pytest.mark.parametrize(
    ['data', 'expected'],
    [
        ({'sub': "10", 'exp': 9999}, {"sub": "10", 'exp': 9999})
    ]
)


@data_parametrize
def test_same_jwt_encode(data, expected):
    data_schema = FullPayload(**data)
    assert expected == data_schema.model_dump()
    assert create_access_token(data) == create_access_token(data_schema)


@data_parametrize
def test_encode_decode(data, expected):
    token_dict = create_access_token(data)
    decoded_data = decode_access_token(token_dict["access_token"])
    assert decoded_data["sub"] == expected["sub"]


def test_match_payload_structure():
    with pytest.raises(TypeError, match="Payload must be of type dict with filled data or Payload with filled data"):
        create_access_token(None)
