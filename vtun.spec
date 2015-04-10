%define debug_package	%{nil}

Summary:	Virtual tunnel over TCP/IP networks
Name:		vtun
Version:	3.0.3
Release:	2
License:	GPLv2
Group:		Networking/Other
URL:		http://vtun.sourceforge.net/
Source0:	http://downloads.sourceforge.net/project/vtun/vtun/%{version}/%{name}-%{version}.tar.gz
Source1:	vtun.socket
Source2:	vtun.service

Provides:	vppp
BuildRequires:	zlib-devel bison openssl-devel flex
Requires(post): rpm-helper
Requires(preun): rpm-helper
Requires(pre): rpm-helper
Requires(postun): rpm-helper
#JMD: For static binary
BuildRequires:	openssl-static-devel, glibc-static-devel
BuildRequires: gcc-c++, gcc, gcc-cpp

%description
VTun provides the method for creating Virtual Tunnels over TCP/IP networks
and allows to shape, compress, encrypt traffic in that tunnels. 
Supported type of tunnels are: PPP, IP, Ethernet and most of other serial 
protocols and programs.

VTun is easily and highly configurable, it can be used for various network
tasks like VPN, Mobil IP, Shaped Internet access, IP address saving, etc.
It is completely user space implementation and does not require modification
to any kernel parts. 

%prep

%setup -q

%build
export CC=gcc
export CXX=g++

%configure \
    --localstatedir=%{_localstatedir}/lib/%{name} \
    --enable-ssl \
    --disable-lzo

#JMD: for static binary
#perl -pi -e "s/-lz/-Wl,-static -lz/g;" Makefile


#JMD: use this so we get Unix98 pty support

cat << EOF >> config.h
#define HAVE_GETPT
#define HAVE_GRANTPT
#define HAVE_UNLOCKPT
#define HAVE_PTSNAME
EOF

%make

%install
make install DESTDIR=%{buildroot} INSTALL_OWNER= INSTALL="/usr/bin/install -p"
install -D -m 0644 -p %{SOURCE1} %{buildroot}/%{_unitdir}/vtun.socket
install -D -m 0644 -p %{SOURCE2} %{buildroot}/%{_unitdir}/vtun.service


%post
%_post_service vtun.service
%_post_service vtun.socket

%preun
%_preun_service vtun.service
%_preun_service vtun.socket

%files
%defattr(644,root,root,755)
%doc ChangeLog Credits FAQ README README.LZO README.Setup README.Shaper TODO vtund.conf
%config(noreplace) %{_sysconfdir}/vtund.conf
%{_unitdir}/vtun.socket
%{_unitdir}/vtun.service
%{_sbindir}/vtund
%dir %{_localstatedir}/lib/vtun
%{_mandir}/man5/vtund.conf.5*
%{_mandir}/man8/vtun.8*
%{_mandir}/man8/vtund.8*
