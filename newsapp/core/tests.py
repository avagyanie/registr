from django.test import TestCase
from .models import Team, News
from datetime import datetime
from django.contrib.auth import get_user_model


User = get_user_model

# Create your tests here.
class TeamTestCase(TestCase):
    def setUp(self) -> None:
        self.team = Team.objects.create(team_member="only a test", position="yes, this is only a test", description ="description")

    def test_team_str(self):
        self.assertEqual(str(self.team), self.team.team_member)

    def test_team_description(self):
        self.assertEqual("description", self.team.description)

    def tearDown(self) -> None:
        del self.team


class NewsTestCase(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(username = "Info", email = "infopulse@gmail.com", password = "1234567")
        self.first_news = News.objects.create(date = datetime.now(), title = "test", description = "desc", news_type = "1", user = self.user)

    def test_news_str(self):
        pass

    def test_news_description(self):
        pass

    def tearDown(self) -> None:
        del self.user
        del self.first_news
 