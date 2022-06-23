import pytest
from src.db import DisorderDB

class TestBasicThings:
    def func(self, x):
        return x + 1

    def test_answer(self):
        assert self.func(3) == 4

@pytest.fixture
def db():
    return DisorderDB('db/test.db')