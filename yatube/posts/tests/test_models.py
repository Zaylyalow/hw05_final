from django.test import TestCase

from ..models import Group, Post, User


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user = User.objects.create_user(username='testAuthor')

        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            group=cls.group,
            text='Длинное сообщение',
        )

    def test_model_post_have_correct_str_text(self):
        """Проверка работоспособности __str__ у модели Post."""
        self.assertEqual(
            str(PostModelTest.post),
            PostModelTest.post.text[:30],
        )

    def test_model_group_have_correct_str_title(self):
        """Проверка работоспособности __str__ у модели Group."""
        group = PostModelTest.group
        group_title = group.title
        self.assertEqual(str(group), group_title)

    def test_post_verbose_name(self):
        """Проверка verbose_name в полях модели Post
        совпадает с ожидаемым."""
        post = PostModelTest.post
        field_verboses = {
            'text': 'Текст',
            'created': 'Дата создания',
            'author': 'Автор',
            'group': 'Сообщество',
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    post._meta.get_field(value).verbose_name,
                    expected
                )

    def test_group_verbose_name(self):
        """Проверка verbose_name в полях модели Group
        совпадает с ожидаемым."""
        group = PostModelTest.group
        field_verboses = {
            'title': 'Заголовок',
            'slug': 'Адрес',
            'description': 'Описание',
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    group._meta.get_field(value).verbose_name,
                    expected
                )

    def test_post_help_text(self):
        """Проверка help_text в полях модели Post
        совпадает с ожидаемым."""
        post = PostModelTest.post
        field_help = {
            'text': 'Введите текст поста',
            'group': 'Выберите подходящую группу'
        }
        for value, expected in field_help.items():
            with self.subTest(value=value):
                self.assertEqual(
                    post._meta.get_field(value).help_text,
                    expected
                )
