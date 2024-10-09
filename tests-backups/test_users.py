from sqlalchemy.sql import text

from projects.domain.user import User
#from projects.entrypoints.flask import db


#def test_user_model(session):
#    user = User("test-user-01", "test-user-01@example.com")
#    session.add(user)
#    session.commit()
#    assert user.id > 0

#   http -A bearer --auth 84cf0a9a4a681a8902dfa7e8e9d5a2d4 
#       POST http://localhost:8034/api/users username=test-user-03 password=secret email=test-user-03@kalinsky.me
"""

def test_add_user(session, client, app):
    #assert client.get("/api/users").status_code == 200

    # test that successful registration redirects to the login page
    response = client.post("/api/users", data={"username": "u", "password": "secret", "email": "u@example.com"})
    print(vars(response))
    #assert response.headers["Location"] == "/auth/login"

    # test that the user was inserted into the database
    with app.app_context():
        select = session.select(User).filter_by(username="u")
        user = session.execute(select).scalar()
        assert user is not None
"""

def test_get_manager(test_client, manager_user):
    resp = test_client.get("/api/users/user-by-username/manager1")
    assert resp.json["email"] == manager_user.email

def test_password_hashing():
        u = User(username='susan', email='susan@example.com')
        u.set_password('cat')
        assert not u.check_password('dog')
        assert u.check_password('cat')


def test_add_user(test_client, database):
    #assert client.get("/api/users").status_code == 200

    response = test_client.post("/api/users", data={"username": "u", "password": "secret", "email": "u@example.com"})
    print(vars(response))

    #import ipdb;ipdb.set_trace()
    user = database.session.query(User).filter_by(username="u").one()
    assert user is not None

#def test_user_password():
#    user = User(username="a", email="t@email.com", password="a")
#    assert user.password_hash != "a"
#    assert user.check_password("a")

#def test_a_transaction_using_engine(db_engine):
#    with db_engine.begin() as conn:
#        row = conn.execute('''UPDATE table SET name = 'testing' WHERE id = 1''')

#def test_transaction_doesnt_persist(db_engine):
#    row_name = db_engine.execute('''SELECT name FROM table WHERE id = 1''').fetchone()[0]
#    assert row_name != 'testing'
