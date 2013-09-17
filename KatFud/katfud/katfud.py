import time
import logging
import subprocess
log = logging.getLogger(__name__)

from pyramid.view import view_defaults, view_config
from pyramid.response import Response

import runtime
from motor import run_now


@view_defaults(route_name="katfud", renderer="json")
class KatFud(object):
    """KatFud REST
    """

    def __init__(self, request):
        self.request = request

    @view_config(request_method='GET')
    def stats(self):

        cur_settings = runtime.runtime

        stats = {}

        with open(self.request.registry.settings['katfud.host_file']) as f:
            stats['fudUrl'] = "http://{}".format(f.readline())

        stats['currentTime'] = int(time.time())
        stats['started'] = cur_settings.started
        stats['lastRan'] = cur_settings.lastRan
        stats['numberFeeds'] = cur_settings.numberFeeds
        stats['nextRun'] = cur_settings.nextRun
        stats['firstFeed'] = cur_settings.firstFeed
        stats['periodSec'] = cur_settings.periodSec
        stats['periodScale'] = cur_settings.periodScale

        return stats

    @view_config(request_method='PUT')
    def update_settings(self):

        settings = self.request.json_body

        if settings['code'] != self.request.registry.settings['katfud.security_code']:
            self.request.response.status = 401
            return {"status": "failure (code)"}

        cur_settings = runtime.runtime

        if 'firstFeed' in settings:
            cur_settings.firstFeed = settings['firstFeed']

        if 'periodSec' in settings:
            cur_settings.periodSec = settings['periodSec']

        if 'periodScale' in settings:
            cur_settings.periodScale = settings['periodScale']

        cur_settings.nextRun = cur_settings.firstFeed

        cur_settings.save()

        return {"status": "success"}

    @view_config(route_name='katfudcmd', request_method='POST')
    def run_cmd(self):
        cmd = self.request.matchdict['cmd']
        code = self.request.params['code']

        log.info('Command: {}, Code: {}'.format(cmd, code))

        if code != self.request.registry.settings['katfud.security_code']:
            self.request.response.status = 401
            return {"status": "failure (code)"}

        if cmd == 'run_now':
            if self.request.registry.settings['katfud.non_pi']:
                log.warning("Not running on PI - no motor run now")
                runtime.runtime.set_last_ran()
            else:
                run_now()

        elif cmd == 'reboot':
            if self.request.registry.settings['katfud.non_pi']:
                log.warning("Not running on PI - not rebooting")
            else:
                command = "/sbin/shutdown -r now"
                process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
                output = process.communicate()[0]

        elif cmd == 'shutdown':
            if self.request.registry.settings['katfud.non_pi']:
                log.warning("Not running on PI - not shutting down")
            else:
                command = "/sbin/shutdown now"
                process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
                output = process.communicate()[0]

        return {"status": "success"}
