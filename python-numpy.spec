%define module	numpy

Summary:	Python array processing for numbers, strings, records, and objects
Name:		python-%{module}
Version:	1.1.0
Release:	%mkrel 2
License:	BSD
Group:		Development/Python
Url: 		http://numpy.scipy.org
Source0:	http://downloads.sourceforge.net/numpy/%{module}-%{version}.tar.bz2
Requires:	python >= 2.0
BuildRequires:	python-devel >= 2.0
BuildRequires:	blas-devel
BuildRequires:	lapack-devel
BuildRequires:	gcc-gfortran >= 4.0
Provides:	f2py
Obsoletes:	f2py
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Numpy is a general-purpose array-processing package designed to
efficiently manipulate large multi-dimensional arrays of arbitrary
records without sacrificing too much speed for small multi-dimensional
arrays.  Numpy is built on the Numeric code base and adds features
introduced by numarray as well as an extended C-API and the ability to
create arrays of arbitrary type.

There are also basic facilities for discrete fourier transform,
basic linear algebra and random number generation.

%package devel
Summary:	Numpy library C bindings
Group:		Development/Python
Requires:	%{name} = %{version}-%{release}

%description devel
Install this if you need to access the numpy C bindings.

%prep
%setup -q -n %{module}-%{version}

%build
CFLAGS="%{optflags} -fPIC" %{__python} setup.py config_fc --fcompiler=gnu95 build

%install
%__rm -rf %{buildroot}

# Don't use --skip-build because it will cause some files to be left out of 
# the file list:
%{__python} setup.py install --root=%{buildroot} --record=INSTALLED_FILES_ORIG.tmp

# Don't include original test files and ghost optimized bytecode files:
%__grep -Ev "\\.orig$" INSTALLED_FILES_ORIG.tmp | %__sed 's/\(.*\.pyo\)/%ghost \1/' > INSTALLED_FILES.tmp

# Move development files to multiarch-compliant location:
%__grep -Ev "include/numpy|\\.h$|\\.c$" INSTALLED_FILES.tmp > INSTALLED_FILES
%__grep -E "include/numpy|\\.h$|\\.c$" INSTALLED_FILES.tmp > INSTALLED_FILES_DEVEL
#%__grep -E "include/numpy|\\.h$|\\.c$" INSTALLED_FILES.tmp > INSTALLED_FILES_DEVEL.tmp
#%__mkdir -p -m 755 %{buildroot}%{multiarch_includedir}/python%{py_ver}/numpy
#for i in `%__cat INSTALLED_FILES_DEVEL.tmp`; do
#   %__mv %{buildroot}$i %{buildroot}%{multiarch_includedir}/python%{py_ver}/numpy
#   j=`basename $i`
#   echo %{multiarch_includedir}/python%{py_ver}/numpy/$j >> INSTALLED_FILES_DEVEL
#done

%clean
%__rm -rf %{buildroot}

%files -f INSTALLED_FILES
%defattr(-,root,root)
%doc *.txt

%files devel -f INSTALLED_FILES_DEVEL
%defattr(-,root,root,-)
%doc *.txt
