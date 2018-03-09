import time
from unittest import TestCase
from bot import Bot
import settings

class BotTestCase(TestCase):

	def setUp(self):
		self.bot = Bot()
		self.bot.login()

	def test_get_repo_names(self):
		self.assertEqual(settings.DEFAULT_REPO in self.bot.get_repo_names(), True)
		self.assertEqual('MadeUpRepo' in self.bot.get_repo_names(), False)

	def test_create_issue_get_issues(self):
		issue = {'title': 'test issue',
				 'body': 'this is a test issue.'}
		self.bot.create_issue(settings.DEFAULT_REPO, issue)
		existing_issues = self.bot.get_issues(settings.DEFAULT_REPO, state='open')
		self.assertEqual(issue['title'] in [i.title for i in existing_issues], True)
		self.assertEqual(issue['body'] in [i.body for i in existing_issues], True)