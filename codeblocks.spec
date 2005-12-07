#
# TODO:
#		- set in settings->editor:end-of-line mode to `LF' as default
#
Summary:	An open source, cross platform, free C++ IDE
Summary(pl):	Wieloplatformowe, darmowe IDE do C++ o otwartych ¼ród³ach
Name:		codeblocks
Version:	1.0
%define		_rc	rc2
Release:	0.%{_rc}.0.3
License:	GPL
Group:		Development/Languages
Source0:	http://dl.sourceforge.net/codeblocks/%{name}-%{version}%{_rc}.tgz
# Source0-md5:	425c700feb77d22b1b85b1061d2504d9
Patch0:		%{name}-ac.patch
Patch1:		%{name}-fhs.patch
URL:		http://www.codeblocks.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	dos2unix
BuildRequires:	libtool
BuildRequires:	wxGTK2-devel >= 2.6.0
BuildRequires:	zip
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define	_pluginsdir %{_libdir}/%{name}/plugins

%description
Code::Blocks is a free C++ IDE built specifically to meet the most
demanding needs of its users. It was designed, right from the start,
to be extensible and configurable. Built around a plugin framework,
Code::Blocks can be extended with plugin DLLs. It includes a plugin
wizard so you can compile your own plugins!

Highlights:
 - Open Source! GPL 2, no hidden costs
 - Cross-platform; runs on Linux or Windows (uses wxWidgets)
 - Made in GNU C++; no interpreted languages or proprietary libs
   needed
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

%description -l pl
Code::Blocks to darmowe IDE dla C++ tworzone specjalnie w celu
zaspokojenia najwiêkszych potrzeb swoich u¿ytkowników. Zosta³o
zaprojektowane od pocz±tku aby by³o rozszerzalne i konfigurowalne.
Code::Blocks, jako zbudowane w oparciu o szkielet wtyczek, mo¿na
rozszerzaæ. Zawiera czarodzieja dla wtyczek, wiêc mo¿na kompilowaæ
w³asne.

G³ówne cechy:
 - otwarte ¼ród³a na licencji GPL 2, bez ukrytych kosztów
 - wieloplatformowo¶æ - dzia³a na Linuksie i Windows (przy u¿yciu
   wxWidgets)
 - stworzone w GNU C++, nie wymaga jêzyków interpretowanych ani
   w³asno¶ciowych bibliotek
 - rozszerzalne poprzez wtyczki

Cechy zwi±zane z kompilatorami:
 - obs³uga wielu kompilatorów: GCC (MingW / Linux), MSVC++, Digital
   Mars, Borland C++ 5.5, Open Watcom
 - kompiluje bezpo¶rednio lub z u¿yciem plików Makefile
 - predefiniowane szablony projektów
 - obs³uga w³asnych szablonów
 - u¿ywa formatu XML dla plików projektów
 - projekty z wieloma celami
 - obs³uga przestrzeni zadañ (workspace)
 - import projektów i przestrzeni zadañ MSVC (uwaga: kdo w asemblerze
   i zale¿no¶ci miêdzy projektami nie s± jeszcze obs³ugiwane)
 - import projektów Dev-C++
 - integracja z GDB do odpluskwiania

Cechy interfejsu:
 - pod¶wietlanie sk³adni - konfigurowalne i rozszerzalne
 - zwijanie kodu w plikach C++ i XML
 - interfejs z zak³adkami
 - wtyczka dope³niania kodu
 - przegl±darka klas
 - inteligentne wciêcia
 - prze³±czanie jednym klawiszem miêdzy plikami .h i .c/.cpp
 - lista otwartych plików do szybkiego prze³±czania miêdzy nimi
   (opcja)
 - zewnêtrzne, konfigurowalne "narzêdzia"
 - zarz±dzanie list± rzeczy do zrobienia ("To-do") przez ró¿nych
   u¿ytkowników

%prep
%setup -q -n %{name}-%{version}%{_rc}
%patch0 -p1
%patch1 -p1
find . -type f -and -not -name "*.cpp" -and -not -name "*.h" -and -not -name "*.png" -and -not -name "*.bmp" -and -not -name "*.c" -and -not -name "*.cxx" -and -not -name "*.ico" | sed "s/.*/\"\\0\"/" | xargs dos2unix
chmod a+x acinclude.m4 src/update
find . -name "Makefile.am" -exec %{__sed} -i "s@libdir = \$(pkgdatadir)/plugins@libdir = %{_pluginsdir}@" '{}' ';'

%build
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

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS BUGS COMPILERS README TODO ChangeLog
%attr(755,root,root) %{_bindir}/codeblocks
%attr(755,root,root) %{_bindir}/console_runner
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*
%{_desktopdir}/*.desktop
%{_pixmapsdir}/*.png
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*.zip
%{_datadir}/%{name}/*.txt
%{_datadir}/%{name}/icons
%{_datadir}/%{name}/images
%{_datadir}/%{name}/lexers
%{_datadir}/%{name}/templates
%dir %{_pluginsdir}
%attr(755,root,root) %{_pluginsdir}/*.so
%{_pkgconfigdir}/codeblocks.pc
