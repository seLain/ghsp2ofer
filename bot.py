import os, logging
from github import Github
from git import Repo
from git.exc import GitCommandError
from exceptions import ClonedRepoExistedError
import settings

logger = logging.getLogger(__name__)

class Bot(object):

	def __init__(self):
		self.github = None
		self.url = None

	def login(self, token=None):
		if token:
			self.github = Github(token)
		else:
			self.github = Github(settings.ACCESS_TOKEN)
		# update self.url
		self.url = self.github.get_user().url

	def get_repo_names(self):
		return [r.name for r in self.github.get_user().get_repos()]

	def create_issue(self, repo_name, issue):
		repo = self.github.get_user().get_repo(name=repo_name)
		repo.create_issue(title=issue['title'], body=issue['body'])

	# param state:: 'open', 'closed', 'all'
	def get_issues(self, repo_name, state='open'):
		repo = self.github.get_user().get_repo(name=repo_name)
		return repo.get_issues(state=state)

	def report_status(self, repo_name):
		repo = self.github.get_user().get_repo(name=repo_name)
		return '\n'.join([
					'Bot connected to repository: %s' % repo.full_name,
					'    clone_url: %s' % repo.clone_url
				])

	def repo_clone(self, repo_name, root_dir):
		repo = self.github.get_user().get_repo(name=repo_name)
		repo_dir = os.sep.join([root_dir, repo_name])
		try:
			Repo.clone_from(repo.clone_url, repo_dir)
		except GitCommandError:
			raise ClonedRepoExistedError


if __name__ == "__main__":
	bot = Bot()
	bot.login()
	print(bot.report_status(repo_name=settings.DEFAULT_REPO))
	bot.repo_clone(repo_name=settings.DEFAULT_REPO, root_dir=settings.DEFAULT_CLONE_ROOT_DIR)