# we ship the 1.4.2 docs for now
%define docversion 1.4.2

%define major	2.1.0
%define libname %mklibname %{name} %{major}
%define wrong	%mklibname %{name} 2.1
%define devname %mklibname %{name} -d

Summary:	A free speech synthesizer 
Name:		festival
Version:	2.1
Release:	7
License:	BSD
Group:		Sound
Url:		http://www.cstr.ed.ac.uk/projects/festival/
Source0:	http://festvox.org/packed/festival/%{version}/%{name}-%{version}-release.tar.gz
Source1:	http://festvox.org/packed/festival/%{docversion}/festdoc-%{docversion}.tar.bz2
Source2:	siteinit.scm
Source3:	sitevars.scm
Source4:	http://festvox.org/packed/festival/%{version}/speech_tools-%{version}-release.tar.gz
# Fix up various locations to be more FSSTND compliant
Patch0:		festival-1.4.1-fsstnd.patch
# Set defaults to American English instead of British English - the OALD
# dictionary (free for non-commercial use only) is needed for BE support
# Additionally, prefer the smaller nitech hts voices.
Patch1:		festival-2.1-nitech-american.patch

# Whack some buildroot references
Patch2:		festival_buildroot.patch
Patch3:		festival.gcc47.patch

# (fc) 1.2.96-4mdv Fix a coding error (RH bug #162137) (Fedora)
Patch5:		festival-1.96-speechtools-rateconvtrivialbug.patch
# (fc) 1.2.96-4mdv Link libs with libm, libtermcap, and libesd (RH bug #198190) (Fedora)
# (ahmad) 2.1-2.mga1 modify this patch so that we don't link against libesd,
# as esound is being phased out of the distro
Patch6:		festival-2.1-speechtools-linklibswithotherlibs.patch
# For some reason, CXX is set to gcc on everything but Mac OS Darwin,
# where it's set to g++. Yeah, well. We need it to be right too.
Patch7:		festival-1.96-speechtools-ohjeezcxxisnotgcc.patch
# (fc) 1.2.96-5mdv build speech_tools as shared libraries (Fedora)
Patch8:		festival-1.96-speechtools-shared-build.patch
# (fc) 1.2.96-5mdv Look for speech tools here, not back there (Fedora)
Patch10:	festival-1.96-findspeechtools.patch
# (fc) 1.96-5mdv  Build main library as shared, not just speech-tools (Fedora)
Patch11:	festival-1.96-main-shared-build.patch
# (fc) 1.2.96-5mdv improve soname (Fedora)
Patch12:	festival-2.1-bettersonamehack.patch
# (fc) 
Patch15:	festival-finnish.patch
# Look for siteinit and sitevars in /etc/festival
Patch16:	festival-1.96-etcsiteinit.patch
BuildRequires:	perl
BuildRequires:	speech_tools-devel
BuildRequires:	pkgconfig(ncurses)
Requires:	festival-voice

%description
Festival is a general multi-lingual speech synthesis system developed
at CSTR. It offers a full text to speech system with various APIs, as
well as an environment for development and research of speech synthesis
techniques. It is written in C++ with a Scheme-based command interpreter
for general control.

%package -n	%{libname}
Summary:	Shared libraries for festival text to speech
Group:		System/Libraries
Conflicts:	%{name} < 2.1-4
%rename		%{wrong}

%description -n	%{libname}
This package contains the libraries and includes files necessary for
applications that use %{name}.

%package -n	%{devname}
Summary:	Development libraries and headers for festival text to speech
Group:		Development/C++
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n	%{devname}
This package contains the libraries and includes files necessary to develop
applications using %{name}.
 
%prep
%setup -qn %{name} -a 1 -a 4
%patch0 -p1 -b .fsstnd
# no backup extension, directory is copied during package install
%patch1 -p1 
%patch2 -p1 -b .buildroot
%patch3 -p0 -b .gcc
%patch5 -p1 -b .rateconvtrivialbug
%patch6 -p1 -b .linklibswithotherlibs
%patch7 -p1 -b .cxx
%patch8 -p1 -b .shared
# no backup extension, directory is copied during package install
%patch10 -p1 
# no backup extension, directory is copied during package install
%patch11 -p1 
%patch12 -p1 -b .bettersoname
# no backup extension, directory is copied during package install
%patch15 -p1 
# no backup extension, directory is copied during package install
%patch16 -p1 

# zero length
rm festdoc-1.4.2/speech_tools/doc/index_html.jade
rm festdoc-1.4.2/speech_tools/doc/examples_gen/error_example_section.sgml
rm festdoc-1.4.2/speech_tools/doc/tex_stuff.jade

# (gb) lib64 fixes, don't bother with a patch for now
perl -pi -e '/^REQUIRED_LIBRARY_DIR/ and s,/usr/lib,%{_libdir},' config/project.mak

%build
# build speech tools (and libraries)
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$(pwd)/speech_tools/lib
cd speech_tools
  %configure2_5x
  # -fPIC 'cause we're building shared libraries and it doesn't hurt
  # -fno-strict-aliasing because of a couple of warnings about code
  #   problems; if $RPM_OPT_FLAGS contains -O2 or above, this puts
  #   it back. Once that problem is gone upstream, remove this for
  #   better optimization.
cd -

# build the main program
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$(pwd)/src/lib
# instead of doing this, maybe we should patch the make process
# so it looks in the right place explicitly:
export PATH=$(pwd)/bin:$PATH
%configure2_5x
make \
	CFLAGS="$RPM_OPT_FLAGS -fPIC" \
	CXXFLAGS="$RPM_OPT_FLAGS -fPIC" \
	PROJECT_INCLUDES="-I$PWD/src/include -I/usr/include/EST -I$PWD/speech_tools/include" \
	REQUIRED_LIBRARY_DIR_estools=%{_libdir} \
	REQUIRED_LIBRARY_DIR_estbase=%{_libdir} \
	REQUIRED_LIBRARY_DIR_eststring=%{_libdir}

%install
install -d %{buildroot}%{_datadir}/%{name}/{voices/english,dicts}

# bin
make INSTALLED_BIN=%{buildroot}%{_bindir} make_installed_bin_static
install -m 755 bin/text2wave %{buildroot}%{_bindir}
#install bin/festival_server* bin/text2wave %{buildroot}%{_bindir}
#install src/main/festival{,_client} %{buildroot}%{_bindir}
# this is just nifty. and it's small.
install -m 755 examples/saytime %{buildroot}%{_bindir}

# install the shared library
install -d %{buildroot}%{_libdir}
cp -a src/lib/libFestival.so* %{buildroot}%{_libdir}

# devel
mkdir -p %{buildroot}%{_includedir}/festival
install src/include/*.h %{buildroot}%{_includedir}/%{name}

# data
cp -r lib config examples %{buildroot}%{_datadir}/%{name}
find %{buildroot}%{_datadir}/%{name} -name Makefile -exec rm \{\} \;

# man pages
mkdir -p %{buildroot}%{_mandir}/man1
cp -a doc/*.1 %{buildroot}%{_mandir}/man1

# lib: the bulk of the program -- the scheme stuff and so on
pushd lib
  mkdir -p %{buildroot}%{_datadir}/festival/lib
  for f in *.scm festival.el *.ent *.gram *.dtd *.ngrambin speech.properties ; do
    install -m 644 $f %{buildroot}%{_datadir}/festival/lib/
  done
  mkdir -p %{buildroot}%{_datadir}/festival/lib/multisyn/
  install -m 644 multisyn/*.scm %{buildroot}%{_datadir}/festival/lib/multisyn/
popd 

mv -f %{buildroot}/%{_datadir}/%{name}/lib/etc/unknown_RedHatLinux/audsp %{buildroot}/%{_bindir}
rm -Rf %{buildroot}/%{_datadir}/%{name}/lib/etc/
rm -f %{buildroot}%{_datadir}/%{name}/lib/VCLocalRules

# the actual /etc. :)
mkdir -p %{buildroot}%{_sysconfdir}/festival
# use our version of this file
rm %{buildroot}%{_datadir}/festival/lib/siteinit.scm 
install -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/festival/siteinit.scm
install -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/festival/sitevars.scm

sed -i -e 's,/projects/festival/lib,%{_datadir}/%{name},g' %{buildroot}/%{_datadir}/%{name}/lib/lexicons.scm

%files
%doc ACKNOWLEDGMENTS COPYING NEWS README*
%doc festdoc-1.4.2/festival/html/*html
%doc festdoc-1.4.2/festival/info
%doc festdoc-1.4.2/festival/festival.ps
%{_bindir}/audsp
%{_bindir}/festival
%{_bindir}/festival_client
%{_bindir}/festival_server
%{_bindir}/festival_server_control
%{_bindir}/text2wave
%{_bindir}/saytime
%dir %{_datadir}/festival
%dir %{_datadir}/festival/lib
%{_datadir}/festival/lib/*.scm
%{_datadir}/festival/lib/festival.el
%{_datadir}/festival/lib/*.ent
%{_datadir}/festival/lib/*.gram
%{_datadir}/festival/lib/*.dtd
%{_datadir}/festival/lib/*.ngrambin
%{_datadir}/festival/lib/speech.properties
%{_datadir}/festival/dicts
%{_datadir}/festival/voices
%dir %{_datadir}/festival/lib/multisyn
%{_datadir}/festival/lib/multisyn/*.scm
%dir %{_datadir}/festival/examples
%{_datadir}/festival/examples/*
%{_mandir}/man1/*
%config(noreplace) %{_sysconfdir}/festival

%files -n %{libname}
%{_libdir}/libFestival.so.%{major}*

%files -n %{devname}
%doc festdoc-1.4.2/speech_tools
%{_libdir}/libFestival.so
%{_includedir}/festival
%{_datadir}/festival/config
