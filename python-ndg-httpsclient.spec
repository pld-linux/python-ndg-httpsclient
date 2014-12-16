#
# Conditional build:
%bcond_without	tests	# do not perform "make test"

%define 	module	ndg-httpsclient
Summary:	Enhanced HTTPS support for httplib and urllib2 using PyOpenSSL
Summary(pl.UTF-8):	Rozszerzona obsługa HTTPS dla modułów httplib i urllib2 poprzez PyOpenSSL
Name:		python-%{module}
Version:	0.3.3
Release:	1
License:	BSD
Group:		Libraries/Python
Source0:	https://pypi.python.org/packages/source/n/ndg-httpsclient/ndg_httpsclient-%{version}.tar.gz
# Source0-md5:	c05794017dedee47b297185d82ef795e
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

%description -l pl.UTF-8
Ten moduł to implementacja klienta HTTPS dla modułów httplib i urllib2
oparta na module PyOpenSSL. PyOpenSSL udostępnia pełniejszą
implementację SSL niż domyślnie dostarczana z Pythonem i umożliwia
pełną weryfikację drugiej strony połączenia SSL.

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

%py_comp $RPM_BUILD_ROOT%{py_sitescriptdir}
%py_ocomp $RPM_BUILD_ROOT%{py_sitescriptdir}
%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/ndg_httpclient
%{py_sitescriptdir}/ndg
%if "%{py_ver}" > "2.4"
%{py_sitescriptdir}/ndg_httpsclient-%{version}-py*.egg-info
%{py_sitescriptdir}/ndg_httpsclient-%{version}-py*-nspkg.pth
%endif
