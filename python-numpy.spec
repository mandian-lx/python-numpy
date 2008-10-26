%define module	numpy

Summary:	Python array processing for numbers, strings, records, and objects
Name:		python-%{module}
Version:	1.2.0
Release:	%mkrel 1
License:	BSD
Group:		Development/Python
Url: 		http://numpy.scipy.org
Source0:	http://downloads.sourceforge.net/numpy/%{module}-%{version}.tar.lzma
Requires:	python >= 2.4
BuildRequires:	python-devel >= 2.4
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
arrays. Numpy is built on the Numeric code base and adds features
introduced by numarray as well as an extended C-API and the ability to
create arrays of arbitrary type.

Numpy also provides facilities for basic linear algebra routines,
basic Fourier transforms, and random number generation.

%package devel
Summary:	Numpy library C bindings
Group:		Development/Python
Requires:	%{name} = %{version}-%{release}

%description devel
Install this if you need to access the Numpy C bindings.

%prep
%setup -q -n %{module}-%{version}

%build
CFLAGS="%{optflags} -fPIC" %{__python} setup.py config_fc --fcompiler=gnu95 build

%install
%__rm -rf %{buildroot}

# Don't use --skip-build because it will cause some files to be left out of 
# the file list:
%{__python} setup.py install --root=%{buildroot} --record=FILELIST_ORIG.tmp

# Don't include original test files and ghost optimized bytecode files:
%__grep -Ev "\\.orig$" FILELIST_ORIG.tmp | %__sed 's/\(.*\.pyo\)/%ghost \1/' > FILELIST.tmp

# Move development files to multiarch-compliant location:
%__grep -Ev "include/numpy|\\.h$|\\.c$" FILELIST.tmp > FILELIST
%__grep -E "include/numpy|\\.h$|\\.c$" FILELIST.tmp > FILELIST_DEVEL
#%__grep -E "include/numpy|\\.h$|\\.c$" FILELIST.tmp > FILELIST_DEVEL.tmp
#%__mkdir -p -m 755 %{buildroot}%{multiarch_includedir}/python%{py_ver}/numpy
#for i in `%__cat FILELIST_DEVEL.tmp`; do
#   %__mv %{buildroot}$i %{buildroot}%{multiarch_includedir}/python%{py_ver}/numpy
#   j=`basename $i`
#   echo %{multiarch_includedir}/python%{py_ver}/numpy/$j >> FILELIST_DEVEL
#done

%clean
%__rm -rf %{buildroot}

%files -f FILELIST
%defattr(-,root,root)
%doc *.txt

%files devel -f FILELIST_DEVEL
%defattr(-,root,root,-)
%doc *.txt
