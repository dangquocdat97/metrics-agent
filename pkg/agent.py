import time
from typing import Dict
import threading
from pkg.metrics import MetricsPsutil, new_metrics_psutil
from pkg.prometheus import Prom, new_prom
from pkg import constant




class Agent(threading.Thread):
    def __init__(self, metrics_psutil: MetricsPsutil, prom: Prom):
        super().__init__()
        self.metrics = metrics_psutil
        self.prom = prom

    def get_metrics(self) -> Dict[str, float]:
        return self.metrics.get_metrics()

    # temporary hardcode for specific metrics
    def insert_new_metrics_for_monitor(self):
        self.prom.prom_gauge.insert_new_metric(name_metric=constant.CPU_USAGE, description=constant.CPU_USAGE_DOCS)
        self.prom.prom_gauge.insert_new_metric(name_metric=constant.MEM_USAGE, description=constant.MEM_USAGE_DOCS)

    # temporary hardcode for specific metrics
    def collect_metrics(self):
        metrics = self.get_metrics()
        cpu_usage = metrics.get(constant.CPU_USAGE, 0)
        mem_usage = metrics.get(constant.MEM_USAGE, 0)
        self.prom.prom_gauge.set(constant.CPU_USAGE, cpu_usage)
        self.prom.prom_gauge.set(constant.MEM_USAGE, mem_usage)

    def run(self):
        while True:
            self.collect_metrics()
            time.sleep(2)


def create_new_agent() -> Agent:
    prom = new_prom()
    metrics = new_metrics_psutil()
    return Agent(metrics_psutil=metrics, prom=prom)


def init_agent():
    agent = create_new_agent()
    agent.insert_new_metrics_for_monitor()

