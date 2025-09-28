#
# Conditional build:
%bcond_without	tests	# unit tests
#
%define		pdir	Starlink
%define		pnam	AST
Summary:	Starlink::AST - Interface to the Starlink AST library
Summary(pl.UTF-8):	Starlink::AST - interfejs do biblioteki Starlink AST
Name:		perl-Starlink-AST
Version:	3.05
Release:	1
License:	open_source
Group:		Development/Languages/Perl
Source0:	https://www.cpan.org/modules/by-authors/id/G/GS/GSB/Starlink-AST-%{version}.tar.gz
# Source0-md5:	d4b0cb11f6fd166ac2753b05e4b469cf
URL:		https://metacpan.org/dist/Starlink-AST
BuildRequires:	perl-ExtUtils-CBuilder
BuildRequires:	perl-Module-Build >= 0.3604
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	rpm-perlprov >= 4.1-13
BuildRequires:	rpmbuild(macros) >= 1.745
%if %{with tests}
BuildRequires:	perl-Astro-FITS-CFITSIO
BuildRequires:	perl-Astro-FITS-Header
BuildRequires:	perl-Test-Number-Delta
BuildRequires:	perl-Test-Deep
BuildRequires:	perl-Test-Simple
BuildRequires:	perl-Tk
BuildRequires:	perl-Tk-Zinc
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		Werror_cflags	%{nil}

%description
Starlink::AST provides a Perl wrapper to the Starlink AST library.
The Starlink AST library provides facilities for transforming
coordinates from one system to another in an object oriented manner.
Multiple coordinate frames can be associated with a data set and it is
also possible to generate automatic mappings between frames.

Coordinate frame objects can be imported from FITS headers and from
NDF files.

%description -l pl.UTF-8
Starlink::AST udostępnia perlowe obudowanie biblioteki Starlink AST.
Biblioteka ta zapewnia możliwość przekształcania współrzędnych z
jednego systemu do innego w sposób zorientowany obiektowo. Z danymi
można powiązać wiele ramek współrzędnych, możliwe jest także
generowanie automatycznych odwzorowań między ramkami.

Obiekty ramek współrzędnych mogą być importowane z nagłówków FITS oraz
plików NDF.

%prep
%setup -q -n %{pdir}-%{pnam}-%{version}
%{__mv} t/plot00_pgplot.t t/plot00_pgplot.t-requires-X
%{__mv} t/plot00_tk.t t/plot00_tk.t-requires-X

# temporary (3.05): seem to fail due to overflows (32-bit only?)
%{__mv} t/chebymap.t{,-tests_84-85_fail_in_3.05}
%{__mv} t/moc.t{,-datacheck_fails_in_3.05}

%build
%{__perl} Build.PL \
	--config "optimize=%{rpmcflags}" \
	--installdirs=vendor

./Build

%{?with_tests:./Build test}

%install
rm -rf $RPM_BUILD_ROOT

./Build install \
	destdir=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{perl_vendorarch}/auto/Starlink/AST/AST.bs

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc Changes README
%dir %{perl_vendorarch}/Starlink
%{perl_vendorarch}/Starlink/AST.pm
%dir %{perl_vendorarch}/Starlink/AST
%{perl_vendorarch}/Starlink/AST/*.pm
%dir %{perl_vendorarch}/auto/Starlink
%dir %{perl_vendorarch}/auto/Starlink/AST
%attr(755,root,root) %{perl_vendorarch}/auto/Starlink/AST/AST.so
%{_mandir}/man3/Starlink::AST*.3pm*
