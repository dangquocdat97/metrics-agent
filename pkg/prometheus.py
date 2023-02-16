from prometheus_client import Counter, Gauge, push_to_gateway, CollectorRegistry, start_http_server
from typing import Dict, Type, List
from pkg import constant


class PromCount(object):
    def __init__(self, ):
        self.count_metrics: Dict[str, Counter] = {}

    @staticmethod
    def _create_count_metric(metric_name: str, desc: str):
        return Counter(name=metric_name, documentation=desc)

    def is_metric_exist(self, metric_name: str) -> bool:
        if self.count_metrics.get(metric_name, None) is not None:
            return True
        return False

    def insert_metric(self, metric_name: str, description: str):
        if self.is_metric_exist(metric_name) is False:
            self.count_metrics[metric_name] = self._create_count_metric(metric_name, description)
            return
        print("Metrics is existed")

    def inc(self, metric_name: str, value: int):
        if self.is_metric_exist(metric_name) is True:
            self.count_metrics[metric_name].inc(value)


class PromGauge(object):
    def __init__(self, ):
        self.gauge_metrics: Dict[str, Gauge] = {}

    @staticmethod
    def _create_gauge_metric(metric_name: str, desc: str) -> Gauge:
        print("create new gauge metric")
        return Gauge(name=metric_name, documentation=desc)

    def is_metric_exist(self, metric_name: str) -> bool:
        if self.gauge_metrics.get(metric_name, None) is not None:
            return True
        return False

    def insert_new_metric(self, name_metric: str, description: str):
        if self.is_metric_exist(name_metric) is False:
            print("insert new metrics: ", name_metric)
            self.gauge_metrics[name_metric] = self._create_gauge_metric(name_metric, description)
            return
        print("Metrics is existed")

    def inc(self, metric_name: str, value: int = 1):
        if self.is_metric_exist(metric_name) is True:
            self.gauge_metrics[metric_name].inc(value)

    def dec(self, metric_name: str, value: int = 1):
        if self.is_metric_exist(metric_name) is True:
            self.gauge_metrics[metric_name].dec(value)

    def set(self, metric_name: str, value: int = 1):
        if self.is_metric_exist(metric_name) is True:
            print("set value for metrics: ", value)
            self.gauge_metrics[metric_name].set(value)


class Prom(object):
    def __init__(self, prom_count: PromCount, prom_gauge: PromGauge):
        self.prom_count = prom_count
        self.prom_gauge = prom_gauge
        start_http_server(constant.HTTP_PORT_EXPORTER)


def new_prom() -> Prom:
    count = PromCount()
    gauge = PromGauge()
    return Prom(prom_count=count, prom_gauge=gauge)
