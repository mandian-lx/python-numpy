%define enable_atlas 0
%{?_with_atlas: %global enable_atlas 1}

%define module	numpy

# disable this for bootstrapping nose and sphinx
%define enable_tests 0
%define enable_doc 0

Summary:	A fast multidimensional array facility for Python
Name:		python-%{module}
Epoch:		1
Version:	1.7.1
Release:	6
License:	BSD
Group:		Development/Python
Url: 		http://numpy.scipy.org
Source0:	https://sourceforge.net/projects/numpy/files/NumPy/1.7.1/numpy-%{version}.tar.gz
Patch0:		numpy-1.5.1-link.patch

%rename	f2py
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
BuildRequires: python-devel
BuildRequires: python-cython
BuildRequires: python-setuptools
BuildRequires: pkgconfig(python3)
BuildRequires: python3-distribute

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
Requires:	%{name} = %{EVRD}

%description devel
This package contains tools and header files need to develop modules 
in C and Fortran that can interact with Numpy

%package -n python3-numpy
Summary:        A fast multidimensional array facility for Python3
Group:          Development/Python
License:        BSD

%description -n python3-numpy
Numpy is a general-purpose array-processing package designed to
efficiently manipulate large multi-dimensional arrays of arbitrary
records without sacrificing too much speed for small multi-dimensional
arrays. Numpy is built on the Numeric code base and adds features
introduced by numarray as well as an extended C-API and the ability to
create arrays of arbitrary type.

Numpy also provides facilities for basic linear algebra routines,
basic Fourier transforms, and random number generation.

%package -n python3-numpy-devel
Summary:        Numpy headers and development tools
Group:          Development/Python
Requires:       python3-numpy = %{epoch}:%{version}-%{release}

%description -n python3-numpy-devel
This package contains tools and header files need to develop modules.
in C and Fortran that can interact with Numpy.

%prep
%setup -qc
mv %{module}-%{version} python2
cp -a python2 python3
pushd python2
%patch0 -p1
# workaround for rhbz#849713
# http://mail.scipy.org/pipermail/numpy-discussion/2012-July/063530.html
rm numpy/distutils/command/__init__.py && touch numpy/distutils/command/__init__.py
popd

pushd python3
%patch0 -p1
rm numpy/distutils/command/__init__.py && touch numpy/distutils/command/__init__.py
popd

%build
pushd python3
CFLAGS="%{optflags} -fPIC -O3" PYTHONDONTWRITEBYTECODE= python3 setup.py config_fc --fcompiler=gnu95 build
#env ATLAS=%{_libdir} FFTW=%{_libdir} BLAS=%{_libdir} \
#    LAPACK=%{_libdir} CFLAGS="%{optflags} -fPIC -O3" \
#    %{__python3} setup.py build
popd

pushd python2
CFLAGS="%{optflags} -fPIC -O3" PYTHONDONTWRITEBYTECODE= python setup.py config_fc --fcompiler=gnu95 build
#env ATLAS=%{_libdir} FFTW=%{_libdir} BLAS=%{_libdir} \
#    LAPACK=%{_libdir} CFLAGS="%{optflags} -fPIC -O3" \
#    python setup.py build

%if %enable_doc
pushd doc
export PYTHONPATH=`dir -d ../build/lib.linux*`
%make html
popd
%endif

popd


%install
# first install python3 so the binaries are overwritten by the python2 ones
pushd python3
#%{__python} setup.py install -O1 --skip-build --root %{buildroot}
# skip-build currently broken, this works around it for now
#env ATLAS=%{_libdir} FFTW=%{_libdir} BLAS=%{_libdir} \
#    LAPACK=%{_libdir} CFLAGS="%{optflags} -fPIC -O3" \
#    python3 setup.py install --root %{buildroot}
CFLAGS="%{optflags} -fPIC -O3" PYTHONDONTWRITEBYTECODE= python3 setup.py install --root=%{buildroot}

rm -rf docs-f2py ; mv %{buildroot}%{python3_sitearch}/%{module}/f2py/docs docs-f2py
mv -f %{buildroot}%{python3_sitearch}/%{module}/f2py/f2py.1 f2py.1
rm -rf doc ; mv -f %{buildroot}%{python3_sitearch}/%{module}/doc .

install -D -p -m 0644 f2py.1 %{buildroot}%{_mandir}/man1/f2py.1
rm -rf %{buildroot}%{python3_sitearch}/%{module}/__pycache__

# Drop shebang from non-executable scripts to make rpmlint happy
find %{buildroot}%{py3_platsitedir} -name "*py" -perm 644 -exec sed -i '/#!\/usr\/bin\/env python/d' {} \;

popd

pushd python2
# skip-build currently broken, this works around it for now
#env ATLAS=%{_libdir} FFTW=%{_libdir} BLAS=%{_libdir} \
#    LAPACK=%{_libdir} CFLAGS="%{optflags} -fPIC -O3" \
#    python setup.py install --root %{buildroot}
CFLAGS="%{optflags} -fPIC -O3" PYTHONDONTWRITEBYTECODE= python setup.py install --root=%{buildroot}

rm -rf docs-f2py; mv %{buildroot}%{py_platsitedir}/%{module}/f2py/docs docs-f2py
mv -f %{buildroot}%{py_platsitedir}/%{module}/f2py/f2py.1 f2py.1
install -D -p -m 0644 f2py.1 %{buildroot}%{_mandir}/man1/f2py.1

rm -rf %{buildroot}%{py_platsitedir}/%{module}/tools/

# Remove doc files that should be in %doc:
rm -f %{buildroot}%{py_platsitedir}/%{module}/COMPATIBILITY
rm -f %{buildroot}%{py_platsitedir}/%{module}/*.txt
rm -f %{buildroot}%{py_platsitedir}/%{module}/site.cfg.example

# Drop shebang from non-executable scripts to make rpmlint happy
find %{buildroot}%{py_platsitedir} -name "*py" -perm 644 -exec sed -i '/#!\/usr\/bin\/env python/d' {} \;
popd

%check
%if %enable_tests
# Don't run tests from within main directory to avoid importing the uninstalled numpy stuff:
pushd doc &> /dev/null
PYTHONPATH="%{buildroot}%{py_platsitedir}" %{__python} -c "import pkg_resources, numpy; numpy.test()"
popd &> /dev/null

pushd doc &> /dev/null
PYTHONPATH="%{buildroot}%{python3_sitearch}" %{__python3} -c "import pkg_resources, numpy ; numpy.test()"
popd &> /dev/null
%endif

%files 
%doc python2/LICENSE.txt python2/README.txt python2/THANKS.txt python2/DEV_README.txt python2/COMPATIBILITY python2/site.cfg.example 
%if %enable_doc
%doc python2/doc/build/html
%endif
%dir %{py_platsitedir}/%{module}
%{py_platsitedir}/%{module}/*.py*
%{py_platsitedir}/%{module}/core/ 
%{py_platsitedir}/%{module}/compat/
%{py_platsitedir}/%{module}/doc/
%exclude %{py_platsitedir}/%{module}/core/include/
%exclude %{py_platsitedir}/%{module}/core/lib/*.a
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
%{_bindir}/f2py
%{_mandir}/man1/f2py.*
%{py_platsitedir}/%{module}/core/include/
%{py_platsitedir}/%{module}/core/lib/*.a
%{py_platsitedir}/%{module}/numarray/include/
%{py_platsitedir}/%{module}/distutils/
%{py_platsitedir}/%{module}/f2py/
%{py_platsitedir}/%{module}/random/randomkit.h

%files -n python3-numpy
%doc python3/LICENSE.txt python3/README.txt python3/THANKS.txt python3/DEV_README.txt python3/COMPATIBILITY python3/site.cfg.example
%dir %{py3_platsitedir}/%{module}
%{py3_platsitedir}/%{module}/*.py*
%{py3_platsitedir}/%{module}/core
%exclude %{py3_platsitedir}/%{module}/core/include/
%exclude %{py3_platsitedir}/%{module}/core/lib/*.a
%{py3_platsitedir}/%{module}/fft
%{py3_platsitedir}/%{module}/lib
%{py3_platsitedir}/%{module}/linalg
%{py3_platsitedir}/%{module}/ma
%{py3_platsitedir}/%{module}/numarray
%exclude %{py3_platsitedir}/%{module}/numarray/include/
%{py3_platsitedir}/%{module}/oldnumeric
%{py3_platsitedir}/%{module}/random
%exclude %{py3_platsitedir}/%{module}/random/randomkit.h
%{py3_platsitedir}/%{module}/testing
%{py3_platsitedir}/%{module}/tests
%{py3_platsitedir}/%{module}/compat
%{py3_platsitedir}/%{module}/matrixlib
%{py3_platsitedir}/%{module}/polynomial
%{py3_platsitedir}/%{module}-*.egg-info

%files -n python3-numpy-devel
%{_bindir}/f2py3
%{py3_platsitedir}/%{module}/f2py
%{py3_platsitedir}/%{module}/core/include/
%{py3_platsitedir}/%{module}/core/lib/*.a
%{py3_platsitedir}/%{module}/numarray/include/
%{py3_platsitedir}/%{module}/distutils/
%{py3_platsitedir}/%{module}/random/randomkit.h
%{py3_platsitedir}/%{module}/lib/*.a
