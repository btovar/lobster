import datetime
import logging
import multiprocessing

from lobster.commands.plot import Plotter

logger = logging.getLogger('lobster.actions')

class DummyQueue(object):
    def start(*args):
        pass

    def put(*args):
        pass

    def get(*args):
        return None

class Actions(object):
    def __init__(self, config):
        if 'plotdir' not in config:
            self.plotq = DummyQueue()
        else:
            logger.info('plots in {0} will be updated automatically'.format(config['plotdir']))
            if 'foremen logs' in config:
                logger.info('foremen logs will be included from: {0}'.format(', '.join(config['foremen logs'])))
            plotter = Plotter(config, config['plotdir'])

            def plotf(q):
                while q.get() not in ('stop', None):
                    try:
                        plotter.make_plots(foremen=config.get('foremen logs'))
                    except:
                        pass

            self.plotq = multiprocessing.Queue()
            self.plotp = multiprocessing.Process(target=plotf, args=(self.plotq,))
            self.plotp.start()
            logger.info('spawning process for automatic plotting with pid {0}'.format(self.plotp.pid))

        self.__last = datetime.datetime.now()

    def __del__(self):
        logger.info('shutting down process for automatic plotting with pid {0}'.format(self.plotp.pid))
        self.plotq.put('stop')
        self.plotp.join()

    def take(self, force=False):
        now = datetime.datetime.now()
        if (now - self.__last).seconds > 15 * 60 or force:
            self.plotq.put('plot')
            self.__last = now

