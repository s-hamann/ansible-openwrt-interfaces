OpenWrt Interfaces
==================

This role handles network interface configuration on [OpenWrt](https://www.openwrt.org/) targets, i.e. IP address assignment, bridges and VLANs.
It uses DSA configuration settings and is not compatible with targets that still use swconfig.

Requirements
------------

This role requires [gekmihesg's Ansible library for OpenWrt](https://github.com/gekmihesg/ansible-openwrt), the `ansible.utils` collection and the [netaddr](https://github.com/netaddr/netaddr/) Python package on the Ansible controller.

Role Variables
--------------

* `openwrt_interfaces`  
  A dictionary of interfaces to configure. Keys are interface names and values are in turn dictionaries that describe the interface configuration.
  Most keys are simply passed to the OpenWrt interface configuration.
  Refer to [the documentation](https://openwrt.org/docs/guide-user/base-system/basic-networking#interface_sections) for information about valid and required options.
  The following keys have a special meaning in this role:
  * `ip`  
    An IPv4 address in CIDR notation that is statically assigned to the interface.
    Sets the OpenWrt interface options `ipaddr`, `netmask` and `proto` accordingly.
    Shorter but otherwise identical to setting them explicitly.
    Optional.
  * `ports`  
    If this is set, the interface is set up as a bridge and the listed network devices are added to it as switch ports.
    When set, it must be a list of network device names, e.g. `eth0` or `lan1`.
    Simple numbers are prefixed with `lan`, e.g. `1` is short for `lan1`.
    A range of numbers can be used to denote multiple ports, e.g. `1-3` is short for `lan1`, `lan2` and `lan3`.
    If `ports` is not set but `vlan` is, `ports` is automatically set to all ports referenced in `vlan`.
    Optional.
  * `vlan`  
    If this is set, the interface is set up as a bridge with support for the VLANs defined here.
    It must be a dictionary where keys are VLAN names and values are in turn dictionaries that describe the VLAN configuration.
    Most keys of the individual VLANs are simply passed to the OpenWrt interface configuration (like described above).
    Again, some keys have a special meaning:
    * `ip`  
      See `ip` above.
      Optional.
    * `id`  
      The numeric ID of the VLAN.
      Mandatory.
    * `ports`  
      A list of switch ports assigned to this VLAN.
      It works exactly like `ports` above, except that it is possible to add a suffix to each port to denote if it is tagged (`:t`), untagged (`:u`) or untagged with PVID (`:u*`).
      When set on a range, the suffix applies to each element, e.g. `1-3:t` is short for `lan1:t`, `lan2:t`, `lan3:t`.
      Mandatory.

Dependencies
------------

This role does not depend on any specific roles.

Example Configuration
---------------------

The following is a short example for some of the configuration options this role provides:

```yaml
openwrt_interfaces:
  wan:
    device: eth0
    proto: dhcp
  switch:
    vlan:
      lan:
        id: 10
        ports:
          - 1-8
          - 16:t
      guest:
        id: 20
        ports:
          - 9-14
          - 16:t
      mgmt:
        id: 30
        ip: "192.168.1.1/24"
        ports:
          - 15
          - 16:t
```

License
-------

MIT
