import pulumi
from pulumi_azure_native import resources

import storage
import network
import vm

cfg = pulumi.Config()
env = pulumi.get_stack()

# Lab 1: Resource Group
resource_group = resources.ResourceGroup(
    "rg",
    resource_group_name=f"rg-lab-{env}-sr",
    tags={"environment": env, "managed-by": "pulumi"},
)
pulumi.export("resource_group", resource_group.name)
pulumi.export("location", resource_group.location)

# Lab 2: Storage (the name now comes from stack config)
storage.create_storage(resource_group, cfg.require("storageAccountName"))

# Lab 3: Network
vnet, web_subnet, app_subnet, db_subnet = network.create_network(resource_group)
pulumi.export("vnet_name", vnet.name)
pulumi.export("web_subnet_id", web_subnet.id)
pulumi.export("app_subnet_id", app_subnet.id)
pulumi.export("db_subnet_id", db_subnet.id)

# Lab 4: VM, only in stacks where deployVm is true
if cfg.get_bool("deployVm"):
    public_ip, virtual_machine = vm.create_vm(resource_group, web_subnet)
    pulumi.export("public_ip", public_ip.ip_address)
    pulumi.export(
        "ssh_command",
        public_ip.ip_address.apply(lambda ip: f"ssh -i ~/.ssh/lab_vm azureuser@{ip}"),
    )
