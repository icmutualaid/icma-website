# The init-db command should call the init_db function and output a message.
def test_init_db_command(runner, monkeypatch):
    class Recorder(object):
        called = False

    def fake_init_db():
        Recorder.called = True

    monkeypatch.setattr('blog.db.init_db', fake_init_db)
    result = runner.invoke(args=['init-db'])
    assert 'Initialized' in result.output
    assert Recorder.called


# The create-user command should call create_user.
def test_create_user(runner, monkeypatch, app):
    class Recorder(object):
        called = False

    def fake_create_user(*_):
        Recorder.called = True

    monkeypatch.setattr('blog.auth.create_user', fake_create_user)

    with app.app_context():
        runner.invoke(args=['create-user', 'test-user', 'test-pass'])

    assert Recorder.called
