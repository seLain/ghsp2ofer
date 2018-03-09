import logging
from github import Github
import settings

logger = logging.getLogger(__name__)

class Bot(object):

	def __init__(self):
		self.github = None

	def login(self, token=None):
		if token:
			self.github = Github(token)
		else:
			self.github = Github(settings.ACCESS_TOKEN)

	def get_repo_names(self):
		return [r.name for r in self.github.get_user().get_repos()]

	def create_issue(self, repo_name, issue):
		repo = self.github.get_user().get_repo(name=repo_name)
		repo.create_issue(title=issue['title'], body=issue['body'])

	# param state:: 'open', 'closed', 'all'
	def get_issues(self, repo_name, state='open'):
		repo = self.github.get_user().get_repo(name=repo_name)
		return repo.get_issues(state=state)