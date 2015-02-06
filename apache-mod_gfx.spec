#Module-Specific definitions
%define mod_name mod_gfx
%define mod_conf B52_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	Performs image operations on the fly
Name:		apache-%{mod_name}
Version:	0.1
Release: 	8
Group:		System/Servers
License:	GPLv3
URL:		http://nauticaltech.com/software/mod_gfx/
Source0:	http://nauticaltech.com/software/mod_gfx/%{mod_name}-%{version}.tar.gz
Source1:	%{mod_conf}
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= 2.2.0
Requires(pre):	apache >= 2.2.0
Requires:	apache-conf >= 2.2.0
Requires:	apache >= 2.2.0
BuildRequires:	apache-devel >= 2.2.0
BuildRequires:	libgd-devel

%description
mod_gfx is a configurable Apache module that uses libgd to perform image
operations on the fly. Some of the supported image operations are: resize,
resample, watermark, and crop. A couple of its special features are origin
selection via URI regex and round-robin over a list of hosts.

%prep

%setup -q -n %{mod_name}-%{version}

cp %{SOURCE1} %{mod_conf}

%build
%{_bindir}/apxs -Iinclude -c module/%{mod_name}.c -lgd

%install

install -d %{buildroot}%{_sysconfdir}/httpd/modules.d
install -d %{buildroot}%{_libdir}/apache-extramodules

install -m0755 module/.libs/%{mod_so} %{buildroot}%{_libdir}/apache-extramodules/
install -m0644 %{mod_conf} %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

%post
if [ -f %{_var}/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f %{_var}/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart 1>&2
    fi
fi

%clean

%files
%doc Benchmark README
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}



%changelog
* Sat Feb 11 2012 Oden Eriksson <oeriksson@mandriva.com> 0.1-7mdv2012.0
+ Revision: 772661
- rebuild

* Tue May 24 2011 Oden Eriksson <oeriksson@mandriva.com> 0.1-6
+ Revision: 678320
- mass rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 0.1-5mdv2011.0
+ Revision: 588004
- rebuild

* Mon Mar 08 2010 Oden Eriksson <oeriksson@mandriva.com> 0.1-4mdv2010.1
+ Revision: 516116
- rebuilt for apache-2.2.15

* Mon Aug 17 2009 Oden Eriksson <oeriksson@mandriva.com> 0.1-3mdv2010.0
+ Revision: 417292
- rebuilt against libjpeg v7

* Sat Aug 01 2009 Oden Eriksson <oeriksson@mandriva.com> 0.1-2mdv2010.0
+ Revision: 406591
- rebuild

* Sun Feb 22 2009 Oden Eriksson <oeriksson@mandriva.com> 0.1-1mdv2009.1
+ Revision: 343853
- import apache-mod_gfx


* Sun Feb 22 2009 Oden Eriksson <oeriksson@mandriva.com> 0.1-1mdv2009.1
- initial Mandriva package
