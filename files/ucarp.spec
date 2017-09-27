%define _hardened_build 1
%define realname ucarp
Summary: Common Address Redundancy Protocol (CARP) for Unix
Name: ucarp-jbs
Version: 1.5.2
Release: 4%{?dist}
# See the COPYING file which details everything
License: MIT and BSD
URL: http://www.ucarp.org/
Provides: ucarp
Conflicts: ucarp

Source0: ucarp-jbs-%{version}.tar
Source1: ucarp@.service
Source2: vip-unique_id.conf.example
Source3: vip-common.conf
Source4: vip-up
Source5: vip-down
Source6: ucarp
Source7: README.md
Source8: ucarp.service

BuildRequires: gettext
BuildRequires: autoconf, automake, libtool
BuildRequires: libpcap-devel
BuildRequires: systemd

Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description
UCARP allows a couple of hosts to share common virtual IP addresses in order
to provide automatic failover. It is a portable userland implementation of the
secure and patent-free Common Address Redundancy Protocol (CARP, OpenBSD's
alternative to the patents-bloated VRRP).
Strong points of the CARP protocol are: very low overhead, cryptographically
signed messages, interoperability between different operating systems and no
need for any dedicated extra network link between redundant hosts.


%prep
%setup -q

%build
%configure
%{__make} %{?_smp_mflags}


%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR=%{buildroot}
%find_lang %{realname}

# Install the unit file
%{__install} -D -p -m 0755 %{SOURCE1} \
    %{buildroot}%{_unitdir}/ucarp@.service
%{__install} -D -p -m 0755 %{SOURCE8} \
    %{buildroot}%{_unitdir}/ucarp.service

%{__mkdir_p} %{buildroot}/etc/ucarp
%{__mkdir_p} %{buildroot}%{_libexecdir}/ucarp

# Install the example config files
%{__install} -D -p -m 0600 %{SOURCE2} %{SOURCE3} %{SOURCE7} \
    %{buildroot}/etc/ucarp/

# Install helper scripts
%{__install} -D -p -m 0700 %{SOURCE4} %{SOURCE5} %{SOURCE6} \
    %{buildroot}%{_libexecdir}/ucarp/


%clean
%{__rm} -rf %{buildroot}

%post
%systemd_post ucarp@.service

%preun
%systemd_preun ucarp@.service

%postun
%systemd_postun_with_restart ucarp@.service


%files -f %{realname}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog NEWS README
%{_unitdir}/ucarp@.service
%{_unitdir}/ucarp.service
%attr(0700,root,root) %dir /etc/ucarp/
%config(noreplace) /etc/ucarp/vip-common.conf
/etc/ucarp/vip-unique_id.conf.example
/etc/ucarp/README.md
%config(noreplace) %{_libexecdir}/ucarp/
%{_sbindir}/ucarp

%changelog
* Fri Aug 04 2017 James Sumners <james.sumners@gmail.com> - 1.5.2-1
- Initial release
