import pytest


@pytest.mark.preference_api
class TestPreferenceApi:
    """
    Test class to verify CRUD /preference API endpoints
    """

    @classmethod
    def setup_class(cls):
        #TODO: write test setup
        pass

    @pytest.mark.create
    def test_create(self):
        pass

    @pytest.mark.read
    def test_read(self):
        pass

    @pytest.mark.update
    def test_update(self):
        pass

    @pytest.mark.delete
    def test_delete(self):
        pass

    @classmethod
    def teardown_class(cls):
        #TODO: teardown the setup
        pass

