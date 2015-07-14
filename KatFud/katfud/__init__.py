import sys
import signal

from pyramid.config import Configurator


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """

    from pyramid.settings import asbool
    isNonPi = asbool(settings.get('katfud.non_pi', 'true'))
    settings['katfud.non_pi'] = isNonPi

    if not isNonPi:
        import RPIO as GPIO

        def signal_handler(signal, frame):
            print "Shutting down KatFud"
            GPIO.cleanup_interrupts()
            GPIO.cleanup()
            sys.exit(0)

        for sig in [signal.SIGTERM, signal.SIGINT, signal.SIGHUP, signal.SIGQUIT]:
            signal.signal(sig, signal_handler)

    config = Configurator(settings=settings)
    config.include('pyramid_mako')
    config.include('pyramid_chameleon')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('katfud', '/v1/katfud')
    config.add_route('katfudcmd', '/v1/katfud/{cmd}')
    config.add_route('times', '/fud/times')
    config.scan()
    return config.make_wsgi_app()
