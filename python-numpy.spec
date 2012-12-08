%define enable_atlas 0
%{?_with_atlas: %global enable_atlas 1}

%define module	numpy

# disable this for bootstrapping nose and sphinx
%define enable_tests 0
%define enable_doc 0

Summary:	A fast multidimensional array facility for Python
Name:		python-%{module}
Version:	1.6.2
Epoch:		1
Release:	4
License:	BSD
Group:		Development/Python
Url: 		http://numpy.scipy.org
Source0:	http://downloads.sourceforge.net/numpy/%{module}-%{version}.tar.gz
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
Requires:	%{name} = %{EVRD}

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
CFLAGS="%{optflags} -fPIC -O3" PYTHONDONTWRITEBYTECODE= %{__python} setup.py install --root=%{buildroot} 

rm -rf docs-f2py; %__mv %{buildroot}%{py_platsitedir}/%{module}/f2py/docs docs-f2py
mv -f %{buildroot}%{py_platsitedir}/%{module}/f2py/f2py.1 f2py.1
install -D -p -m 0644 f2py.1 %{buildroot}%{_mandir}/man1/f2py.1

rm -rf %{buildroot}%{py_platsitedir}/%{module}/tools/

# Remove doc files that should be in %doc:
rm -f %{buildroot}%{py_platsitedir}/%{module}/COMPATIBILITY
rm -f %{buildroot}%{py_platsitedir}/%{module}/*.txt
rm -f %{buildroot}%{py_platsitedir}/%{module}/site.cfg.example

# Drop shebang from non-executable scripts to make rpmlint happy
find %{buildroot}%{py_platsitedir} -name "*py" -perm 644 -exec sed -i '/#!\/usr\/bin\/env python/d' {} \;

%check
%if %enable_tests
# Don't run tests from within main directory to avoid importing the uninstalled numpy stuff:
pushd doc &> /dev/null
PYTHONPATH="%{buildroot}%{py_platsitedir}" %{__python} -c "import numpy; numpy.test()"
popd &> /dev/null
%endif

%files 
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
%{_bindir}/f2py
%{_mandir}/man1/f2py.*
%{py_platsitedir}/%{module}/core/include/
%{py_platsitedir}/%{module}/numarray/include/
%{py_platsitedir}/%{module}/distutils/
%{py_platsitedir}/%{module}/f2py/
%{py_platsitedir}/%{module}/random/randomkit.h


%changelog
* Fri Jun 08 2012 Lev Givon <lev@mandriva.org> 1:1.6.2-2
+ Revision: 803420
- Tweak to build on 2010.1.

* Sun May 20 2012 Lev Givon <lev@mandriva.org> 1:1.6.2-1
+ Revision: 799735
- Update to 1.6.2.

* Tue Nov 08 2011 Matthew Dawkins <mattydaw@mandriva.org> 1:1.6.1-2
+ Revision: 728879
- rebuild for new gfortran
  cleaned up spec

* Thu Jul 21 2011 Lev Givon <lev@mandriva.org> 1:1.6.1-1
+ Revision: 690874
- Update to 1.6.1.

* Sun May 15 2011 Lev Givon <lev@mandriva.org> 1:1.6.0-1
+ Revision: 674859
- Update to 1.6.0.

* Thu May 05 2011 Oden Eriksson <oeriksson@mandriva.com> 1:1.5.1-2
+ Revision: 668018
- mass rebuild

  + Pascal Terjan <pterjan@mandriva.org>
    - Fix extensions linkage

* Thu Nov 18 2010 Lev Givon <lev@mandriva.org> 1:1.5.1-1mdv2011.0
+ Revision: 598753
- Update to 1.5.1.

* Sat Oct 30 2010 Götz Waschk <waschk@mandriva.org> 1:1.5.0-5mdv2011.0
+ Revision: 590554
- rebuild for new python

* Sat Oct 30 2010 Olivier Thauvin <nanardon@mandriva.org> 1:1.5.0-4mdv2011.0
+ Revision: 590528
- rebuild

  + Michael Scherer <misc@mandriva.org>
    - add a switch to disable doc due to boostraping problem
    - disable test, so we can recompile for python 2.7
    - rebuild for python 2.7

* Thu Sep 16 2010 Lev Givon <lev@mandriva.org> 1:1.5.0-2mdv2011.0
+ Revision: 578796
- Patch to enable doc build (numpy bug #1596).

* Tue Aug 31 2010 Lev Givon <lev@mandriva.org> 1:1.5.0-1mdv2011.0
+ Revision: 574837
- Update to 1.5.0.

  + Per Øyvind Karlsen <peroyvind@mandriva.org>
    - don't manually compress package in %%install, it breaks short-circuitting and
      is also automatically done by helpers anyways..

* Tue Apr 27 2010 Christophe Fergeau <cfergeau@mandriva.com> 1:1.4.1-2mdv2010.1
+ Revision: 539595
- rebuild so that shared libraries are properly stripped again

* Thu Apr 22 2010 Lev Givon <lev@mandriva.org> 1:1.4.1-1mdv2010.1
+ Revision: 537982
- Update to 1.4.1.

* Thu Jan 28 2010 Frederik Himpe <fhimpe@mandriva.org> 1:1.4.0-1mdv2010.1
+ Revision: 497771
- Disable atlas build: it is not in main

  + Guillaume Rousse <guillomovitch@mandriva.org>
    - new version

  + Lev Givon <lev@mandriva.org>
    - Clean up spec file.
      Build against atlas instead of netlib blas/lapack.

* Thu Sep 10 2009 Lev Givon <lev@mandriva.org> 1:1.3.0-4mdv2010.0
+ Revision: 436957
- Remove python-devel suggested install because it induces
  installation of lots of other devel stuff.

* Tue Sep 08 2009 Lev Givon <lev@mandriva.org> 1:1.3.0-3mdv2010.0
+ Revision: 433755
- Add python-devel as a suggested install because it is required to run
  some tests.

* Wed Sep 02 2009 Lev Givon <lev@mandriva.org> 1:1.3.0-2mdv2010.0
+ Revision: 424322
- Add python-nose as an optional install dependency.

* Fri Jun 19 2009 Per Øyvind Karlsen <peroyvind@mandriva.org> 1:1.3.0-1mdv2010.0
+ Revision: 387249
- boost gcc optimization level to -O3 as this proves beneficial for performance

* Sun Apr 05 2009 Lev Givon <lev@mandriva.org> 1:1.3.0-1mdv2009.1
+ Revision: 364159
- Update to 1.3.0.

* Thu Mar 19 2009 Paulo Andrade <pcpa@mandriva.com.br> 1.3.0b1-1mdv2009.1
+ Revision: 358059
- Update to latest upstream release.

* Thu Dec 25 2008 Adam Williamson <awilliamson@mandriva.org> 1.2.1-3mdv2009.1
+ Revision: 318550
- rebuild for new python

* Tue Nov 25 2008 Lev Givon <lev@mandriva.org> 1.2.1-2mdv2009.1
+ Revision: 306745
- Rebuild against lapack 3.2.

* Thu Oct 30 2008 Lev Givon <lev@mandriva.org> 1.2.1-1mdv2009.1
+ Revision: 298753
- Update to 1.2.1.

* Sun Oct 26 2008 Lev Givon <lev@mandriva.org> 1.2.0-1mdv2009.1
+ Revision: 297454
- Update to 1.2.0.

* Sun Aug 03 2008 Lev Givon <lev@mandriva.org> 1.1.1-1mdv2009.0
+ Revision: 262015
- Update to 1.1.1.

* Fri Jul 11 2008 Lev Givon <lev@mandriva.org> 1.1.0-2mdv2009.0
+ Revision: 233799
- Bump release to rebuild against reorganized blas/lapack libraries.

* Thu May 29 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 1.1.0-1mdv2009.0
+ Revision: 212881
- update to new version 1.1.0
- spec file clean

  + Thierry Vignaud <tv@mandriva.org>
    - fix summary-not-capitalized
    - kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Tue Nov 13 2007 Lev Givon <lev@mandriva.org> 1.0.4-1mdv2008.1
+ Revision: 108503
- Update to 1.0.4.

* Fri Nov 09 2007 Lev Givon <lev@mandriva.org> 1.0.3.1-2mdv2008.1
+ Revision: 106991
- Bump release to rebuild against lapack 3.1.1.

* Wed Aug 22 2007 Lev Givon <lev@mandriva.org> 1.0.3.1-1mdv2008.0
+ Revision: 69185
- Update to 1.0.3.1.

* Wed Jun 20 2007 Lev Givon <lev@mandriva.org> 1.0.3-1mdv2008.0
+ Revision: 41659
- Update to 1.0.3.

* Tue Apr 17 2007 Lev Givon <lev@mandriva.org> 1.0.2-1mdv2008.0
+ Revision: 13991
- Update to 1.0.2.


* Mon Jan 22 2007 Lev Givon <lev@mandriva.org> 1.0.1-2mdv2007.0
+ Revision: 111955
- Patch to search for X11 libs in lib64 (Bug 28348).

* Sat Dec 02 2006 Emmanuel Andry <eandry@mandriva.org> 1.0.1-1mdv2007.1
+ Revision: 90060
- new version 1.0.1

* Thu Oct 26 2006 Lev Givon <lev@mandriva.org> 1.0rc1-1mdv2007.1
+ Revision: 72558
- Import python-numpy

* Wed Sep 27 2006 Lev Givon <lev@mandriva.org> 1.0rc1-1mdk
- Update.

* Mon Jul 31 2006 Lev Givon <lev@mandriva.org> 1.0b1-1mdk
- Update.

* Tue May 23 2006 Lev Givon <lev@mandriva.org> 0.9.8-2mdk
- Put all .h files in devel package.

* Fri May 19 2006 Lev Givon <lev@mandriva.org> 0.9.8-1mdk
- Update.

* Tue Apr 25 2006 Lev Givon <lev@mandriva.org> 0.9.6-2mdk
- Fix build dependencies.

* Sun Mar 19 2006 Lev Givon <lev@mandriva.org> 0.9.6-1mdk
- Update.

* Fri Mar 17 2006 Lev Givon <lev@mandriva.org> 0.9.5-4mdk
- Make package obsolete old f2py.

* Thu Mar 16 2006 Lev Givon <lev@mandriva.org> 0.9.5-3mdk
- Fix multiarch problem.

* Thu Mar 02 2006 Lev Givon <lev@mandriva.org> 0.9.5-2mdk
- Define devel package.

* Thu Feb 23 2006 Lev Givon <lev@mandriva.org> 0.9.5-1mdk
- Update.

* Tue Jan 31 2006 Lev Givon <lev@mandriva.org> 0.9.4-1mdk
- Update.

* Fri Jan 20 2006 Lev Givon <lev@mandriva.org> 0.9.2-1mdk
- Initial Mandriva package.

