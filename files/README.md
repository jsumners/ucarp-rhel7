# General Overview
Each VIP consists of the following required variables:

+ `VID`: a unique number, amongst all VIPs, between 1 and 255
+ `PASSWORD`: a string password
+ `BIND_INTERFACE`: the interface to bind the VIP to
+ `SOURCE_ADDRESS`: the primary address of the `BIND_INTERFACE`
+ `VIP_ADDRESS`: the address to add

These variables are set by first sourcing the `vip-common.conf` file and then
sourcing a `vip-unique_id.conf` file within `/etc/ucarp`. The `unique_id` comes
from the systemd service name. For example, if the service is `ucarp@foo.service`
then the associated VIP file would be `/etc/ucarp/vip-foo.conf`.

Given the following values and the defaults from the shipped `vip-common.conf`:

+ `unique_id`: "foo"
+ `VID`: 1
+ `PASSWORD`: "/etc/ucarp/password_file"
+ `BIND_INTERFACE`: "eth0"
+ `SOURCE_ADDRESS`: "10.10.10.5"
+ `VIP_ADDRESS`: "10.10.10.25"

The following will be executed:

```
/usr/sbin/ucarp --interface=eth0 --pass=/etc/ucarp/password_file \
  --srcip=10.10.10.5 --vhid=1 --addr=10.10.10.25 \
  --upscript=/usr/libexec/ucarp/vip-up --downscript=/usr/libexec/ucarp/vip-down \
  --pidfile=/var/tmp/foo.pid
```

Note: you may also specify a `OPTIONS` variable in your VIP config. The value
of this variable will be substituted as-is prior to the `--upscript` parameter.

# systemd enablement
Given a VIP config `/etc/ucarp/vip-foo.conf`, and a fresh install that has not been
enabled yet:

1. `systemctl enable ucarp.service`
2. `systemctl enable ucarp@foo.service`
3. `systemctl start ucarp.service`
