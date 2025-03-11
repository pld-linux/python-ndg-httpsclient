#
# Conditional build:
%bcond_with	tests	# tests [require localhost networking]
%bcond_without	python2	# CPython 2.x module
%bcond_without	python3	# CPython 3.x module

%define 	module	ndg-httpsclient
Summary:	Enhanced HTTPS support for httplib and urllib2 using PyOpenSSL
Summary(pl.UTF-8):	Rozszerzona obsługa HTTPS dla modułów httplib i urllib2 poprzez PyOpenSSL
Name:		python-%{module}
Version:	0.4.2
Release:	11
License:	BSD
Group:		Libraries/Python
Source0:	https://github.com/cedadev/ndg_httpsclient/archive/%{version}.tar.gz
# Source0-md5:	08236101a72bb18f9f62c123d199420b
Patch0:		%{name}-tests.patch
URL:		http://ndg-security.ceda.ac.uk/wiki/ndg_httpsclient
%if %{with python2}
BuildRequires:	python-modules >= 1:2.6
BuildRequires:	python-pyOpenSSL
BuildRequires:	python-setuptools
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.2
BuildRequires:	python3-pyOpenSSL
BuildRequires:	python3-setuptools
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
Requires:	python-modules >= 1:2.6
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

%package -n python3-%{module}
Summary:	Enhanced HTTPS support for httplib and urllib2 using PyOpenSSL
Summary(pl.UTF-8):	Rozszerzona obsługa HTTPS dla modułów httplib i urllib2 poprzez PyOpenSSL
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.2
Requires:	python3-pyOpenSSL
Requires:	python3-pyasn1

%description -n python3-%{module}
This is a HTTPS client implementation for httplib and urllib2 based on
PyOpenSSL. PyOpenSSL provides a more fully featured SSL implementation
over the default provided with Python and importantly enables full
verification of the SSL peer.

%description -n python3-%{module} -l pl.UTF-8
Ten moduł to implementacja klienta HTTPS dla modułów httplib i urllib2
oparta na module PyOpenSSL. PyOpenSSL udostępnia pełniejszą
implementację SSL niż domyślnie dostarczana z Pythonem i umożliwia
pełną weryfikację drugiej strony połączenia SSL.

%prep
%setup -q -n ndg_httpsclient-%{version}
%patch -P 0 -p1

%build
%if %{with python2}
%py_build

%if %{with tests}
TOPDIR=$(pwd)
cd ndg/httpsclient/test
./scripts/openssl_https_server.sh &
HTTPDPID=$!
sleep 1
trap "kill $HTTPDPID" ERR
for test in test_*.py ; do
PYTHONPATH=$TOPDIR/build-2/lib %{__python} $test
done
kill $HTTPDPID
trap - ERR
cd ../../..
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
TOPDIR=$(pwd)
cd ndg/httpsclient/test
./scripts/openssl_https_server.sh &
HTTPDPID=$!
sleep 1
trap "kill $HTTPDPID" ERR
for test in test_*.py ; do
PYTHONPATH=$TOPDIR/build-3/lib %{__python3} $test
done
kill $HTTPDPID
trap - ERR
cd ../../..
%endif
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%{__rm} -r $RPM_BUILD_ROOT%{py_sitescriptdir}/ndg/httpsclient/test
%endif

%if %{with python3}
%py3_install

%{__rm} -r $RPM_BUILD_ROOT%{py3_sitescriptdir}/ndg/httpsclient/test
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc README.md ndg/httpsclient/LICENSE
%{py_sitescriptdir}/ndg
%if "%{py_ver}" > "2.4"
%{py_sitescriptdir}/ndg_httpsclient-%{version}-py*.egg-info
%{py_sitescriptdir}/ndg_httpsclient-%{version}-py*-nspkg.pth
%endif
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc README.md ndg/httpsclient/LICENSE
%attr(755,root,root) %{_bindir}/ndg_httpclient
%{py3_sitescriptdir}/ndg
%{py3_sitescriptdir}/ndg_httpsclient-%{version}-py*.egg-info
%{py3_sitescriptdir}/ndg_httpsclient-%{version}-py*-nspkg.pth
%endif
