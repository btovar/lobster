#!/usr/bin/env python
import os
import shutil
import time
import yaml
from lobster import cmssw
from lobster import job
from argparse import ArgumentParser

import work_queue as wq

parser = ArgumentParser(description='A job submission tool for CMS')
parser.add_argument('config_file_name', nargs='?', default='lobster.yaml', help='Configuration file to process.')
args = parser.parse_args()

with open(args.config_file_name) as config_file:
    config = yaml.load(config_file)

# id = 0
# tasks = []

# job_src = job.SimpleJobProvider("sleep 10", 25)
job_src = cmssw.JobProvider(config)

queue = wq.WorkQueue(12345)

while not job_src.done():
    # need to lure workers into connecting to the master
    stats = queue.stats
    if stats.total_workers_joined + stats.tasks_waiting == 0:
        num = 1
    else:
        num = stats.workers_ready
    for i in range(num):
    # for i in range(queue.stats.capacity - queue.stats.workers_busy):
        job = job_src.obtain()

        if not job:
            break

        (id, cmd, inputs, outputs) = job

        task = wq.Task(cmd)
        task.specify_tag(id)

        for (local, remote) in inputs:
            if os.path.isfile(local):
                task.specify_input_file(local, remote, wq.WORK_QUEUE_CACHE)
            elif os.path.isdir(local):
                task.specify_directory(local, remote, wq.WORK_QUEUE_INPUT,
                        wq.WORK_QUEUE_CACHE, recursive=True)
            else:
                raise NotImplementedError

        for (local, remote) in outputs:
            task.specify_output_file(local, remote)

        queue.submit(task)

    task = queue.wait(3)
    if task:
        job_src.release(task.tag, task.return_status)
    else:
        time.sleep(1)
