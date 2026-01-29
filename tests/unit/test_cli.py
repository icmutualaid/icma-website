# The create-user command should call create_user.
def test_create_user(runner, monkeypatch, app):
    class Recorder(object):
        called = False

    def fake_create_user(*_):
        Recorder.called = True

    monkeypatch.setattr('blog.cli.create_user', fake_create_user)

    with app.app_context():
        runner.invoke(args=['create-user', 'test-user', 'test-pass'])

    assert Recorder.called
