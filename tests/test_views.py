from django.urls import reverse

QUESTION_ID = 62991161


class TestHomepage:

    def test_get_all_list(self, client, db):
        url = reverse('home')
        response = client.get(url)
        assert response.status_code == 200

    def test_get_python_list(self, client, db):
        url = reverse('home')
        response = client.get(url, data={'tagged': 'python'})
        assert response.status_code == 200
        assert 'python' in str(response.content)

    def test_get_question_details(self, client, db):
        url = reverse('details', args=[QUESTION_ID])
        response = client.get(url)
        assert response.status_code == 200
