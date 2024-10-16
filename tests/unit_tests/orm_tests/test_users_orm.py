from sqlalchemy.sql import text

from projects.domain.user import User


def test_users_mapper_can_load_users(db):
    db.session.execute(
        text( "INSERT into users (username, email ) VALUES "
            "('test-user-01', 'test-user-01@example.com'),"
            "('test-user-02', 'test-user-02@example.com'),"
            "('test-user-03', 'test-user-03@example.com')"
    )
    )
    expected = [
        User("test-user-01", "test-user-01@example.com"),
        User("test-user-02", "test-user-02@example.com"),
        User("test-user-03", "test-user-03@example.com"),
    ]
    assert db.session.query(User).all() == expected


def test_users_mapper_can_save_users(db):
    new_user = User("test-user-01", "test-user-01@example.com")
    db.session.add(new_user)
    db.session.commit()

    rows = list(db.session.execute(text('SELECT username, email FROM "users"')))
    assert rows == [("test-user-01", "test-user-01@example.com")]
