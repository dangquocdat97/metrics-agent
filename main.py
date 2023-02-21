import psutil
from pkg.agent import create_new_agent
from pkg.metrics import find_proc_by_cmd

cmd_go_process = ["/usr/bin/cadvisor ", "-logtostderr"]

if __name__ == '__main__':
    try:
        agent = create_new_agent()
        agent.start()
        print("hello")
        process = find_proc_by_cmd(cmd_go_process)
        # if process is not None and isinstance(process.pid, int):
        #     agent.add_proc_by_name_and_pid(pid=process.pid, proc_name="example")
        agent.proc_add_new_ins_by_name_and_pid(pid=67283, proc_name="cadvisor")

    except Exception as err:
        print(err)








