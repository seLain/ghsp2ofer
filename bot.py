import os, logging, shutil, glob, random, time
from datetime import datetime, timedelta
from github import Github, InputGitTreeElement
from git import Repo
from git.exc import GitCommandError
from exceptions import ClonedRepoExistedError, BranchUpToDateException, DefaultCommitToolException
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

	def remote_addfiles_commit(self, repo_name, file_list, message=''):
		# load repo and get meta
		repo = self.github.get_user().get_repo(name=repo_name)
		master_ref = repo.get_git_ref('heads/master')
		master_sha = master_ref.object.sha
		base_tree = repo.get_git_tree(master_sha)
		# enroll the files to be committed
		element_list = list()
		for entry in file_list:
			with open(os.sep.join([settings.DEFAULT_SOURCE_ROOT_DIR, repo_name, entry]), 'r') as input_file:
				data = input_file.read()
			element = InputGitTreeElement(entry.replace('\\', '/'), '100644', 'blob', data)
			element_list.append(element)
		# prepare commit trees and make commit request
		tree = repo.create_git_tree(element_list, base_tree)
		parent = repo.get_git_commit(master_sha)
		commit = repo.create_git_commit(message, tree, [parent])
		master_ref.edit(commit.sha)

	def addfiles_commit_push_remote(self, repo_name, root_dir, file_list, message='', remote_name='origin'):
		# load repo
		repo_dir = os.sep.join([root_dir, repo_name])
		repo = Repo(repo_dir)
		# copy and add files specified to local repository
		for file in file_list:
			src = os.sep.join([settings.DEFAULT_SOURCE_ROOT_DIR, repo_name, file])
			dest = os.sep.join([repo_dir, file])
			try:
				shutil.copy2(src, dest)
				repo.git.add(file)
			except IOError as e: # parent directory not exists or something wrong
				# creating parent directories
				os.makedirs(os.path.dirname(dest))
				shutil.copy2(src, dest)
				repo.git.add(file)
		# make commit
		try:
			repo.git.commit('-m %s' % message)
			remote = repo.remote(remote_name)
			remote.set_url('https://%s:%s@github.com/%s/%s.git' %\
				(settings.USERNAME, settings.PASSWORD, settings.USERNAME, repo_name))
			remote.pull()
			remote.push()
		except GitCommandError as e:
			print(e)
			raise BranchUpToDateException

	def random_auto_commit(self):
		# prepare all files abailable
		search_for = os.sep.join([settings.DEFAULT_SOURCE_ROOT_DIR,
								  settings.DEFAULT_REPO,
								  '**', '*.*'])
		prefix = settings.DEFAULT_SOURCE_ROOT_DIR + os.sep + settings.DEFAULT_REPO + os.sep
		files = [f.replace(prefix, '') for f in glob.glob(search_for, recursive=True)]
		# randomly choose one and make commit
		chosen_files = list(random.sample(set(files), random.randint(1, 4)))
		message = ' '.join(['add files:']+[os.path.basename(f) for f in chosen_files])
		# perform commit and push to remote
		if settings.DEFAULT_COMMIT_TOOL == 'GitPython':
			try:
				self.addfiles_commit_push_remote(repo_name=settings.DEFAULT_REPO,
												 root_dir=settings.DEFAULT_CLONE_ROOT_DIR,
												 file_list=chosen_files,
												 message=message)
			except BranchUpToDateException:
				print('up to date. nothing to do. pass.')
		elif settings.DEFAULT_COMMIT_TOOL == 'PyGithub':
			self.remote_addfiles_commit(repo_name=settings.DEFAULT_REPO,
									file_list=chosen_files,
									message=message)
		else:
			raise DefaultCommitToolException

	def run(self):
		try:
			bot.repo_clone(repo_name=settings.DEFAULT_REPO,
						   root_dir=settings.DEFAULT_CLONE_ROOT_DIR)
		except ClonedRepoExistedError:
			print('Repository existed. Does not clone.')
		while True:
			print('auto commit.')
			self.random_auto_commit()
			print('done. going sleep...')
			sleep_minutes = random.randint(settings.RANDOM_MIN_MINUTES, settings.RANDOM_MAX_MINUTES)
			awake_time = datetime.now() + timedelta(minutes=sleep_minutes)
			print('scheduled to sleep %s minutes. next awake: %s' % (sleep_minutes, awake_time))
			time.sleep(60*sleep_minutes)
			print('awake.')

if __name__ == "__main__":
	bot = Bot()
	bot.login()
	#print(bot.report_status(repo_name=settings.DEFAULT_REPO))
	bot.run()
	''' # make a local clone repo, make changes, and commit -> push
	try:
		bot.repo_clone(repo_name=settings.DEFAULT_REPO,
					   root_dir=settings.DEFAULT_CLONE_ROOT_DIR)
	except ClonedRepoExistedError:
		print('Repository existed. Does not clone.')
	try:
		bot.addfiles_commit_push_remote(repo_name=settings.DEFAULT_REPO,
										root_dir=settings.DEFAULT_CLONE_ROOT_DIR,
										file_list=['exceptions.py'],
										message='commit_push_remote')
	except BranchUpToDateException:
		print('Branch up to date. Does not commit.')
	'''
	''' # make remote commit through GitHub API
	file_list = ['settings.py',]
	bot.remote_addfiles_commit(repo_name=settings.DEFAULT_REPO,
							   file_list = file_list,
							   message='add files %s' % file_list)
	'''