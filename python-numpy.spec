%define enable_atlas 0
%{?_with_atlas: %global enable_atlas 1}

%define module	numpy
%define name	python-%{module}
%define version 1.5.0
%define release %mkrel 4
%define epoch 	1

# disable this for bootstrapping nose and sphinx
%define enable_tests 0
%define enable_doc 0

Summary:	A fast multidimensional array facility for Python
Name:		python-%{module}
Version:	%{version}
Epoch:		%{epoch}
Release:	%{release}
License:	BSD
Group:		Development/Python
Url: 		http://numpy.scipy.org
Source0:	http://downloads.sourceforge.net/numpy/%{module}-%{version}.tar.gz
Patch0:		doc-build-fix-1.5.0.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
Provides:	f2py
Obsoletes:	f2py
%if %enable_atlas
BuildRequires:	libatlas-devel
%else
BuildRequires:	blas-devel
%endif
BuildRequires:	lapack-devel
BuildRequires:	gcc-gfortran >= 4.0
%if %enable_doc
BuildRequires:	python-sphinx >= 1.0
BuildRequires:	python-matplotlib
%endif
%if %enable_tests
BuildRequires:	python-nose
%endif
%py_requires -d

%description
Numpy is a general-purpose array-processing package designed to
efficiently manipulate large multi-dimensional arrays of arbitrary
records without sacrificing too much speed for small multi-dimensional
arrays. Numpy is built on the Numeric code base and adds features
introduced by numarray as well as an extended C-API and the ability to
create arrays of arbitrary type.

Numpy also provides facilities for basic linear algebra routines,
basic Fourier transforms, and random number generation.

%package devel
Summary:	Numpy headers and development tools
Group:		Development/Python
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description devel
This package contains tools and header files need to develop modules 
in C and Fortran that can interact with Numpy

%prep
%setup -q -n %{module}-%{version}
%patch0 -p1

%build
CFLAGS="%{optflags} -fPIC -O3" PYTHONDONTWRITEBYTECODE= %{__python} setup.py config_fc --fcompiler=gnu95 build

%if %enable_doc
pushd doc
export PYTHONPATH=`dir -d ../build/lib.linux*`
%make html
popd
%endif

%install
%__rm -rf %{buildroot}
CFLAGS="%{optflags} -fPIC -O3" PYTHONDONTWRITEBYTECODE= %{__python} setup.py install --root=%{buildroot} 

%__rm -rf docs-f2py; %__mv %{buildroot}%{py_platsitedir}/%{module}/f2py/docs docs-f2py
%__mv -f %{buildroot}%{py_platsitedir}/%{module}/f2py/f2py.1 f2py.1
%__install -D -p -m 0644 f2py.1 %{buildroot}%{_mandir}/man1/f2py.1

%__rm -rf %{buildroot}%{py_platsitedir}/%{module}/tools/

# Remove doc files that should be in %doc:
%__rm -f %{buildroot}%{py_platsitedir}/%{module}/COMPATIBILITY
%__rm -f %{buildroot}%{py_platsitedir}/%{module}/*.txt
%__rm -f %{buildroot}%{py_platsitedir}/%{module}/site.cfg.example

%check
%if %enable_tests
# Don't run tests from within main directory to avoid importing the uninstalled numpy stuff:
pushd doc &> /dev/null
PYTHONPATH="%{buildroot}%{py_platsitedir}" %{__python} -c "import numpy; numpy.test()"
popd &> /dev/null
%endif

%clean
%__rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%doc LICENSE.txt README.txt THANKS.txt DEV_README.txt COMPATIBILITY site.cfg.example 
%if %enable_doc
%doc doc/build/html
%endif
%dir %{py_platsitedir}/%{module}
%{py_platsitedir}/%{module}/*.py*
%{py_platsitedir}/%{module}/core/ 
%{py_platsitedir}/%{module}/compat/
%{py_platsitedir}/%{module}/doc/
%exclude %{py_platsitedir}/%{module}/core/include/
%{py_platsitedir}/%{module}/fft/
%{py_platsitedir}/%{module}/lib/
%{py_platsitedir}/%{module}/linalg/
%{py_platsitedir}/%{module}/ma/
%{py_platsitedir}/%{module}/matrixlib/
%{py_platsitedir}/%{module}/numarray/
%exclude %{py_platsitedir}/%{module}/numarray/include/
%{py_platsitedir}/%{module}/oldnumeric/
%{py_platsitedir}/%{module}/polynomial/
%{py_platsitedir}/%{module}/random/
%exclude %{py_platsitedir}/%{module}/random/randomkit.h
%{py_platsitedir}/%{module}/testing/
%{py_platsitedir}/%{module}/tests/ 
%{py_platsitedir}/%{module}-*.egg-info

%files devel
%defattr(-,root,root,-)
%{_bindir}/f2py
%{_mandir}/man1/f2py.*
%{py_platsitedir}/%{module}/core/include/
%{py_platsitedir}/%{module}/numarray/include/
%{py_platsitedir}/%{module}/distutils/
%{py_platsitedir}/%{module}/f2py/
%{py_platsitedir}/%{module}/random/randomkit.h
