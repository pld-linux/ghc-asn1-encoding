#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	asn1-encoding
Summary:	ASN1 data reader and writer in RAW, BER and DER forms
Summary(pl.UTF-8):	Biblioteka odczytu i zapisu danych ASN1 w postaciach RAW, BER i DER
Name:		ghc-%{pkgname}
Version:	0.9.6
Release:	2
License:	BSD
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/asn1-encoding
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	98bc3d5b717eb6b5f47c2d676c9eaaf4
URL:		http://hackage.haskell.org/package/asn1-encoding
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-asn1-types >= 0.3.0
BuildRequires:	ghc-asn1-types < 0.4
BuildRequires:	ghc-base >= 3
BuildRequires:	ghc-base < 5
BuildRequires:	ghc-bytestring
BuildRequires:	ghc-hourglass >= 0.2.6
%if %{with prof}
BuildRequires:	ghc-prof
BuildRequires:	ghc-asn1-types-prof >= 0.3.0
BuildRequires:	ghc-base-prof >= 3
BuildRequires:	ghc-bytestring-prof
BuildRequires:	ghc-hourglass-prof >= 0.2.6
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
%requires_eq	ghc
Requires(post,postun):	/usr/bin/ghc-pkg
Requires:	ghc-base >= 3
Requires:	ghc-bytestring
Requires:	ghc-asn1-types >= 0.3.0
Requires:	ghc-hourglass >= 0.2.6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
ASN1 data reader and writer in raw form with supports for high level
forms of ASN1 (BER, and DER).

%description -l pl.UTF-8
Biblioteka odczytu i zapisu danych ASN1 w postaci surowej z obsługują
formatów ASN1 wyższego poziomu (BER i DER).

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ghc-asn1-types-prof >= 0.3.0
Requires:	ghc-base-prof >= 3
Requires:	ghc-bytestring-prof
Requires:	ghc-hourglass-prof >= 0.2.6

%description prof
Profiling %{pkgname} library for GHC. Should be installed when GHC's
profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.hs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.hs build

runhaskell Setup.hs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.hs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.hs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc %{name}-%{version}-doc/*
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%attr(755,root,root) %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.so
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.a
%exclude %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*_p.a

%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/ASN1
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/ASN1/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/ASN1/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/ASN1/BinaryEncoding
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/ASN1/BinaryEncoding/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/ASN1/BinaryEncoding/*.dyn_hi

%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/ASN1/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/ASN1/BinaryEncoding/*.p_hi
%endif
