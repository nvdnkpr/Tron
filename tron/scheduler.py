import datetime
import logging

from tron.utils import time

log = logging.getLogger('tron.scheduler')

class ConstantScheduler(object):
    """The constant scheduler always schedules a run because the job should be running constantly"""
    def next_run(self, job):
        run = job.build_run()
        run.run_time = time.current_time()
        return run


class DailyScheduler(object):
    """The daily scheduler schedules one run per day"""
    def next_run(self, job):
        run = job.build_run()

        # For a daily scheduler, always assume the next job run is tomorrow
        run_time = (time.current_time() + datetime.timedelta(days=1)).replace(hour=0, minute=0, second=0)

        run.run_time = run_time
        return run
        

class IntervalScheduler(object):
    """The interval scheduler runs a job (to success) based on a configured interval
    """
    def __init__(self, interval=None):
        self.interval = interval
    
    def next_run(self, job):
        run = job.build_run()

        # Find the last success to pick the next time to run
        for past_run in reversed(job.runs):
            if past_run.is_success:
                run.run_time = past_run.end_time + self.interval
                break
        else:
            log.debug("Found no past runs for job %s, next run is now", run)
            run.run_time = time.current_time()
        
        return run
    
        
    