from django.db import models

class Blog(models.Model):
    # Указываем на автора
    # Ссылаемся на таблицу с пользователями
    # При удалении автора автоматически удаляются все посты
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.TextField(max_length=100)
    text = models.TextField(max_length=500)
    
class Comment(models.Model):
    # Указываем на конкретный пост
    # Ссылаемся на таблицу с блогами
    # При удалении поста автоматически удаляются все комментарии
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    text = models.TextField(max_length=100)