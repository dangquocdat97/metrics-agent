
import time
from pkg.prometheus import new_prom


if __name__ == '__main__':
    prom = new_prom()
    prom.prom_gauge.insert_new_metric(name_metric="cpu_usage", description="cpu usage of process")
    prom.prom_gauge.set("cpu_usage", 2)
    while True:
        time.sleep(3)
        prom.prom_gauge.inc("cpu_usage", 1)






