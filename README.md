[![Python Support](https://img.shields.io/badge/python-3.6-blue.svg)]()
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/79fdd815b4f740a39fc6ec4093493410)](https://www.codacy.com/app/seLain/ghsp2ofer?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=seLain/ghsp2ofer&amp;utm_campaign=Badge_Grade)

## What's This 

On the way to build a fully-automated coding bot.

## For Now

It's a functional prototype bot which can replicate code files randomly from designated source.
The replicated code is then committed to local git repo and pushed to Github repo.

## How2Start

First, be sure you have Python 3.6+ installed. (Python 3.6.5rc1+ recommended)

Optionally create a virtual environment for this bot, and dive into this virtual environment.

`python36 -m venv py36_venv\ghsp2ofer`
`py36_venv\ghsp2ofer\Scripts\activate` (on Windows)

Download **ghsp2ofer** and extract to a specific folder, such as `ghsp2ofer_bot`. change your working directory to `ghsp2ofer_bot`.

Install required packages.

`(ghsp2ofer) pip install -r requirements`

Create two necessary directories: `ghsp2ofer_bot\cloned_repos`, `ghsp2ofer_bot\source_repos`.

Create an empty repository on Github (wihtout .gitignore). For example, new repository `Spoofer`.

Rename `ghsp2ofer_bot\settings_example.py` as `ghsp2ofer_bot\settings.py`, put necessary information in to `ghsp2ofer_bot\settings.py`.
 * Set settings.DEFAULT_REPO as `Spoofer` ( or whatever repository name you created earlier)
 * Set settings.WAIT_STRATEGY, currently two strategies are available:
   1. RandomWaitStrategy: delays next commit by random(settings.RANDOM_MIN_MINUTES, settings.RANDOM_MAX_MINUTES) minutes.
   2. RandomWorkHourStrategy: delays next commit by random(settings.RANDOM_MIN_MINUTES, settings.RANDOM_MAX_MINUTES) minutes if and only if the next commit time lays in settings.WORK_HOURS
 * Set settings.RANDOM_MIN_MINUTES, settings.RANDOM_MAX_MINUTES. The bot will be triggered and sleep for random(settings.RANDOM_MIN_MINUTES, settings.RANDOM_MAX_MINUTES) minutes.
 * Set settings.WORK_HOURS which specifies working hours of this bot. 

Create directory `ghsp2ofer_bot\source_repos\Spoofer`, and put in code files to be replicated.

Final step,

`(ghsp2ofer) python bot.py`
