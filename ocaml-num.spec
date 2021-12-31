#
# Conditional build:
%bcond_without	ocaml_opt	# skip building native optimized binaries (bytecode is always built)

# not yet available on x32 (ocaml 4.02.1), update when upstream will support it
%ifnarch %{ix86} %{x8664} %{arm} aarch64 ppc sparc sparcv9
%undefine	with_ocaml_opt
%endif

%if %{without ocaml_opt}
%define		_enable_debug_packages	0
%endif

%define		module	num
Summary:	Legacy Num library for arbitrary-precision integer and rational arithmetic
Summary(pl.UTF-8):	Stara biblioteka Num do arytmetyki dowolnej precyzji na liczbach całkowitych i wymiernych
Name:		ocaml-num
Version:	1.4
Release:	2
License:	LGPL v2+ with exceptions
Group:		Libraries
Source0:	https://github.com/ocaml/num/archive/v%{version}/%{module}-%{version}.tar.gz
# Source0-md5:	cda2b727e116a0b6a9c03902cc4b2415
URL:		https://github.com/ocaml/num
BuildRequires:	ocaml >= 1:4.0
BuildRequires:	ocaml-findlib-devel
%requires_eq	ocaml-runtime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This library implements arbitrary-precision arithmetic on big integers
and on rationals.

This is a legacy library. It used to be part of the core OCaml
distribution (in otherlibs/num) but is now distributed separately. New
applications that need arbitrary-precision arithmetic should use the
Zarith library (https://github.com/ocaml/Zarith) instead of the Num
library, and older applications that already use Num are encouraged to
switch to Zarith. Zarith delivers much better performance than Num and
has a nicer API.

%description -l pl.UTF-8
Ta biblioteka implementuje arytmetykę dowolnej precyzji na dużych
liczbach całkowitych i wymiernych.

To jest stara biblioteka. Była częścią podstawowej dystrybucji OCamla
(w otherlibs/num), ale obecnie jest rozprowadzana osobno. Nowe
aplikacje wymagające arytmetyki dowolnej precyzji powinny używać
biblioteki Zarith (https://github.com/ocaml/Zarith) zamiast Num, a w
starszych aplikacjach wykorzystujących bibliotekę Num zaleca się
przejść na Zarith. Zarith zapewnia lepszą wydajność i przyjemniejsze
API.

%package devel
Summary:	Legacy Num library for arbitrary-precision integer and rational arithmetic - development part
Summary(pl.UTF-8):	Stara biblioteka Num do arytmetyki dowolnej precyzji na liczbach całkowitych i wymiernych - część programistyczna
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains files needed to develop OCaml programs using Num
library.

%description devel -l pl.UTF-8
Pakiet ten zawiera pliki niezbędne do tworzenia programów w OCamlu
używających biblioteki Num.

%prep
%setup -q -n num-%{version}

%build
%{__make} all \
%if %{without ocaml_opt}
	BNG_ARCH=generic \
	ARCH=none
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
%if %{without ocaml_opt}
	BNG_ARCH=generic \
	ARCH=none \
%endif
	DESTDIR=$RPM_BUILD_ROOT \
	OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc Changelog README.md
%attr(755,root,root) %{_libdir}/ocaml/stublibs/*.so
%dir %{_libdir}/ocaml/%{module}
%{_libdir}/ocaml/%{module}/META
%dir %{_libdir}/ocaml/num-top
%{_libdir}/ocaml/num-top/META
%{_libdir}/ocaml/*.cma
%{_libdir}/ocaml/num-top/num_top.cma
%if %{with ocaml_opt}
%attr(755,root,root) %{_libdir}/ocaml/*.cmxs
%endif

%files devel
%defattr(644,root,root,755)
%{_libdir}/ocaml/*.cmi
%{_libdir}/ocaml/*.cmti
%{_libdir}/ocaml/*.mli
%{_libdir}/ocaml/libnums.a
%if %{with ocaml_opt}
%{_libdir}/ocaml/nums.a
%{_libdir}/ocaml/*.cmx
%{_libdir}/ocaml/*.cmxa
%endif
%{_libdir}/ocaml/num-top/*.cmi
