%global package_speccommit a509568573bfb03b491aaac218964cb95625e7bb
%global package_srccommit v0.34.1
Summary: Xapi storage script plugin server
Name:    xapi-storage-script
Version: 0.34.1
Release: 8%{?xsrel}%{?dist}
License: LGPL-2.1-or-later WITH OCaml-LGPL-linking-exception
URL:     https://github.com/xapi-project/xapi-storage-script
Source0: xapi-storage-script-0.34.1.tar.gz
Source1: xapi-storage-script.service
Source2: xapi-storage-script-sysconfig
Source3: xapi-storage-script-conf.in
BuildRequires: ocaml-ocamldoc
BuildRequires: xs-opam-repo
BuildRequires: ocaml-xcp-idl-devel
BuildRequires: message-switch-devel
BuildRequires: xapi-storage-ocaml-plugin-devel
BuildRequires: systemd
BuildRequires: xapi-storage
BuildRequires: python

Requires:       jemalloc
%{?systemd_requires}

%description
Allows script-based Xapi storage adapters.

%prep
%autosetup -p1

%build
make
sed -e "s|@LIBEXECDIR@|%{_libexecdir}|g" %{SOURCE3} > xapi-storage-script.conf

%check
# they are marked as executable in git, seem to loose executable bit after patchqueue from PINning
chmod +x test/volume/*/*.py
make test

%install
mkdir -p %{buildroot}%{_libexecdir}/xapi-storage-script/volume
mkdir -p %{buildroot}%{_libexecdir}/xapi-storage-script/datapath
mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_mandir}/man8
make install BINDIR=%{buildroot}%{_sbindir} MANDIR=%{buildroot}%{_mandir}
%{__install} -D -m 0644 xapi-storage-script.conf %{buildroot}%{_sysconfdir}/xapi-storage-script.conf
%{__install} -D -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/xapi-storage-script.service
%{__install} -D -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/xapi-storage-script

%post
%systemd_post xapi-storage-script.service

%preun
%systemd_preun xapi-storage-script.service

%postun
%systemd_postun xapi-storage-script.service

%files
%{_libexecdir}/xapi-storage-script
%{_sbindir}/xapi-storage-script
%{_mandir}/man8/xapi-storage-script.8*
%{_unitdir}/xapi-storage-script.service
%config(noreplace) %{_sysconfdir}/sysconfig/xapi-storage-script
%config(noreplace) %{_sysconfdir}/xapi-storage-script.conf

%changelog
* Thu Jul 20 2023 Rob Hoes <rob.hoes@citrix.com> - 0.34.1-8
- Bump release and rebuild

* Mon Jun 19 2023 Christian Lindig <christian.lindig@citrix.com> - 0.34.1-7
- Bump release and rebuild

* Thu Jun 08 2023 Christian Lindig <christian.lindig@citrix.com> - 0.34.1-6
- Bump release and rebuild

* Fri May 12 2023 Christian Lindig <christian.lindig@citrix.com> - 0.34.1-5
- Bump release and rebuild

* Fri May 12 2023 Christian Lindig <christian.lindig@citrix.com> - 0.34.1-4
- Bump release and rebuild

* Thu Feb 23 2023 Pau Ruiz Safont <pau.ruizsafont@cloud.com> - 0.34.1-3
- Change license to match source repo

* Mon Sep 27 2021 Pau Ruiz Safont <pau.safont@citrix.com> - 0.34.1-2
- Bump package after xs-opam update

* Mon Aug 23 2021 Pau Ruiz Safont <pau.safont@citrix.com> - 0.34.1-1
- CP-38064: compatibility with Core 0.13

* Tue Jul 13 2021 Edwin Török <edvin.torok@citrix.com> - 0.34.0-2
- bump packages after xs-opam update

* Mon Mar 23 2020 Christian Lindig <christian.lindig@citrix.com> - 0.34.0-1
- Fix Stdlib warning
- Fix Travis

* Fri Aug 23 2019 Edwin Török <edvin.torok@citrix.com> - 0.33.0-2
- bump packages after xs-opam update

* Fri Aug 02 2019 Christian Lindig <christian.lindig@citrix.com> - 0.33.0-1
- CP-31450: Add domid to Datapath.attach

* Tue Jul 30 2019 Christian Lindig <christian.lindig@citrix.com> - 0.32.0-1
- Use syslog from xcp-idl for now
- Simplify travis and update to 4.07

* Tue Dec 04 2018 Christian Lindig <christian.lindig@citrix.com> - 0.31.0-1
- Moved from jbuilder to dune and deprecated xcp in favour of xapi-idl.

* Fri Nov 16 2018 Christian Lindig <christian.lindig@citrix.com> - 0.30.0-1
- New ocaml-rpc

* Thu Nov 01 2018 Christian Lindig <christian.lindig@citrix.com> - 0.29.0-1
- Update opam files for Opam 2

* Mon Sep 24 2018 Christian Lindig <christian.lindig@citrix.com> - 0.28.0-1
- CP-27110: Storage PPX

* Fri Aug 31 2018 Christian Lindig <christian.lindig@citrix.com> - 0.27.0-1
- Simplify PPX processing in jbuild file
- Use OCaml 4.06 for Travis

* Fri Jul 13 2018 Christian Lindig <christian.lindig@citrix.com> - 0.26.0-1
- CA-293335: Don't add extra sr_uuid to device_config on SR.attach
- Only run SR.create compat fallback for PVS version of SM scripts

* Thu Jun 28 2018 Christian Lindig <christian.lindig@citrix.com> - 0.25.0-1
- CA-292370: Remove uri from returned plugin configuration info
- CP-27591: Convert to new xapi-storage interface based on ocaml-rpc's IDL
- CP-27591: Make script names case-insensitive
- CP-28132: Update after Datapath.attach changes
- CP-28132: Remove unused code for handling VDI.attach
- CP-28132: Add 5.0 to supported API versions
- CP-28546: Move everything from v4 to v5
- CP-28546: Remove 4.0 from supported_api_versions
- CP-28546: check that datapath plugin version is compatible
- CP-28132: remove domain_uuid from attach response
- Add more type annotations
- Don't remove uri key from device_config in compat_uri

* Fri Jun 15 2018 Christian Lindig <christian.lindig@citrix.com> - 0.24.0-1
- CA-290241: save VDI's is_a_snapshot & snapshot_of fields

* Mon May 14 2018 Christian Lindig <christian.lindig@citrix.com> - 0.23.0-1
- jbuild: update rpc dependency name
- opam: update dependencies

* Thu May 10 2018 Christian Lindig <christian.lindig@citrix.com> - 0.22.0-1
- CP-26583: Update Rrdd references to use PPX port
- CP-26583: Add Rpc_async module to jbuild for PPX port

* Tue Apr 10 2018 Christian Lindig <christian.lindig@citrix.com> - 0.21.0-1
- CA-283693: Store & return correct snapshot_time for VDIs
- Update .travis.yml

* Wed Apr 04 2018 Christian Lindig <christian.lindig@citrix.com> - 0.20.0-1
- CP-26340: SR.probe, SR.create and SR.attach API changes
- CP-26340: SR.probe changes to match xcp-idl
- Update after xcp-idl changes
- Add a unit test for v4 API
- Add SR probe test
- Fix Rpc.Runtime_error("Enum[String s;...]", _)
- Changes after adding SR UUID to sr_info in xcp-idl
- Report SR_PROBE capability
- CA-284508: SR.attach expects an sr_uuid inside device-config, but on
  the CLI iti's outside: xe pbd-create sr-uuid=...

* Wed Feb 28 2018 Christian Lindig <christian.lindig@citrix.com> - 0.19.0-1
- CA-283728: check for required_api_version
- CA-283728: backward compatible return types for SR.create
- CA-283728: backward compatibility for uuid
- CA-283728: dummy SR for unit tests

* Fri Feb 23 2018 Edwin Török <edvin.torok@citrix.com> - 0.18.0-2
- CA-283728: run xapi-storage-script unit tests

* Fri Feb 09 2018 Christian Lindig <christian.lindig@citrix.com> - 0.18.0-1
- CP-23027: Plumb through new URI returned in SR.create
- CP-24350: plumb through sharable flag
- Store VDI type in the 'keys' field of the volume
- CA-272163: convert exceptions from SMAPIv3 backend
- CA-277837: plumb through uuid for SR.attach
- fix compiler warnings on unused opens and deprecated functions

* Wed Jan 31 2018 Christian Lindig <christian.lindig@citrix.com> - 0.17.0-1
- CP-26711: The storage library has been renamed after porting to jbuilder.

* Fri Jan 26 2018 Christian Lindig <christian.lindig@citrix.com> - 0.16.0-1
- Use Core, Async instead of their deprecated Std submodules
- Move to Core.Unix.Syslog module
- Update after Async bind signature change
- Add needed ~equal params after List signature change in Core
- Update due to upstream core_kernel updates to 0.10.0

* Fri Jan 19 2018 Christian Lindig <christian.lindig@citrix.com> - 0.15.0-1
- CP-26574: Ported build from oasis to jbuilder.

* Mon Jan 15 2018 Konstantina Chremmou <konstantina.chremmmou@citrix.com> - 0.14.0-2
- Ported build from oasis to jbuilder

* Fri Oct 13 2017 Rob Hoes <rob.hoes@citrix.com> - 0.14.0-1
- Add cbt_enabled=false field to vdi_of_volume to fix compilation

* Mon Mar 13 2017 Marcello Seri <marcello.seri@citrix.com> - 0.13.0-2
- Update OCaml dependencies and build/install script after xs-opam-repo split

* Thu Mar 09 2017 Rob Hoes <rob.hoes@citrix.com> - 0.13.0-1
- Port xapi-storage-script to new ppx-based modules

* Fri Feb 17 2017 Frederico Mazzone <frederico.mazzone@citrix.com> - 0.12.3-2
- CA-243676: Do not restart toolstack services on RPM upgrade

* Tue Jan 10 2017 Rob Hoes <rob.hoes@citrix.com> - 0.12.3-1
- git: Add metadata to the result of `git archive`

* Thu Sep 22 2016 Rob Hoes <rob.hoes@citrix.com> - 0.12.2-1
- Update to 0.12.2

* Mon Aug 22 2016 Rafal Mielniczuk <rafal.mielniczuk@citrix.com> - 0.12.1-3
- Package for systemd

* Mon May 16 2016 Si Beaumont <simon.beaumont@citrix.com> - 0.12.1-2
- Re-run chkconfig on upgrade

* Wed Feb 03 2016 Euan Harris <euan.harris@citrix.com> - 0.12.1-1
- Update to 0.12.1

* Tue Sep 15 2015 David Scott <dave.scott@citrix.com> - 0.12.0-3
- Bump release

* Wed Sep  9 2015 David Scott <dave.scott@citrix.com> - 0.12.0-1
- Update to 0.12.0

* Fri Aug  7 2015 David Scott <dave.scott@citrix.com> - 0.11.0-1
- Update to 0.11.0

* Tue Aug  4 2015 David Scott <dave.scott@citrix.com> - 0.10.0-1
- Update to 0.10.0

* Mon Jul 20 2015 David Scott <dave.scott@citrix.com> - 0.9.0-2
- Backport robustness patch

* Wed Jul 15 2015 David Scott <dave.scott@citrix.com> - 0.9.0-1
- Update to 0.9.0

* Wed Jul 15 2015 David Scott <dave.scott@citrix.com> - 0.8.0-2
- Backport clone-on-boot fix

* Wed Jul 15 2015 David Scott <dave.scott@citrix.com> - 0.8.0-1
- Update to 0.8.0

* Thu Jul 9 2015 David Scott <dave.scott@citrix.com> - 0.7.0-1
- Update to 0.7.0

* Wed Jul 8 2015 David Scott <dave.scott@citrix.com> - 0.6.0-1
- Update to 0.6.0

* Tue Jul 7 2015 David Scott <dave.scott@citrix.com> - 0.5.0-1
- Update to 0.5.0

* Tue Apr 28 2015 David Scott <dave.scott@citrix.com> - 0.4.0-1
- Update to 0.4.0

* Fri Apr 24 2015 David Scott <dave.scott@citrix.com> - 0.3.0-1
- Update to 0.3.0

* Sat Apr  4 2015 David Scott <dave.scott@citrix.com> - 0.2.0-1
- Update to 0.2.0

* Sun Oct 19 2014 David Scott <dave.scott@citrix.com> - 0.1.2-1
- Write the pidfile properly
- VDI.epoch_{begin,end} are no-ops

* Fri Oct 17 2014 David Scott <dave.scott@citrix.com> - 0.1.1-1
- Add the /volume and /datapath subdirectories to the package
- Fix daemonization
- Use syslog

* Thu Oct 16 2014 David Scott <dave.scott@citrix.com> - 0.1-1
- Initial package
