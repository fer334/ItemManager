from django.urls import reverse, resolve


class TestUrls:

    def test_index_url(self):
            path = reverse('login:index')
            assert resolve(path).view_name == 'login:index'