%define		_rc	rc2
%define		_snap	20060721
Summary:	An open source, cross platform, free C++ IDE
Summary(pl.UTF-8):   Wieloplatformowe, darmowe IDE do C++ o otwartych źródłach
Name:		codeblocks
Version:	1.0
#Release:	0.%{_rc}.0.5
Release:	0.%{_snap}
License:	GPL
Group:		Development/Languages
# Source0:    http://dl.sourceforge.net/codeblocks/%{name}-%{version}%{_rc}.tgz
Source0:	%{name}-%{_snap}.tar.gz
# Source0-md5:	1ec8c03eff46629cdb1cbc1516ffa78e
Source1:	%{name}.conf
Patch0:		%{name}-ac.patch
Patch1:		%{name}-fhs.patch
Patch2:		%{name}-pwd.patch
Patch3:		%{name}-gcc-4.1.patch
URL:		http://www.codeblocks.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	dos2unix
BuildRequires:	libtool
BuildRequires:	unixODBC-devel
BuildRequires:	wxGTK2-devel >= 2.6.0
BuildRequires:	zip
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pluginsdir %{_libdir}/%{name}/plugins

%description
Code::Blocks is a free C++ IDE built specifically to meet the most
demanding needs of its users. It was designed, right from the start,
to be extensible and configurable. Built around a plugin framework,
Code::Blocks can be extended with plugin DLLs. It includes a plugin
wizard so you can compile your own plugins!

Highlights:
 - Open Source! GPL 2, no hidden costs
 - Cross-platform; runs on Linux or Windows (uses wxWidgets)
 - Made in GNU C++; no interpreted languages or proprietary libs needed
 - Extensible thru plugins

Compiler-related features:
 - Multiple compiler support: GCC (MingW / Linux), MSVC++, Digital
   Mars, Borland C++ 5.5, Open Watcom
 - Compiles directly or with makefiles
 - Predefined project templates
 - Custom template support
 - Uses XML format for project files
 - Multi-target projects
 - Workspaces support
 - Imports MSVC projects and workspaces (NOTE: assembly code and
   inter-project dependencies not supported yet)
 - Imports Dev-C++ projects
 - Integrates with GDB for debugging

Interface Features:
 - Syntax highlighting, customizable and extensible
 - Code folding for C++ and XML files
 - Tabbed interface
 - Code completion plugin
 - Class Browser
 - Smart indent
 - One-key swap between .h and .c/.cpp files
 - Open files list for quick switching between files (optional)
 - External customizable "Tools"
 - To-do list management with different users

%description -l pl.UTF-8
Code::Blocks to darmowe IDE dla C++ tworzone specjalnie w celu
zaspokojenia największych potrzeb swoich użytkowników. Zostało
zaprojektowane od początku aby było rozszerzalne i konfigurowalne.
Code::Blocks, jako zbudowane w oparciu o szkielet wtyczek, można
rozszerzać. Zawiera czarodzieja dla wtyczek, więc można kompilować
własne.

Główne cechy:
 - otwarte źródła na licencji GPL 2, bez ukrytych kosztów
 - wieloplatformowość - działa na Linuksie i Windows (przy użyciu
   wxWidgets)
 - stworzone w GNU C++, nie wymaga języków interpretowanych ani
   własnościowych bibliotek
 - rozszerzalne poprzez wtyczki

Cechy związane z kompilatorami:
 - obsługa wielu kompilatorów: GCC (MingW / Linux), MSVC++, Digital
   Mars, Borland C++ 5.5, Open Watcom
 - kompiluje bezpośrednio lub z użyciem plików Makefile
 - predefiniowane szablony projektów
 - obsługa własnych szablonów
 - używa formatu XML dla plików projektów
 - projekty z wieloma celami
 - obsługa przestrzeni zadań (workspace)
 - import projektów i przestrzeni zadań MSVC (uwaga: kdo w asemblerze i
   zależności między projektami nie są jeszcze obsługiwane)
 - import projektów Dev-C++
 - integracja z GDB do odpluskwiania

Cechy interfejsu:
 - podświetlanie składni - konfigurowalne i rozszerzalne
 - zwijanie kodu w plikach C++ i XML
 - interfejs z zakładkami
 - wtyczka dopełniania kodu
 - przeglądarka klas
 - inteligentne wcięcia
 - przełączanie jednym klawiszem między plikami .h i .c/.cpp
 - lista otwartych plików do szybkiego przełączania między nimi (opcja)
 - zewnętrzne, konfigurowalne "narzędzia"
 - zarządzanie listą rzeczy do zrobienia ("To-do") przez różnych
   użytkowników

%package devel
Summary:	Development files for Code::Blocks
Summary(pl.UTF-8):   Pliki nagłówkowe Code::Blocks
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package provides development files for Code::Blocks. Install this
package only if you plan to write plugins for Code::Blocks.

%description devel -l pl.UTF-8
Ten pakiet dostarcza plików nagłówkowych Code::Blocks. Należy
instalować ten pakiet tylko w celu pisania wtyczek do Code::Blocks.

%prep
#%setup -q -n %{name}-%{version}%{_rc}
%setup -q -n %{name}-%{_snap}
find . -type f -and -not -name "*.cpp" -and -not -name "*.h" -and -not -name "*.png" -and -not -name "*.bmp" -and -not -name "*.c" -and -not -name "*.cxx" -and -not -name "*.ico" | sed "s/.*/\"\\0\"/" | xargs dos2unix
chmod a+x acinclude.m4 src/update
#%patch0 -p1
#%patch1 -p1
#%patch2 -p1
%patch3 -p0

%build
# Because of new bootstrap script, crating revision.m4
echo "m4_define([SVN_REVISION], trunk-r0)" > ./revision.m4

%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--with-wx-config=wx-gtk2-ansi-config
%{__make}
%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_sysconfdir}
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT
cp %{SOURCE1} "$RPM_BUILD_ROOT%{_sysconfdir}/Code::Blocks v1.0"

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS BUGS COMPILERS README TODO ChangeLog
%config(noreplace) %verify(not md5 mtime size) "%{_sysconfdir}/Code::Blocks v1.0"
%attr(755,root,root) %{_bindir}/codeblocks
%attr(755,root,root) %{_bindir}/cb_console_runner
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*
%{_desktopdir}/*.desktop
%{_pixmapsdir}/*.png
%{_iconsdir}/gnome/48x48/mimetypes/*.png
%{_datadir}/application-registry/codeblocks.applications
%{_datadir}/mime/packages/codeblocks.xml
%{_datadir}/mime-info/codeblocks*
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/scripts
%dir %{_datadir}/%{name}/plugins
%{_datadir}/%{name}/scripts
%{_datadir}/%{name}/*.zip
%{_datadir}/%{name}/*.txt
%{_datadir}/%{name}/icons
%{_datadir}/%{name}/images
%{_datadir}/%{name}/lexers
%{_datadir}/%{name}/templates
%{_datadir}/%{name}/plugins/*
#%dir %{_pluginsdir}
#%attr(755,root,root) %{_pluginsdir}/*.so
%{_pkgconfigdir}/codeblocks.pc
%{_mandir}/man1/*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/*.la
%{_includedir}/codeblocks
