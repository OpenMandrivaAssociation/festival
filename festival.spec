# we ship the 1.4.2 docs for now.
%define docversion 1.4.2

%define major	2.1
%define libname %mklibname %{name} %{major}
%define devname %mklibname %{name} -d

Summary:	A free speech synthesizer 
Name:		festival
Version:	2.1
Release:	4
License:	BSD
Group:		Sound
Url:		http://www.cstr.ed.ac.uk/projects/festival/
Source0:	http://festvox.org/packed/festival/%{version}/%{name}-%{version}-release.tar.gz
Source1:	http://festvox.org/packed/festival/%{docversion}/festdoc-%{docversion}.tar.bz2
Source2:	siteinit.scm
Source3:	sitevars.scm
# Fix up various locations to be more FSSTND compliant
Patch0:		festival-1.4.1-fsstnd.patch
# Set defaults to American English instead of British English - the OALD
# dictionary (free for non-commercial use only) is needed for BE support
# Additionally, prefer the smaller nitech hts voices.
Patch1:		festival-2.1-nitech-american.patch
Patch3: festival.gcc47.patch
# (fc) 1.2.96-5mdv Look for speech tools here, not back there (Fedora)
##Patch10:	festival-1.96-findspeechtools.patch
# (fc) 1.96-5mdv  Build main library as shared, not just speech-tools (Fedora)
Patch11:	festival-1.96-main-shared-build.patch
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
%setup -qn %{name} -a 1
%apply_patches

# zero length
rm festdoc-1.4.2/speech_tools/doc/index_html.jade
rm festdoc-1.4.2/speech_tools/doc/examples_gen/error_example_section.sgml
rm festdoc-1.4.2/speech_tools/doc/tex_stuff.jade

# (gb) lib64 fixes, don't bother with a patch for now
perl -pi -e '/^REQUIRED_LIBRARY_DIR/ and s,/usr/lib,%{_libdir},' config/project.mak

%build
# build the main program
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$(pwd)/src/lib
# instead of doing this, maybe we should patch the make process
# so it looks in the right place explicitly:
export PATH=$(pwd)/bin:$PATH
%configure2_5x
make \
	CFLAGS="$RPM_OPT_FLAGS -fPIC" \
	CXXFLAGS="$RPM_OPT_FLAGS -fPIC" 

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
%doc ACKNOWLEDGMENTS COPYING INSTALL NEWS README*
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
%{_mandir}/man1/*
%config(noreplace) %{_sysconfdir}/festival

%files -n %{libname}
%{_libdir}/libFestival.so.%{major}*

%files -n %{devname}
%doc festdoc-1.4.2/speech_tools
%{_libdir}/libFestival.so
%{_includedir}/festival
%{_datadir}/festival/config

