import logging
import multiprocesshandlers
import time
import random
from multiprocessing import Process
from threading import Thread


def create_logger():
    app_name = 'sistel-osc-socket'
    log_file = app_name + '.log'
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    fh = multiprocesshandlers.RotatingFileHandler(log_file, maxBytes=1024 * 50, backupCount=3)
    fh.setLevel(logging.INFO)
    ch = multiprocesshandlers.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger


def run_proc(proc_name, logger):

    def run_thread(thread_name):
        while True:
            time.sleep(random.random() * 1)
            logger.info('%s-%s: %s' % (proc_name, thread_name, time.strftime("%Y-%m-%d %H:%M:%S")))

    threads = []
    for i in range(0, 10):
        t = Thread(target=run_thread, args=["Thread-%s" % i])
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

if __name__ == '__main__':
    logger = create_logger()

    procs = []
    for i in range(0, 10):
        p = Process(target=run_proc, args=['Proc-%s' % i, logger])
        p.start()
        procs.append(p)

    for p in procs:
        p.join()