from django.db import models
import time

class User(models.Model):
    user_id = models.CharField(primary_key=True, default=str(int(time.time())), max_length=12, editable=False)
    user_data = models.JSONField(default=dict)


class Flag(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    user_flags = models.JSONField(default=dict)


# class Whatsapp(models.Model):
#     user_id = models.ForeignKey(User, on_delete=models.CASCADE, primary_key=True)
#     client_details = models.JSONField(default=dict)