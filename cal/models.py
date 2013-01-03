from django.db import models


class Calendar(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    public = models.BooleanField(default=False)

    def to_hash(self):
        return {'id': self.id, 'public': self.public}


class Todo(models.Model):
    calendar = models.OneToOneField(Calendar)
    created_on = models.DateTimeField(auto_now_add=True)
    start = models.DateTimeField()
    # For now lets allow null values here since we are not considering due dates
    end = models.DateTimeField(null=True)
    title = models.CharField(max_length=30)
    done = models.BooleanField(default=False)

    def to_hash(self, ignore_cal=False):
        return dict({'id': self.id,
          'title': self.title,
          'start': self.start.isoformat(),
          'end': self.end.isoformat() if self.end else None,
          'done': self.done,
          }.items() +
          ({'calendar': self.calendar.to_hash()}.items() if not ignore_cal else []))
