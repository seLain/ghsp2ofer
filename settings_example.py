# GitHub repository access token
USERNAME = ''
PASSWORD = ''
EMAIL = ''
ACCESS_TOKEN = ''

# Name of default repository
DEFAULT_REPO = ''

# Default root dir to put cloned repositories
DEFAULT_CLONE_ROOT_DIR = 'cloned_repos'

# Default root dir to put source repositories
DEFAULT_SOURCE_ROOT_DIR = 'source_repos'

# Choose commit tool
# The value can only be one of ['GitPython', 'PyGithub']
DEFAULT_COMMIT_TOOL = 'GitPython'

# WaitStrategy selection. The value must be one of the concrete wait strategies in wait_strategy.py
WAIT_STRATEGY = 'RandomWorkHourStrategy'

# Random commit interval
RANDOM_MIN_MINUTES = 60
RANDOM_MAX_MINUTES = 120

# Bot working hours
WORK_HOURS = [9, 18] # from 9:00AM~6:00PM