from django.db import models

class Rating(models.Model):
    # レーティングのフィールドを定義する
    # 例: value = models.IntegerField()
    
    
    def __str__(self):
        return f"Rating: {self.value}"