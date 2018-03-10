import time, pathlib, os
from unittest import TestCase
from bot import Bot
import settings
from exceptions import ClonedRepoExistedError

class BotTestCase(TestCase):

	def setUp(self):
		# set up needed testing data folder
		pathlib.Path('/test_data').mkdir(parents=True, exist_ok=True)
		# set up bot instance
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

	def test_repo_clone(self):
		expected_dir = os.sep.join(['.pytest_data', settings.DEFAULT_REPO])
		# make sure the clone dir does not exist yet
		self.assertEqual(os.path.isdir(expected_dir), False)
		self.bot.repo_clone(repo_name=settings.DEFAULT_REPO, root_dir='.pytest_data')
		self.assertEqual(os.path.isdir(expected_dir), True)
		# test if expected_dir exist already. if yes, ClonedRepoExistedError should be thrown
		try:
			self.bot.repo_clone(repo_name=settings.DEFAULT_REPO, root_dir='.pytest_data')
		except ClonedRepoExistedError:
			self.assertEqual(True, True)