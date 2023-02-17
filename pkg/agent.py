import time
import threading
from .metrics import ProcPsutil, new_metrics_psutil
from .prometheus import Prom, new_prom, PromGauge, PromCount
from pkg import constant
from typing import Dict,  Union, List


class Agent(threading.Thread):
    def __init__(self, list_proc: List[ProcPsutil], prom: Prom):
        super().__init__()
        self.prom = prom
        self.list_proc = list_proc

    @staticmethod
    def get_data_usage(proc: ProcPsutil) -> Dict[str, float]:
        return proc.get_metrics()

    # temporary hardcode for specific metrics
    def insert_new_metrics_for_monitor(self, process_name: str):
        def callback_insert_metrics(prom: Union[PromGauge, PromCount], metric_name: str, desc: str):
            prom.insert_new_metric(process_name, metric_name, desc)

        # temporary demo for gauge metrics
        for metric in constant.LIST_METRICS:
            callback_insert_metrics(prom=self.prom.prom_gauge, metric_name=metric.get("metric_name", ""),
                                    desc=metric.get("desc", ""))

    # temporary hardcode for specific gauge metrics
    def collect_metrics_for_prom(self, proc: ProcPsutil):
        data = self.get_data_usage(proc)
        print("set metrics for prometheus with proc : ", proc.name, data)
        for metric in constant.LIST_METRICS:
            metric_name = metric.get("metric_name")
            usage = data.get(metric_name, 0)

            self.prom.prom_gauge.set(metric_name, usage)

    def add_proc(self, proc: ProcPsutil):
        self.list_proc.append(proc)
        self.insert_new_metrics_for_monitor(proc.name)

    def add_proc_by_name_and_pid(self, pid: int, proc_name: str):
        proc = new_metrics_psutil(pid, proc_name)
        self.list_proc.append(proc)
        self.insert_new_metrics_for_monitor(proc.name)

    def remove_proc(self, proc: ProcPsutil):
        self.list_proc.remove(proc)

    def run(self):
        while True:
            for proc in self.list_proc:
                if proc.is_proc_alive() is True:
                    self.collect_metrics_for_prom(proc)
                else:
                    self.remove_proc(proc)
            time.sleep(2)


def create_new_agent() -> Agent:
    prom = new_prom()
    return Agent(list_proc=[], prom=prom)

