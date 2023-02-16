import os
from typing import Type, Dict
import psutil
from pkg import constant


class MetricsPsutil(object):
    def __init__(self, psutil_process: psutil.Process = None):
        self.proc = psutil_process

    def is_proc_alive(self) -> bool:
        if self.proc is not None:
            return self.proc.is_running()
        return False

    def get_proc_status(self) -> str:
        return self.proc.status()

    def get_proc_cpu_usage(self) -> float:
        return self.proc.cpu_percent(interval=1)

    def get_proc_memory_usage(self) -> float:
        return self.proc.memory_percent()

    @staticmethod
    def find_proc_by_cmd(cmd: list) -> Type[psutil.Process]:
        for proc in psutil.process_iter():
            try:
                if proc.cmdline() == cmd:
                    return proc
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                print("type of: ", type(psutil.Process))
                return psutil.Process

    def get_metrics(self) -> Dict[str, float]:
        if self.is_proc_alive():
            return {constant.CPU_USAGE: self.get_proc_cpu_usage(), constant.MEM_USAGE: self.get_proc_memory_usage()}
        return {}


def create_psutil_provider(pid: int) -> psutil.Process:
    return psutil.Process(pid=pid)


# temporary for current process
def new_metrics_psutil() -> MetricsPsutil:
    provider = create_psutil_provider(os.getpid())
    return MetricsPsutil(provider)
