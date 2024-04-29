from diagrams.generic.virtualization import Virtualbox
from diagrams.onprem.iac import Ansible
from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.client import Client
from diagrams.generic.os import Debian
from diagrams.custom import Custom

with Diagram(""):
    virtual_box = Virtualbox("VirtualBox")

    with Cluster("Virtual Machines"):
        vm_group = [
            Debian("master"),
            Debian("slave1"),
            Debian("slave2")
        ]

    ansible = Ansible("Ansible")
    vagrant = Custom("Vagrant", "../../images/vagrant.png")

    ansible >> vm_group
    virtual_box >> vm_group
    vagrant >> ansible
    vagrant >> virtual_box
