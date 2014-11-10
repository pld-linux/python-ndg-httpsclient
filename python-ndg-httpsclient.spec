#
# Conditional build:
%bcond_without	tests	# do not perform "make test"

%define 	module	ndg-httpsclient
Summary:	Provides enhanced HTTPS support for httplib and urllib2 using PyOpenSSL
Name:		python-%{module}
Version:	0.3.2
Release:	1
License:	BSD
Group:		Libraries/Python
Source0:	https://pypi.python.org/packages/source/n/ndg-httpsclient/ndg_httpsclient-%{version}.tar.gz
# Source0-md5:	076303c7aa0e41f3b45a7cb43dbb0743
URL:		http://ndg-security.ceda.ac.uk/wiki/ndg_httpsclient
BuildRequires:	python-distribute
BuildRequires:	python-pyOpenSSL
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
Requires:	python-modules
Requires:	python-pyOpenSSL
Requires:	python-pyasn1
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is a HTTPS client implementation for httplib and urllib2 based on
PyOpenSSL. PyOpenSSL provides a more fully featured SSL implementation
over the default provided with Python and importantly enables full
verification of the SSL peer.

%prep
%setup -q -n ndg_httpsclient-%{version}

%build
%{__python} setup.py build --build-base build-2 %{?with_tests:test}

%install
rm -rf $RPM_BUILD_ROOT

%{__python} setup.py \
	build --build-base build-2 \
	install --skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/ndg_httpclient
%{py_sitescriptdir}/ndg
%if "%{py_ver}" > "2.4"
%{py_sitescriptdir}/ndg_httpsclient-%{version}-py*.egg-info
%endif
