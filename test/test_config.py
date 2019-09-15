import json
from src.spec import spec


def test_spec():
    with open('spec.json', 'r') as f:
        new_spec = json.load(f)
    assert spec == new_spec
