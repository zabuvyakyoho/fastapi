from httpx import request
from sqlalchemy.pool import StaticPool
from sqlalchemy import create_engine, text
from TodoApp.routers.auth import get_current_user, get_db
from ..database import Base, sessionmaker
from ..main import app
from fastapi.testclient import TestClient
from fastapi import status
import pytest
from ..models import Todos


SQLALCHEMY_DATABASE_URL = "sqlite:///./testdb.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass = StaticPool,
)


TestingSessoinLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def get_test_db():
    db = TestingSessoinLocal()
    try:
        yield db
    finally:
        db.close()

def override_get_current_user():
    return {'username': 'sasha', 'id': 2, 'user_role': 'admin'}

app.dependency_overrides[get_db] = get_test_db
app.dependency_overrides[get_current_user] = override_get_current_user


client = TestClient(app)

@pytest.fixture
def test_todo():
    todo = Todos(
        title='Learn to code!',
        description='Need to learn everyday!',
        priority=5,
        complete=False,
        owner_id=2,
    )
    
    db = TestingSessoinLocal()
    db.add(todo)
    db.commit()
    
    data_dict = {column.name: getattr(todo, column.name) for column in Todos.__table__.columns}
    print('before: ', data_dict)

    yield todo

    data_dict = {column.name: getattr(todo, column.name) for column in Todos.__table__.columns}
    print('after :', data_dict)

@pytest.fixture(autouse=True)
def clear_db():
    with engine.connect() as connection:
        connection.execute(text('DELETE FROM TODOS;'))
        connection.commit()

def test_read_one_authenticated(test_todo):
    response = client.get("/todos/todo/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
                'title': 'Learn to code!', 
                'description': 'Need to learn everyday!', 
                'priority': 5, 
                'complete': False, 
                'owner_id': 2
    }


def test_read_one_authenticated_not_found():
    response = client.get("/todos/todo/99")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Todo not found'}


def  test_create_todo(test_todo):
    request_data={
        'title': 'New Todo!',
        'description': 'New todo description',
        'priority': 5,
        'complete': False
    }

    response = client.post('/todos/todo/', json=request_data)
    assert response.status_code == 201

    db = TestingSessoinLocal()
    model = db.query(Todos).order_by(Todos.id.desc()).first()
    assert model.title == request_data.get('title')
    assert model.description == request_data.get('description')
    assert model.priority == request_data.get('priority')
    assert model.complete == request_data.get('complete')


def test_update_todo(test_todo):
    request_data={
        'title': 'Change the title of the todo already saved',
        'description': 'Need to learn everyday!',
        'priority': 5,
        'complete': False,
    }

    response = client.put('/todos/todo/1', json=request_data)
    assert response.status_code == 204
    db = TestingSessoinLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model.title == 'Change the title of the todo already saved'
