from django.db import models

# Create your models here.

class Task(models.Model):
    """Represents a to-do task that can be pending or completed."""

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        status = "✓" if self.is_completed else "…"
        return f"{status} {self.title}"

    class Meta:
        ordering = ['-created_at']
