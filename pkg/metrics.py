import os
from typing import Type, Dict, List
import psutil
from pkg import constant


# Handle for Process management
############################################################
class ProcPsutil(object):
    def __init__(self, psutil_process: psutil.Process, proc_name: str):
        self.proc = psutil_process
        self.name = proc_name

    def is_proc_alive(self) -> bool:
        if self.proc is not None:
            return self.proc.is_running()
        return False

    def get_proc_status(self) -> str:
        return self.proc.status()

    def get_proc_threads(self) -> int:
        return self.proc.num_threads()

    def get_proc_cpu_usage(self) -> float:
        return self.proc.cpu_percent()

    def get_proc_memory_usage(self) -> float:
        return self.proc.memory_percent()

    # get data of some specific metrics
    def get_metrics(self) -> Dict[str, float]:
        return {constant.CPU_USAGE: self.get_proc_cpu_usage(), constant.MEM_USAGE: self.get_proc_memory_usage(),
                constant.NUM_THREADS: self.get_proc_threads()}


def create_psutil_provider(pid: int) -> psutil.Process:
    return psutil.Process(pid=pid)


# temporary for current process
def new_metrics_psutil(pid: int, proc_name: str) -> ProcPsutil:
    provider = create_psutil_provider(pid)
    return ProcPsutil(provider, proc_name)


def find_proc_by_cmd(cmd: list) -> Type[psutil.Process]:
    for proc in psutil.process_iter():
        try:
            if proc.cmdline() == cmd:
                return proc
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            print("type of: ", type(psutil.Process))
            return psutil.Process

# Handle for base psutil
############################################################


class BasePsutil(object):
    def __init__(self):
        self.p = psutil
        self.num_cpu = self.p.cpu_count()

    def get_cpu_percent(self) -> List:
        return self.p.cpu_percent(interval=1, percpu=True)

    def get_metrics(self) -> Dict:
        res = {}
        cpu_percent = self.get_cpu_percent()
        for index in range(0, self.num_cpu):
            res["usage_cpu"+str(index)] = cpu_percent[index]
        return res

