import time
import threading
from .metrics import ProcPsutil, new_metrics_psutil, BasePsutil
from .prometheus import Prom, new_prom, PromGauge, PromCount
from pkg import constant
from typing import Dict,  Union, List


class Agent(threading.Thread):
    def __init__(self, list_proc: List[ProcPsutil], prom: Prom, base: BasePsutil):
        super().__init__()
        self.prom = prom
        self.list_proc = list_proc
        self.base = base
        self.base_insert_metrics_cpu()

    def base_insert_metrics_cpu(self):
        print("set base cpu metrics")
        for index in range(0, self.base.num_cpu):
            self.prom.prom_gauge.insert_new_metric(process_name="base", metric_name="usage_cpu"+str(index),
                                                   description="base usage cpu of core"+str(index))

    def base_collect_metrics_for_prom(self):
        data = self.base.get_metrics()
        # print("cpu usage per core: ", data)
        for index in range(0, self.base.num_cpu):
            metric_name = "usage_cpu"+str(index)
            self.prom.prom_gauge.set(process_name="base", metric_name=metric_name,
                                     value=data.get(metric_name, 0))

    @staticmethod
    def proc_get_data_usage(proc: ProcPsutil) -> Dict[str, float]:
        return proc.get_metrics()

    # temporary hardcode for specific metrics
    def proc_insert_new_metrics(self, process_name: str):
        def callback_insert_metrics(prom: Union[PromGauge, PromCount], metric_name: str, desc: str):
            prom.insert_new_metric(process_name, metric_name, desc)

        # temporary demo for gauge metrics
        for metric in constant.LIST_METRICS:
            metric_name = metric.get("metric_name", "")
            desc = metric.get("desc", "")
            for sub_metric_name in metric_name:
                callback_insert_metrics(prom=self.prom.prom_gauge, metric_name=sub_metric_name, desc=desc)
            # if not isinstance(metric, List):
            #     callback_insert_metrics(prom=self.prom.prom_gauge, metric_name=metric.get("metric_name", ""),
            #                             desc=metric.get("desc", ""))
            # else:
            #     for sub_metric in metric:
            #         callback_insert_metrics(prom=self.prom.prom_gauge, metric_name=sub_metric.get("metric_name", ""),
            #                                 desc=sub_metric.get("desc", ""))

    # temporary hardcode for specific gauge metrics
    def proc_collect_metrics_for_prom(self, proc: ProcPsutil):
        data = self.proc_get_data_usage(proc)
        # print("set metrics for prometheus with proc : ", proc.name, data)
        for metric in constant.LIST_METRICS:
            metric_name = metric.get("metric_name", "")
            for sub_metric_name in metric_name:
                usage = data.get(sub_metric_name, 0)
                self.prom.prom_gauge.set(process_name=proc.name, metric_name=sub_metric_name, value=usage)

    def proc_add_new_ins(self, proc: ProcPsutil):
        self.list_proc.append(proc)
        self.proc_insert_new_metrics(proc.name)

    def proc_add_new_ins_by_name_and_pid(self, pid: int, proc_name: str):
        proc = new_metrics_psutil(pid, proc_name)
        self.list_proc.append(proc)
        self.proc_insert_new_metrics(proc.name)

    def proc_remove(self, proc: ProcPsutil):
        self.list_proc.remove(proc)
        
    def proc_collect_metrics_thread(self):
        while True:
            for proc in self.list_proc:
                if proc.is_proc_alive() is True:
                    self.proc_collect_metrics_for_prom(proc)
                else:
                    self.proc_remove(proc)
            time.sleep(2)
            
    def base_collect_metrics_thread(self):
        while True:
            self.base_collect_metrics_for_prom()
            time.sleep(2)
        pass

    def run(self):
        base_thread = threading.Thread(target=self.base_collect_metrics_thread)
        base_thread.start()
        proc_thread = threading.Thread(target=self.proc_collect_metrics_thread)
        proc_thread.start()
        pass


def create_new_agent() -> Agent:
    prom = new_prom()
    return Agent(list_proc=[], prom=prom, base=BasePsutil())

