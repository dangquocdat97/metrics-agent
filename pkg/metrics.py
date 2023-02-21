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

    def get_proc_threads(self) -> dict:
        return {constant.NUM_THREADS[0]: self.proc.num_threads()}

    def get_proc_cpu_usage(self) -> dict:
        return {constant.CPU_USAGE[0]: self.proc.cpu_percent()}

    def get_proc_memory_usage(self) -> dict:
        return {constant.MEM_USAGE[0]: self.proc.memory_percent()}

    def get_io_counters(self):
        try:
            data = self.proc.io_counters()
            return {"read_count":data[0], "write_count":data[1], "read_bytes":data[2], "write_bytes":data[3]}
        except Exception as err:
            print(err)
            return {"read_count":0, "write_count":0, "read_bytes":0, "write_bytes":0}

    # get data of some specific metrics
    def get_metrics(self) -> Dict[str, float]:
        res = {}
        proc_thread = self.get_proc_threads()
        io_counters = self.get_io_counters()
        cpu = self.get_proc_cpu_usage()
        mem = self.get_proc_memory_usage()
        res.update(proc_thread)
        res.update(cpu)
        res.update(mem)
        res.update(io_counters)
        return res


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

