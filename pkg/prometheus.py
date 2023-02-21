from prometheus_client import Counter, Gauge,  start_http_server
from typing import Dict,  Union
from pkg import constant


class PromBase(object):
    def __init__(self,):
        self.metrics: Dict[str, Union[Counter, Gauge]] = {}

    @staticmethod
    def _encode_metrics_name(process_name, metric_type: str) -> str:
        return constant.PROJECT_NAME+"_"+process_name+"_"+metric_type

    @staticmethod
    def _create_metric(metric_name, description) -> Union[Counter, Gauge]:
        pass

    def is_metric_exist(self, metric_name: str) -> bool:
        if self.metrics.get(metric_name, None) is not None:
            return True
        return False

    def insert_new_metric(self, process_name, metric_name, description: str):
        metric_name = self._encode_metrics_name(process_name, metric_name)
        if self.is_metric_exist(metric_name) is False:
            self.metrics[metric_name] = self._create_metric(metric_name, description)
            return
        print("Metrics is existed")

    def inc(self, process_name:str, metric_name: str, value: int):
        metric_name = self._encode_metrics_name(process_name, metric_name)
        if self.is_metric_exist(metric_name) is True:
            self.metrics[metric_name].inc(value)


class PromCount(PromBase):
    def __init__(self, ):
        super().__init__()
        self.metrics: Dict[str, Counter] = {}

    @staticmethod
    def _create_metric(metric_name, description) -> Union[Counter, Gauge]:
        return Counter(name=metric_name, documentation=description)


class PromGauge(PromBase):
    def __init__(self, ):
        super().__init__()
        self.metrics: Dict[str, Gauge] = {}

    @staticmethod
    def _create_metric(metric_name, description) -> Union[Counter, Gauge]:
        return Gauge(name=metric_name, documentation=description)

    def dec(self, process_name: str, metric_name: str, value: int = 1):
        metric_name = self._encode_metrics_name(process_name, metric_name)
        if self.is_metric_exist(metric_name) is True:
            self.metrics[metric_name].dec(value)

    def set(self, process_name: str, metric_name: str, value: int = 1):
        metric_name = self._encode_metrics_name(process_name, metric_name)
        if self.is_metric_exist(metric_name) is True:
            print("set value for metrics {}: {}".format(metric_name, value))
            self.metrics[metric_name].set(value)

        else:
            print("metric name is not valid {}".format(metric_name))


class Prom(object):
    def __init__(self, prom_count: PromCount, prom_gauge: PromGauge):
        self.prom_count = prom_count
        self.prom_gauge = prom_gauge
        start_http_server(constant.HTTP_PORT_EXPORTER)


def new_prom() -> Prom:
    count = PromCount()
    gauge = PromGauge()
    return Prom(prom_count=count, prom_gauge=gauge)
