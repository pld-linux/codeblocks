
Summary:	An open source, cross platform, free C++ IDE
Summary(pl.UTF-8):	Wieloplatformowe, darmowe IDE do C++ o otwartych źródłach
Name:		codeblocks
Version:	10.05
Release:	2
License:	GPL v3
Group:		X11/Development/Tools
Source0:	http://download.berlios.de/codeblocks/%{name}-%{version}-src.tar.bz2
# Source0-md5:	ab077d562e98b0586f2f86c14cb773ba
Patch0:		%{name}-FHS-plugins.patch
Patch2:		%{name}-ac.patch
Patch3:		%{name}-pwd.patch
URL:		http://www.codeblocks.org/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	bzip2-devel
BuildRequires:	gtk+2-devel
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	sed >= 4.0
BuildRequires:	unixODBC-devel
BuildRequires:	wxGTK2-unicode-devel >= 2.8.0
BuildRequires:	zip
BuildRequires:	zlib-devel
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	gtk-update-icon-cache
Requires(post,postun):	shared-mime-info
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pluginsdir %{_libdir}/%{name}/plugins

%description
Code::Blocks is a free C++ IDE built specifically to meet the most
demanding needs of its users. It was designed, right from the start,
to be extensible and configurable. Built around a plugin framework,
Code::Blocks can be extended with plugin DLLs. It includes a plugin
wizard so you can compile your own plugins!

Highlights:
 - Open Source! GPL 3, no hidden costs
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
 - otwarte źródła na licencji GPL 3, bez ukrytych kosztów
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
Summary(pl.UTF-8):	Pliki nagłówkowe Code::Blocks
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package provides development files for Code::Blocks. Install this
package only if you plan to write plugins for Code::Blocks.

%description devel -l pl.UTF-8
Ten pakiet dostarcza plików nagłówkowych Code::Blocks. Należy
instalować ten pakiet tylko w celu pisania wtyczek do Code::Blocks.

%prep
%setup -q -n %{name}-%{version}-release

%patch0 -p1
%patch2 -p1
%patch3 -p1

#hardcode libdir, continue of patch0
sed -i 's|@libdir@|%{_libdir}|' src/sdk/configmanager.cpp

# fix version inside the configure script
sed -i 's/1\.0svn/%{version}/g' revision.m4

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--with-wx-config=wx-gtk2-unicode-config \
	--with-contrib-plugins=all

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	mimeicondir=%{_iconsdir}/hicolor/48x48/mimetypes

rm -f $RPM_BUILD_ROOT%{_pluginsdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%update_icon_cache hicolor
%update_desktop_database_post
%update_mime_database

%postun
/sbin/ldconfig
%update_icon_cache hicolor
%update_desktop_database_postun
%update_mime_database

%files
%defattr(644,root,root,755)
%doc AUTHORS BUGS COMPILERS README TODO ChangeLog
%attr(755,root,root) %{_bindir}/cb_share_config
%attr(755,root,root) %{_bindir}/codeblocks
%attr(755,root,root) %{_bindir}/codesnippets
%attr(755,root,root) %{_bindir}/cb_console_runner
%attr(755,root,root) %{_libdir}/libwxsmithlib.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libwxsmithlib.so.0
%attr(755,root,root) %{_libdir}/libcodeblocks.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcodeblocks.so.0
%{_desktopdir}/codeblocks.desktop
%{_pixmapsdir}/*.png
%{_iconsdir}/hicolor/48x48/mimetypes/*.png
%{_datadir}/mime/packages/codeblocks.xml
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/scripts
%{_datadir}/%{name}/scripts/*
%{_datadir}/%{name}/*.zip
%{_datadir}/%{name}/*.txt
%{_datadir}/%{name}/icons
%{_datadir}/%{name}/images
%{_datadir}/%{name}/lexers
%{_datadir}/%{name}/lib_finder
%{_datadir}/%{name}/templates
%dir %{_libdir}/%{name}
%dir %{_libdir}/wxSmithContribItems
%dir %{_pluginsdir}
%attr(755,root,root) %{_pluginsdir}/*.so
%attr(755,root,root) %{_libdir}/wxSmithContribItems/*.so.*
%{_mandir}/man1/*.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcodeblocks.so
%attr(755,root,root) %{_libdir}/libwxsmithlib.so
%attr(755,root,root) %{_libdir}/wxSmithContribItems/*.so
%{_libdir}/libcodeblocks.la
%{_libdir}/libwxsmithlib.la
%{_libdir}/wxSmithContribItems/*.la
%{_pkgconfigdir}/codeblocks.pc
%{_pkgconfigdir}/wxsmith*.pc
%{_includedir}/codeblocks
%{_includedir}/wxSmithContribItems
%{_includedir}/wxsmith
