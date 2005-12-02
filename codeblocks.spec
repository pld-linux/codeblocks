Summary:	An open source, cross platform, free C++ IDE
Name:		codeblocks
Version:	1.0
%define		_rc	rc2
Release:	0.%{_rc}.0.1
License:	GPL
Group:		Development/Languages
Source0:	http://dl.sourceforge.net/codeblocks/%{name}-%{version}%{_rc}.tgz
# Source0-md5:	0
URL:		http://www.codeblocks.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	dos2unix
BuildRequires:	libtool
BuildRequires:	wxGTK2-devel
BuildRequires:	wxWindows-devel
BuildRequires:	zip
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Code::Blocks is a free C++ IDE built specifically to meet the most
demanding needs of its users. It was designed, right from the start,
to be extensible and configurable. Built around a plugin framework,
Code::Blocks can be extended with plugin DLLs. It includes a plugin
wizard so you can compile your own plugins!

Features:

Highlights:

     - Open Source! GPL2, no hidden costs.
     - Cross-platform. Runs on Linux or Windows (uses wxWidgets).
     - Made in GNU C++. No interpreted languages or proprietary libs
       needed.
     - Comes in two presentations: Standalone, and MinGW bundle
     - Devpack support (optional)
     - Extensible thru plugins (SDK available in the downloads section)

Compiler-related features:

     - Multiple compiler support:
       - GCC (MingW / Linux GCC)
       - MSVC++
       - Digital Mars
       - Borland C++ 5.5
       - Open Watcom
     - Compiles directly or with makefiles
     - Predefined project templates
     - Custom template support
     - Uses XML format for project files.
     - Multi-target projects
     - Workspaces support
     - Imports MSVC projects and workspaces (NOTE: assembly code and
       inter-project dependencies not supported yet)
     - Imports Dev-C++ projects
     - Integrates with GDB for debugging

Interface Features:

     - Syntax highlighting, customizable and extensible
     - Code folding for C++ and XML files.
     - Tabbed interface
     - Code completion plugin
     - Class Browser
     - Smart indent
     - One-key swap between .h and .c/.cpp files
     - Open files list for quick switching between files (optional)
     - External customizable "Tools"
     - To-do list management with different users

%prep
%setup -q -n %{name}-%{version}%{_rc}
find . -type f -and -not -name "*.cpp" -and -not -name "*.h" -and -not -name "*.png" -and -not -name "*.bmp" -and -not -name "*.c" -and -not -name "*.cxx" -and -not -name "*.ico" | sed "s/.*/\"\\0\"/" | xargs dos2unix
chmod a+x acinclude.m4 src/update

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
#doc README COPYING AUTHORS BUGS COMPILERS TODO NEWS ChangeLog
%attr(755,root,root) %{_bindir}/codeblocks
%attr(755,root,root) %{_bindir}/console_runner
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*
#{_datadir}/application-registry/codeblocks.applications
#{_datadir}/applications/codeblocks.desktop
#{_datadir}/icons/gnome/48x48/mimetypes/gnome-mime-application-x-codeblocks.png
#{_datadir}/mime-info/*
#{_datadir}/mime/packages/codeblocks.xml
#{_datadir}/pixmaps/codeblocks.png
#define pkgdata %{_datadir}/%{name}
#{pkgdata}/*
