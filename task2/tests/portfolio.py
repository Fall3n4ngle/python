from .base import BaseTestCase

class PortfolioTests(BaseTestCase):
    def test_portfolio_route(self):
        response = self.client.get('/portfolio', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'I am a Software Developer', response.data)  

    def test_contact_route(self):
        response = self.client.get('/portfolio/contact', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Send Me Message', response.data)  

    def test_skills_route(self):
        response = self.client.get('/portfolio/skills/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'CSS', response.data) 