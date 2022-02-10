# -*- encoding:utf-8 -*-
# author: liuheng
import time
import multiprocessing
from processors.server import app
from processors import generator as generators
from processors import tester as testers
from setting import *
from loguru import logger

if IS_WINDOWS:
    multiprocessing.freeze_support()

tester_process, generator_process, server_process = None, None, None

class Scheduler:
    def run_tester(self, website, cycle=CYCLE_TESTER):
        if not ENABLE_TESTER:
            logger.info('tester note enabled, exit')
        tester = getattr(testers, TESTER_MAP[website])(website)
        loop = 0
        while True:
            logger.debug(f'tester loop {loop} start...')
            tester.run()
            loop += 1
            time.sleep(cycle)

    def run_generator(self, website, cycle=CYCLE_GENERATOR):
        if not ENABLE_GENERATOR:
            logger.info('getter not enable, exit')
            return
        generator = getattr(generators, GENERATOR_MAP[website])(website)
        loop = 0
        while True:
            logger.debug(f'getter loop {loop} start...')
            generator.run()
            loop += 1
            time.sleep(cycle)

    def runserver(self, _):
        if not ENABLE_SERVER:
            logger.info('server not enabled, exit')
            return
        app.run(host=API_HOST, port=API_PORT, threaded=API_THREADED)


    def run(self, website):
        global tester_process, generator_process, server_process
        try:
            logger.info(f'starting account pool for website {website}...')
            if ENABLE_TESTER:
                tester_process = multiprocessing.Process(target=self.run_tester, args=(website,))
                logger.info(f'starting tester, pid {tester_process.pid}...')
                tester_process.start()

            if ENABLE_GENERATOR:
                generator_process = multiprocessing.Process(target=self.run_generator, args=(website,))
                logger.info(f'starting getter, pid{generator_process.pid}...')
                generator_process.start()

            if ENABLE_SERVER:
                server_process = multiprocessing.Process(target=self.run_server, args=(website,))
                logger.info(f'starting server, pid{server_process.pid}...')
                server_process.start()
            tester_process.join()
            generator_process.join()
            server_process.join()
        except KeyboardInterrupt:
            logger.info('received keyboard interrupt signal')
            tester_process.terminate()
            generator_process.terminate()
            server_process.terminate()
        finally:
            # must call join method before calling is_alive
            tester_process.join()
            generator_process.join()
            server_process.join()
            logger.info(f'tester is {"alive" if tester_process.is_alive() else "dead"}')
            logger.info(f'getter is {"alive" if generator_process.is_alive() else "dead"}')
            logger.info(f'server is {"alive" if server_process.is_alive() else "dead"}')
            logger.info('accountpool terminated')