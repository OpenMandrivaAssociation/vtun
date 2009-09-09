Summary:	Virtual tunnel over TCP/IP networks
Name:		vtun
Version:	3.0.2
Release:	%mkrel 2
License:	GPL
Group:		Networking/Other
URL:		http://vtun.sourceforge.net/
Source:		%{name}-%{version}.tar.gz
Source1:	vtund.init.tar.bz2
Obsoletes:	vppp
Provides:	vppp
BuildRequires:	zlib1-devel bison openssl-devel flex
Requires(post): rpm-helper
Requires(preun): rpm-helper
Requires(pre): rpm-helper
Requires(postun): rpm-helper
#JMD: For static binary
BuildRequires:	openssl-static-devel, glibc-static-devel
BuildRoot:	%_tmppath/%{name}-buildroot

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

%make \
    CFG_FILE=%{_sysconfdir}/vtund.conf \
    PID_FILE=/var/run/vtund.pid  \
    STAT_DIR=/var/log/vtund \
    LOCK_DIR=/var/lock/vtund

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/var/{log,lock}/vtund
tar -jxvf %{SOURCE1} -C $RPM_BUILD_ROOT
install vtund -D ${RPM_BUILD_ROOT}/%{_sbindir}/vtund
install scripts/reroute ${RPM_BUILD_ROOT}/%{_sbindir}

install vtund.8 -D ${RPM_BUILD_ROOT}/%{_mandir}/man8/vtund.8
install  vtund.conf.5 -D ${RPM_BUILD_ROOT}/%{_mandir}/man5/vtund.5

%clean
rm -rf $RPM_BUILD_ROOT

%post
%_post_service vtund
%_post_service vtunc

%preun
%_preun_service vtund
%_preun_service vtunc

%files
%defattr(644,root,root,755)
%doc ChangeLog Credits FAQ README README.Setup README.Shaper TODO
%doc vtund.conf
%config(noreplace) %_sysconfdir/xinetd.d/vtun
%config(noreplace) %_sysconfdir/sysconfig/vtun?
%_initrddir/vtun?
%dir /var/log/vtund
%dir /var/lock/vtund
%_mandir/man8/*
%_mandir/man5/*
%defattr(755,root,root,755)
%_sbindir/vtund
%_sbindir/reroute


