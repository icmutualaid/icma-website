from blog import create_app


# If config is not passed, there should be some default configuration,
# otherwise the configuration should be overridden.
def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing
