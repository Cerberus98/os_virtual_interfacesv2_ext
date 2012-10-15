# Copyright 2011 OpenStack, LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json

from novaclient import base
from novaclient import utils


class VirtualInterface(base.Resource):
    def create(self):
        self.manager.create()


class VirtualInterfaceManager(base.ManagerWithFind):
    resource_class = base.Resource

    def list(self, instance_id):
        return self._list("/servers/%s/os-virtual-interfaces" % instance_id,
                         "virtual_interfaces")

    def create(self, network_id, instance_id):
        body = {'address': {'network_id': network_id,
                            'instance_id': instance_id}}
        return self._create('/os-virtual-interfaces', body,
                            'virtual_interfaces',
                            return_raw=True)


def ip_address_formatter(field):
    addresses = []
    for addr in field.ip_addresses:
        net_id = field.ip_addresses[0]["network_id"]
        ip_addr = field.ip_addresses[0]["address"]
        label = field.ip_addresses[0]["network_label"]
        addresses.append("label=%s, network_id=%s, ip_address=%s" % (label,
                                                            net_id, ip_addr))
    return ",".join(addresses)


@utils.arg('instance_id', metavar='<instance_id>',
           help="ID of the instance you want to display virtual"
                "interfaces for")
def do_virtual_interface_list(cs, args):
    """
    Add a new virtual interface to an instance
    """
    vifs = cs.os_virtual_interfaces_python_novaclient_ext.list(
                                                        args.instance_id)
    utils.print_list(vifs, ["id", "mac_address", "ip_addresses"],
                     formatters={"ip_addresses": ip_address_formatter})


@utils.arg('network_id', metavar='<network_id>',
           help='Network ID to connect the new virtual interface to')
@utils.arg('instance_id', metavar='<instance_id>',
           help="Instance to attach the new virtual interface to")
def do_virtual_interface_create(cs, args):
    """
    Add a new virtual interface to an instance
    """
    addresses = cs.os_virtual_interfaces_python_novaclient_ext.create(
                                                             args.network_id,
                                                             args.instance_id)
    for address in addresses:
        utils.print_dict(address)
