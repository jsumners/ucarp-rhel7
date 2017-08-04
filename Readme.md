This repository provides a script for building an alternate UCarp RPM for
RHEL 7 systems. The one shipped via the EPEL seems to be a very cursory
update from the RHEL 6 RPM. The EPEL RPM ships a templated systemd
service, but the startup script invoked by that service starts _all_ VIPs defined
in `/etc/ucarp`. This is the wrong thing to do under systemd. Therefore, this RPM
ships a start script that runs a single named VIP for each templated service. Thus,
for the services:

+ `/etc/systemd/system/ucarp.service.wants/ucarp@foo.service`
+ `/etc/systemd/system/ucarp.service.wants/ucarp@bar.service`

There will be two separate processes started.

Additionally, this RPM is built against the [pidfile branch](https://github.com/jsumners/UCarp/tree/pidfile)
of UCarp. This further completes the systemd integration, as systemd recommends
adding the `PIDFile=` parameter to a service that has `Type=forking`.

Other than that, the RPM borrows from the EPEL source --
https://src.fedoraproject.org/cgit/rpms/ucarp.git

# Important

The resulting RPM name, and yum installable name, is "ucarp-jbs" ("jbs" being this
project author's initials). The installed binaries are still their standard names,
e.g. "ucarp". Thus, the resulting RPM conflicts with the EPEL provided RPM.
