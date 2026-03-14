from django.test import TestCase
from django.urls import reverse

from .models import Task


class TaskModelTests(TestCase):
    def test_str_representation(self):
        task = Task(title="Test task")
        self.assertEqual(str(task), "… Test task")


class TaskViewTests(TestCase):
    def test_index_view_empty(self):
        response = self.client.get(reverse('tasks:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No tasks yet.")

    def test_add_task(self):
        response = self.client.post(reverse('tasks:index'), {'title': 'New task', 'description': 'detail'})
        self.assertRedirects(response, reverse('tasks:index'))
        self.assertEqual(Task.objects.count(), 1)
        task = Task.objects.first()
        self.assertEqual(task.description, 'detail')

    def test_complete_and_uncomplete(self):
        task = Task.objects.create(title='Work', description='work desc')
        self.client.get(reverse('tasks:complete', args=[task.id]))
        task.refresh_from_db()
        self.assertTrue(task.is_completed)
        self.client.get(reverse('tasks:uncomplete', args=[task.id]))
        task.refresh_from_db()
        self.assertFalse(task.is_completed)

    def test_delete_task(self):
        task = Task.objects.create(title='To be deleted')
        response = self.client.post(reverse('tasks:delete', args=[task.id]))
        self.assertRedirects(response, reverse('tasks:index'))
        self.assertEqual(Task.objects.count(), 0)
