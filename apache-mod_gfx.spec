#Module-Specific definitions
%define mod_name mod_gfx
%define mod_conf B52_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	Performs image operations on the fly
Name:		apache-%{mod_name}
Version:	0.1
Release: 	%mkrel 4
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
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
mod_gfx is a configurable Apache module that uses libgd to perform image
operations on the fly. Some of the supported image operations are: resize,
resample, watermark, and crop. A couple of its special features are origin
selection via URI regex and round-robin over a list of hosts.

%prep

%setup -q -n %{mod_name}-%{version}

cp %{SOURCE1} %{mod_conf}

%build
%{_sbindir}/apxs -Iinclude -c module/%{mod_name}.c -lgd

%install
rm -rf %{buildroot}

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
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc Benchmark README
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}

