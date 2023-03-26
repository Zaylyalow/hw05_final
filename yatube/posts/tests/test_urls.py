from http import HTTPStatus

from django.test import Client, TestCase

from ..models import Group, Post, User


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.author = User.objects.create_user(username='testAuthor')

        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.author,
            text='Длинное сообщение',
        )

        cls.INDEX = '/'
        cls.GROUP_POSTS = f'/group/{cls.group.slug}/'
        cls.PROFILE = f'/profile/{cls.author.username}/'
        cls.POST_DETAIL = f'/posts/{cls.post.id}/'
        cls.NON_EXISTING_PAGE = '/existing_page/'
        cls.CREATE = '/create/'
        cls.EDIT = f'/posts/{cls.post.id}/edit/'
        cls.CREATE_REVERSE = '/auth/login/?next=/create/'
        cls.EDIT_REVERSE = f'/auth/login/?next=/posts/{cls.post.id}/edit/'
        # added
        cls.COMMENT = f'/posts/{cls.post.id}/comment/'
        cls.FOLLOW_INDEX = '/follow/'
        cls.FOLLOW = f'/profile/{cls.author.username}/follow/'
        cls.UNFOLLOW = f'/profile/{cls.author.username}/unfollow/'

    def setUp(self):
        self.author_client = Client()
        self.author_client.force_login(self.author)
        self.user = User.objects.create_user(username='testAuthorized')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.other_author = User.objects.create_user(username='OtherAuthor')
        self.other_author_client = Client()
        self.other_author_client.force_login(self.other_author)

        self.public_urls = [
            (PostURLTests.INDEX, 'posts/index.html'),
            (PostURLTests.GROUP_POSTS, 'posts/group_list.html'),
            (PostURLTests.PROFILE, 'posts/profile.html'),
            (PostURLTests.POST_DETAIL, 'posts/post_detail.html'),
        ]

        self.private_urls = [
            (PostURLTests.CREATE, 'posts/create_post.html'),
            (PostURLTests.EDIT, 'posts/create_post.html'),
            (PostURLTests.FOLLOW_INDEX, 'posts/follow.html'),
        ]

    def test_existing_pages(self):
        """Проверка существования и доступности страниц любому пользователю."""
        for url, _ in self.public_urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(
                    response.status_code,
                    HTTPStatus.OK
                )

    def test_unexisting_page(self):
        """Проверка запроса на ошибку 404 к несуществующей странице."""
        response = self.client.get(PostURLTests.NON_EXISTING_PAGE)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_authorized_client_creates_post(self):
        """Проверка на создание записи авторизованным пользователем."""
        response = self.authorized_client.get(PostURLTests.CREATE)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_create_url_redirect_anonymous_on_login(self):
        """Проверка перенаправления анонимного пользователя
        со сраницы /posts/create/ на страницу /login/."""
        response = self.client.get(PostURLTests.CREATE)
        self.assertRedirects(response, PostURLTests.CREATE_REVERSE)

    def test_only_author_edites_post(self):
        """Проверка на корректность и доступность страницы
        /posts/<int:post_id>/edit/ автору."""
        response = self.author_client.get(PostURLTests.EDIT)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'posts/create_post.html')

    def test_post_edit_url_redirect_anonymous_on_login(self):
        """Проверка перенаправления анонимного пользователя
        со сраницы /posts/<int:post_id>/edit/ на страницу /login/."""
        response = self.client.get(PostURLTests.EDIT)
        self.assertRedirects(response, PostURLTests.EDIT_REVERSE)

    def test_post_edit_url_redirect_authorized_on_post_detail(self):
        """Проверка перенаправления авторизованного пользователя со сраницы
        /posts/<int:post_id>/edit/ на страницу /posts/<int:post_id>/."""
        response = self.authorized_client.get(PostURLTests.EDIT)
        self.assertRedirects(response, PostURLTests.POST_DETAIL)

    def test_post_edit_url_redirect_other_author_on_post_detail(self):
        """Проверка перенаправления другого автора со сраницы
        /posts/<int:post_id>/edit/ на страницу /posts/<int:post_id>/."""
        self.other_post = Post.objects.create(
            author=self.other_author,
            text='Длинное сообщение2',
        )
        response = self.other_author_client.get(PostURLTests.EDIT)
        self.assertRedirects(response, PostURLTests.POST_DETAIL)

    def test_accordance_urls_templates(self):
        """Проверка cоответствия адресов и шаблонов."""
        for url, template in self.private_urls + self.public_urls:
            with self.subTest(url=url):
                response = self.author_client.get(url)
                self.assertTemplateUsed(
                    response,
                    template
                )

    def test_COMMENT_url_exists_at_desired_location(self):
        """Проверка доступности адреса COMMEN."""
        response = self.author_client.get(self.COMMENT)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_FOLLOW_url_exists_at_desired_location(self):
        """Проверка доступности адреса FOLLOW."""
        response = self.author_client.get(self.FOLLOW)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_UNFOLLOW_url_exists_at_desired_location(self):
        """Проверка доступности адреса UNFOLLOW."""
        response = self.author_client.get(self.UNFOLLOW)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
