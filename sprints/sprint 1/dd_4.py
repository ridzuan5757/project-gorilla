from diagrams import Diagram, Cluster, Edge
from diagrams.programming.framework import Laravel, Vue
from diagrams.programming.language import Php, NodeJS
from diagrams.onprem.logging import RSyslog
from diagrams.custom import Custom

with Diagram(""):
    with Cluster("Cloud BOS"):
        backend = Laravel("Backend")
        frontend = Vue("Frontend")

    otel = Custom("OpenTelemetry\nCollector", "../../images/opentelemetry.png")
    otel_gw = Custom("OpenTelemetry\nGateway",
                     "../../images/opentelemetry.png")

    otel >> Edge(label="Traces | Metrics | Logs") >> otel_gw
    frontend >> Edge(label="Traces") >> otel
    backend >> Edge(label="Traces") >> otel
    RSyslog("RSyslog") >> Edge(label="Logs") >> otel
