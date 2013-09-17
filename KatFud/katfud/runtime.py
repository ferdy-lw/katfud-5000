import time
import subprocess
import logging
log = logging.getLogger(__name__)

from pyramid.events import subscriber, ApplicationCreated

import yaml

runtime = None


@subscriber(ApplicationCreated)
def load_runtime(event):

    event.app.registry.settings['katfud.runtime'] = _Runtime(event.app.registry.settings['katfud.conf_file'])
    global runtime
    runtime = event.app.registry.settings['katfud.runtime']

    command = "./get_hostname.sh"
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]


class _Runtime(object):
    """System runtime details"""

    def __init__(self, config_file):

        self.config_file = config_file

        with open(config_file) as f:
            config = yaml.safe_load(f)

        self.__dict__.update(**config)

        self.started = int(time.time())
        self.lastRan = 'Never'
        self.numberFeeds = 0

        if not hasattr(self, 'nextRun'):
            self.nextRun = self.firstFeed

    def save(self):

        config = {}
        config['firstFeed'] = self.firstFeed
        config['lastRan'] = self.lastRan
        if hasattr(self, 'nextRun'):
            config['nextRun'] = self.nextRun
        config['periodSec'] = self.periodSec
        config['periodScale'] = self.periodScale

        stream = file(self.config_file, 'w')
        yaml.dump(config, stream)

    def is_feed_time(self, set_next_run=False):

        if self.nextRun < int(time.time()):

            if set_next_run:
                self.set_next_run()
                self.set_last_ran()
                log.info("Updated next run time to: {}".format(time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime(self.nextRun))))

            return True

        return False

    def set_next_run(self):

        self.nextRun = int(time.time()) + self.periodSec

    def set_last_ran(self):

        self.lastRan = int(time.time())
        self.save()
