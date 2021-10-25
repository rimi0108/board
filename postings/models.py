from django.db import models

class Posting(models.Model):
    content   = models.CharField(max_length=1000, unique=True)
    image_url = models.URLField(max_length=1000)
    user_id   = models.ForeignKey('users.user', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'postings'
