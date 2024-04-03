"""A Kubernetes Python Pulumi program"""

import pulumi
from pulumi_kubernetes.apps.v1 import Deployment, DeploymentSpecArgs
from pulumi_kubernetes.meta.v1 import LabelSelectorArgs, ObjectMetaArgs
from pulumi_kubernetes.core.v1 import ContainerArgs, PodSpecArgs, PodTemplateSpecArgs
from pulumi_kubernetes.helm.v3 import Chart, LocalChartOpts

app_labels = { "app": "nginx" }

deployment = Deployment(
    "nginx",
    spec=DeploymentSpecArgs(
        selector=LabelSelectorArgs(match_labels=app_labels),
        replicas=1,
        template=PodTemplateSpecArgs(
            metadata=ObjectMetaArgs(labels=app_labels),
            spec=PodSpecArgs(containers=[ContainerArgs(name="nginx", image="nginx")])
        ),
    ))
nginx_ingress = Chart(
    "nginx-ingress",
    LocalChartOpts(
        path="./ingress-nginx",
        namespace="nginx-ingress",
    ),
)

pulumi.export("name", deployment.metadata["name"])
