import pytest
import random

@pytest.mark.flaky(reruns=2)
def test_3():
    assert True


class TestA(object):

    @pytest.mark.flaky(reruns=3)
    def test_1(self):
        assert random.randint(0,1)

    def test_2(self):
        assert random.randint(0,1)

    @pytest.mark.skip
    def test_3(self):
        assert True

    def test_4(self):
        assert True

    def test_5(self):
        assert True

    def test_6(self):
        assert True

    def test_7(self):
        assert True