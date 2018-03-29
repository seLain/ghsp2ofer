from abc import ABCMeta, abstractmethod
from datetime import datetime, timedelta
from exceptions import PotentialInfiniteLoopException
import random
import settings

class WaitStrategy(metaclass=ABCMeta):
	'''
	Abstract method to get next akake time
	:param Datetime current_time: a given current time
	:return: sleep_minutes, awake_time
	'''
	@abstractmethod
	def get_awake_time(self, current_time):
		pass

class RandomWaitStrategy(WaitStrategy):
	def get_awake_time(self, current_time):
		sleep_minutes = random.randint(settings.RANDOM_MIN_MINUTES, settings.RANDOM_MAX_MINUTES)
		awake_time = current_time + timedelta(minutes=sleep_minutes)
		return sleep_minutes, awake_time

class RandomWorkHourStrategy(WaitStrategy):
	def get_awake_time(self, current_time):
		work_hours = settings.WORK_HOURS
		infinite_loop_sentinel = 0
		while True:
			if infinite_loop_sentinel > 100:
				raise PotentialInfiniteLoopException
			sleep_minutes = random.randint(settings.RANDOM_MIN_MINUTES, settings.RANDOM_MAX_MINUTES)
			awake_time = current_time + timedelta(minutes=sleep_minutes)
			if awake_time.hour in range(work_hours[0], work_hours[1]):
				return sleep_minutes, awake_time
			else:
				infinite_loop_sentinel += 1