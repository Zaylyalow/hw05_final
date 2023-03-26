from django.contrib.auth import get_user_model
from django.db import models

from core.models import CreatedModel

User = get_user_model()


class Group(models.Model):
    title = models.CharField(
        max_length=200,
        db_index=True,
        verbose_name="Заголовок")
    slug = models.SlugField(
        max_length=255,
        unique=True,
        verbose_name="Адрес")
    description = models.TextField(
        verbose_name="Описание")

    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"

    def __str__(self):
        return self.title


class Post(CreatedModel):
    text = models.TextField(
        verbose_name="Текст",
        help_text='Введите текст поста')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name="Автор")
    group = models.ForeignKey(
        Group,
        related_name='posts',
        on_delete=models.SET_NULL,
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Сообщество",
        help_text='Выберите подходящую группу')
    image = models.ImageField(
        upload_to='posts/',
        blank=True,
        verbose_name="Картинка")

    class Meta:
        ordering = ('-created',)
        verbose_name = "Пост"
        verbose_name_plural = "Посты"

    def __str__(self):
        return self.text


class Comment(CreatedModel):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Запись')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор')
    text = models.TextField(
        verbose_name='Комментарий',
        help_text='Текст комментария')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-created',)

    def __str__(self):
        return self.text[:15]


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='подписчик'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ('author',)
        constraints = (models.UniqueConstraint(
            fields=['author', 'user'],
            name='unique_follow'
        ),)
