#
# Conditional build:
%bcond_without	tests		# do not perform "make test"
#
%define		pdir	Starlink
%define		pnam	AST
Summary:	Starlink::AST - Interface to the Starlink AST library
Name:		perl-Starlink-AST
Version:	1.02
Release:	13
License:	open_source
Group:		Development/Languages/Perl
Source0:	http://www.cpan.org/modules/by-authors/id/T/TJ/TJENNESS/Starlink-AST-1.02.tar.gz
# Source0-md5:	a5b044630445c2632710107040b70e5a
URL:		http://search.cpan.org/dist/Starlink-AST/
BuildRequires:	perl-ExtUtils-CBuilder
BuildRequires:	perl-Module-Build
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	rpm-perlprov >= 4.1-13
%if %{with tests}
BuildRequires:	perl-Astro-FITS-CFITSIO
BuildRequires:	perl-Test-Number-Delta
BuildRequires:	perl-Test-Deep
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		Werror_cflags	%{nil}

%description
Starlink::AST provides a perl wrapper to the Starlink AST library.
The Starlink AST library provides facilities for transforming
coordinates from one system to another in an object oriented manner.
Multiple coordinate frames can be associated with a data set and it is
also possible to generate automatic mappings between frames.

Coordinate frame objects can be imported from FITS headers and from
NDF files.

%prep
%setup -q -n %{pdir}-%{pnam}-%{version}
%{__mv} t/plot00_pgplot.t t/plot00_pgplot.t-requires-X
%{__mv} t/plot00_tk.t t/plot00_tk.t-requires-X

%build
%{__perl} Build.PL \
	config="optimize=%{rpmcflags}" \
	destdir=$RPM_BUILD_ROOT \
	installdirs=vendor
./Build

%{?with_tests:./Build test}

%install
rm -rf $RPM_BUILD_ROOT

./Build install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog README
%dir %{perl_vendorarch}/Starlink
%{perl_vendorarch}/Starlink/*.pm
%dir %{perl_vendorarch}/Starlink/AST
%{perl_vendorarch}/Starlink/AST/*.pm
%dir %{perl_vendorarch}/auto/Starlink
%dir %{perl_vendorarch}/auto/Starlink/AST
%attr(755,root,root) %{perl_vendorarch}/auto/Starlink/AST/*.so
%{_mandir}/man3/*
