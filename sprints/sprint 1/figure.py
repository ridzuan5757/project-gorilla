from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.infra import Master, Node
from diagrams.k8s.network import Service
from diagrams.custom import Custom
from diagrams.onprem.monitoring import Grafana, Prometheus
from diagrams.generic.network import Router

with Diagram("figure", direction="LR"):
    with Cluster("Master"):
        master = Master("master1")
        calico_master = Custom("Calico", "../../images/calico.png")

    with Cluster("Slave"):
        slave = Node("slave1")
        calico_slave = Custom("Calico", "../../images/calico.png")

        otel = Custom("Opentelemetry\nCollector",
                      "../../images/opentelemetry.png")
        prom = Prometheus("Prometheus")
        graf = Grafana("Grafana")

        otel >> Edge(label="8888 | 8889") >> prom >> Edge(label="9090") >> graf

        otel_svc = Service("NodePort\n4317:32001")
        prom_svc = Service("NodePort\n9090:30001")
        graf_svc = Service("NodePort\n3000:30002")

        prom >> prom_svc
        graf >> graf_svc
        otel_svc >> otel

    calico_master >> Edge(color="darkgreen") << calico_slave
    router = Router("Intranet")
    router >> otel_svc
    prom_svc >> router
    graf_svc >> router
