
PROJECT_NAME = "agent"
###################################

CPU_USAGE = "example_cpu_usage"
CPU_USAGE_DOCS = "cpu usage of process"
MEM_USAGE = "example_mem_usage"
MEM_USAGE_DOCS = "memory usage of process"
IO_COUNTER = "example_io_counter"
IO_COUNTER_DOCS = "read/write usage"
NUM_THREADS = "example_num_thread"
NUM_THREADS_DOCS = "number of threads in process"


########################################
HTTP_PORT_EXPORTER = 5192

LIST_METRICS = [
    {"metric_name": CPU_USAGE, "desc": CPU_USAGE_DOCS},
    {"metric_name": MEM_USAGE, "desc": MEM_USAGE_DOCS},
    {"metric_name": NUM_THREADS, "desc": NUM_THREADS_DOCS},
]
