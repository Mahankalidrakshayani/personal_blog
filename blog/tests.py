from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from blog.models import Category, Tag, Post, Comment, Profile


class BlogModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testauthor', password='password123')
        self.category = Category.objects.create(name='Python & AI')

    def test_category_slug_auto_generation(self):
        self.assertEqual(self.category.slug, 'python-ai')

    def test_post_creation_and_reading_time(self):
        content = " ".join(["word"] * 450)  # 450 words -> 3 min read
        post = Post.objects.create(
            title='My First Test Post',
            author=self.user,
            category=self.category,
            content=content,
            status='published'
        )
        self.assertEqual(post.slug, 'my-first-test-post')
        self.assertEqual(post.reading_time, 3)

    def test_slug_uniqueness_on_conflict(self):
        p1 = Post.objects.create(title='Unique Title', author=self.user, content='Content 1', status='published')
        p2 = Post.objects.create(title='Unique Title', author=self.user, content='Content 2', status='published')
        self.assertEqual(p1.slug, 'unique-title')
        self.assertEqual(p2.slug, 'unique-title-1')

    def test_profile_auto_creation_signal(self):
        new_user = User.objects.create_user(username='signals_user', password='pass')
        self.assertTrue(hasattr(new_user, 'profile'))


class BlogViewPermissionsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.author1 = User.objects.create_user(username='author1', password='pass1')
        self.author2 = User.objects.create_user(username='author2', password='pass2')
        self.category = Category.objects.create(name='Web Development')
        
        # Published post by author1
        self.pub_post = Post.objects.create(
            title='Published Post',
            author=self.author1,
            category=self.category,
            content='This is a public post available to everyone.',
            status='published'
        )

        # Draft post by author1
        self.draft_post = Post.objects.create(
            title='Draft Secret Post',
            author=self.author1,
            category=self.category,
            content='This is a draft post for author eyes only.',
            status='draft'
        )

    def test_homepage_loads(self):
        response = self.client.get(reverse('blog:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Published Post')

    def test_published_post_accessible_by_guest(self):
        response = self.client.get(reverse('blog:post_detail', kwargs={'slug': self.pub_post.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.pub_post.title)

    def test_draft_post_not_accessible_by_guest(self):
        response = self.client.get(reverse('blog:post_detail', kwargs={'slug': self.draft_post.slug}))
        # Redirects to home with warning message
        self.assertEqual(response.status_code, 302)

    def test_draft_post_accessible_by_author(self):
        self.client.login(username='author1', password='pass1')
        response = self.client.get(reverse('blog:post_detail', kwargs={'slug': self.draft_post.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Draft Mode Active')

    def test_author_cannot_edit_other_author_post(self):
        self.client.login(username='author2', password='pass2')
        response = self.client.get(reverse('blog:post_edit', kwargs={'slug': self.pub_post.slug}))
        # Redirects to dashboard with permission denied message
        self.assertEqual(response.status_code, 302)

    def test_author_can_edit_own_post(self):
        self.client.login(username='author1', password='pass1')
        response = self.client.get(reverse('blog:post_edit', kwargs={'slug': self.pub_post.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Edit Post')

    def test_comment_submission_by_logged_in_user(self):
        self.client.login(username='author2', password='pass2')
        response = self.client.post(
            reverse('blog:post_detail', kwargs={'slug': self.pub_post.slug}),
            {'content': 'Fascinating article!'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comment.objects.filter(post=self.pub_post).count(), 1)
        comment = Comment.objects.first()
        self.assertEqual(comment.author, self.author2)
        self.assertEqual(comment.content, 'Fascinating article!')

    def test_search_filtering(self):
        response = self.client.get(reverse('blog:post_list'), {'q': 'Public'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Published Post')

    def test_dashboard_metrics(self):
        self.client.login(username='author1', password='pass1')
        response = self.client.get(reverse('blog:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Published Post')
        self.assertContains(response, 'Draft Secret Post')
