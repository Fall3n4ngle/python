from .base import BaseTestCase
from extensions import db
from app.todo.models import Todo

class TodoTests(BaseTestCase):
    def setUp(self):
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_todo(self):
        response = self.client.post('/todo/', data=dict(title='Test Task'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Task', response.data)

    def test_read_todo_list(self):
        todo = Todo(title='Read Test Task', complete=False)
        db.session.add(todo)
        db.session.commit()

        response = self.client.get('/todo/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Read Test Task', response.data)

    def test_update_todo_status(self):
        todo = Todo(title='Update Test Task', complete=False)
        db.session.add(todo)
        db.session.commit()

        response = self.client.get(f'/todo/update/{todo.id}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Completed', response.data)

    def test_delete_todo(self):
        todo = Todo(title='Delete Test Task', complete=False)
        db.session.add(todo)
        db.session.commit()

        response = self.client.get(f'/todo/delete/{todo.id}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'Delete Test Task', response.data)