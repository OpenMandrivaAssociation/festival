%define festivalversion 1.96
# we ship the 1.4.2 docs for now.
%define docversion 1.4.2
%define speechtoolsversion 1.2.96

%define major 1
%define libname %mklibname speech_tools %major
%define libnamedevel %mklibname speech_tools -d

Summary: 	A free speech synthesizer 
Name:  		festival
Version: 	%{festivalversion}
Release: 	%mkrel 9
License: 	BSD
Group: 		Sound
URL:		http://www.cstr.ed.ac.uk/projects/festival/
Source: 	http://festvox.org/packed/festival/%{festivalversion}/%{name}-%{version}-beta.tar.bz2
Source1:	http://festvox.org/packed/festival/%{festivalversion}/speech_tools-%{speechtoolsversion}-beta.tar.bz2
Source2: 	http://festvox.org/packed/festival/%{docversion}/festdoc-%{docversion}.tar.bz2
Source3:	siteinit.scm
Source4:	sitevars.scm
# Fix up various locations to be more FSSTND compliant
Patch0:		festival-1.4.1-fsstnd.patch
# Set defaults to American English instead of British English - the OALD
# dictionary (free for non-commercial use only) is needed for BE support
# Additionally, prefer the smaller nitech hts voices.
Patch1:		festival-1.96-nitech-american.patch
# Whack some buildroot references
Patch2: festival_buildroot.patch

# Build the ESD module
Patch4: festival-1.96-speechtools-buildesdmodule.patch
# (fc) 1.2.96-4mdv Fix a coding error (RH bug #162137) (Fedora)
Patch5: festival-1.96-speechtools-rateconvtrivialbug.patch
# (fc) 1.2.96-4mdv Link libs with libm, libtermcap, and libesd (RH bug #198190) (Fedora)
Patch6:		festival-1.96-speechtools-linklibswithotherlibs.patch
# For some reason, CXX is set to gcc on everything but Mac OS Darwin,
# where it's set to g++. Yeah, well. We need it to be right too.
Patch7:		festival-1.96-speechtools-ohjeezcxxisnotgcc.patch
# (fc) 1.2.96-5mdv build speech_tools as shared libraries (Fedora)
Patch8:		festival-1.96-speechtools-shared-build.patch
# (fc) 1.2.96-5mdv fix build with gcc on amd64 and ensure all tests passed
Patch9:		speech_tools-1.2.96-gcc41-amd64-int-pointer.patch
# (fc) 1.2.96-5mdv Look for speech tools here, not back there (Fedora)
Patch10: 	festival-1.96-findspeechtools.patch
# (fc) 1.96-5mdv  Build main library as shared, not just speech-tools (Fedora)
Patch11:	festival-1.96-main-shared-build.patch
# (fc) 1.2.96-5mdv improve soname (Fedora)
Patch12:	festival-1.96-bettersonamehack.patch
# (fc) 1.96-5mdv fix build with gcc 4.3 (Fedora)
Patch13:	festival-1.96-gcc43.patch
# remove invalid gcc option 
Patch14: festival-1.96-speech_tools-remove-invalid-gcc-option.patch
# (fc) 
Patch15:	festival-finnish.patch
# Look for siteinit and sitevars in /etc/festival
Patch16: festival-1.96-etcsiteinit.patch



BuildRequires:	perl
BuildRequires:	ncurses-devel
BuildRequires:  esound-devel
Requires:	festival-voice
BuildRoot: 	%{_tmppath}/%{name}-%{festivalversion}-root 

%description
Festival is a general multi-lingual speech synthesis system developed
at CSTR. It offers a full text to speech system with various APIs, as
well as an environment for development and research of speech synthesis
techniques. It is written in C++ with a Scheme-based command interpreter
for general control.


%package -n speech_tools
Summary: Miscellaneous utilities from the Edinburgh Speech Tools 
Group: Sound
Version: %{speechtoolsversion}
Conflicts: festival < 1.96-9mdv

%description -n speech_tools
Miscellaneous utilities from the Edinburgh Speech Tools. Unless you have a
specific need for one of these programs, you probably don't need to install
this.

%package	devel
Summary:	Static libraries and headers for festival text to speech
Group:		Development/C++
Requires:	%{name} = %{festivalversion}-%{release}
Requires:	termcap-devel
Requires:	speech_tools-devel

%description	devel
Festival is a general multi-lingual speech synthesis system developed
at CSTR. It offers a full text to speech system with various APIs, as
well as an environment for development and research of speech synthesis
techniques. It is written in C++ with a Scheme-based command interpreter
for general control.

This package contains the libraries and includes files necessary to develop
applications using festival.
%package -n	%{libname}
Summary:  	Static libraries and headers for festival text to speech
Group: 		System/Libraries
Version: %{speechtoolsversion}
Requires: 	speech_tools = %{speechtoolsversion}-%{release}

%description -n	%{libname}
Festival is a general multi-lingual speech synthesis system developed
at CSTR. It offers a full text to speech system with various APIs, as
well as an environment for development and research of speech synthesis
techniques. It is written in C++ with a Scheme-based command interpreter
for general control.

This package contains the libraries and includes files necessary for
applications that use festival.

%package -n	%{libnamedevel}
Summary:  	Static libraries and headers for festival text to speech
Group: 		Development/C++
Version: %{speechtoolsversion}
Requires: 	speech_tools = %{speechtoolsversion}-%{release}
Requires: 	%{libname} = %{speechtoolsversion}-%{release}
Provides:	speech_tools-devel = %{speechtoolsversion}-%{release}
Obsoletes:	%mklibname -d speech_tools %major
Obsoletes:	%mklibname -d -s speech_tools

%description -n	%{libnamedevel}
Festival is a general multi-lingual speech synthesis system developed
at CSTR. It offers a full text to speech system with various APIs, as
well as an environment for development and research of speech synthesis
techniques. It is written in C++ with a Scheme-based command interpreter
for general control.

This package contains the libraries and includes files necessary to develop
applications using festival.
 

 
%prep

%setup -q -n festival -a 1 -a 2  
%patch0 -p1 -b .fsstnd
# no backup extension, directory is copied during package install
%patch1 -p1 
%patch2 -p1 -b .buildroot
# no backup extension, directory is copied during package install
%patch4 -p1 
%patch5 -p1 -b .rateconvtrivialbug
%patch6 -p1 -b .linklibswithotherlibs
%patch7 -p1 -b .cxx
%patch8 -p1 -b .shared
%patch9 -p1 -b .gcc41-amd64-int-pointer
# no backup extension, directory is copied during package install
%patch10 -p1 
# no backup extension, directory is copied during package install
%patch11 -p1 
%patch12 -p1 -b .bettersoname
%patch13 -p1 -b .gcc43
%patch14 -p1 -b .remove-invalid-gcc-option
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
  %configure
  # -fPIC 'cause we're building shared libraries and it doesn't hurt
  # -fno-strict-aliasing because of a couple of warnings about code
  #   problems; if $RPM_OPT_FLAGS contains -O2 or above, this puts
  #   it back. Once that problem is gone upstream, remove this for
  #   better optimization.
  make \
    CFLAGS="$RPM_OPT_FLAGS -fPIC -fno-strict-aliasing" \
    CXXFLAGS="$RPM_OPT_FLAGS  -fPIC -fno-strict-aliasing"
cd -

# build the main program
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$(pwd)/src/lib
# instead of doing this, maybe we should patch the make process
# so it looks in the right place explicitly:
export PATH=$(pwd)/bin:$PATH
%configure
make \
  CFLAGS="$RPM_OPT_FLAGS -fPIC" \
  CXXFLAGS="$RPM_OPT_FLAGS -fPIC" 

%check
# all tests must pass
cd speech_tools
#make CFLAGS="$RPM_OPT_FLAGS -fPIC -fno-strict-aliasing" \
#    CXXFLAGS="$RPM_OPT_FLAGS  -fPIC -fno-strict-aliasing" test | grep -v INCORRECT
cd ..

%install
rm -rf %{buildroot}

# install speech tools libs, binaries, and include files
pushd speech_tools

  make INSTALLED_LIB=$RPM_BUILD_ROOT%{_libdir} make_installed_lib_shared
  # no thanks, static libs.
  rm -f $RPM_BUILD_ROOT%{_libdir}/*.a

  make INSTALLED_BIN=$RPM_BUILD_ROOT%{_bindir} make_installed_bin_static
  # this list of the useful programs in speech_tools comes from
  # upstream developer Alan W. Black; the other stuff is to be removed.
  pushd $RPM_BUILD_ROOT%{_bindir}
    ls |
        grep -Evw "ch_wave|ch_track|na_play|na_record|wagon|wagon_test" |
        grep -Evw "make_wagon_desc|pitchmark|pm|sig2fv|wfst_build" |
        grep -Evw "wfst_run|wfst_run" |
        xargs rm
  popd

  pushd include
    for d in $( find . -type d | grep -v win32 ); do
      make -w -C $d INCDIR=$RPM_BUILD_ROOT%{_includedir}/EST/$d install_incs
    done  
  popd

popd


install -d %{buildroot}%{_datadir}/%{name}/{voices/english,dicts}

# bin
make INSTALLED_BIN=$RPM_BUILD_ROOT%{_bindir} make_installed_bin_static
install -m 755 bin/text2wave $RPM_BUILD_ROOT%{_bindir}
#install bin/festival_server* bin/text2wave %{buildroot}%{_bindir}
#install src/main/festival{,_client} %{buildroot}%{_bindir}
# this is just nifty. and it's small.
install -m 755 examples/saytime $RPM_BUILD_ROOT%{_bindir}

# install the shared library
cp -a src/lib/libFestival.so* $RPM_BUILD_ROOT%{_libdir}

# devel
mkdir -p $RPM_BUILD_ROOT%{_includedir}/festival
install src/include/*.h %{buildroot}%{_includedir}/%{name}

# data
cp -r lib config examples %{buildroot}%{_datadir}/%{name}
find %{buildroot}%{_datadir}/%{name} -name Makefile -exec rm \{\} \;

# man pages
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
cp -a doc/*.1 $RPM_BUILD_ROOT%{_mandir}/man1

# lib: the bulk of the program -- the scheme stuff and so on
pushd lib
  mkdir -p $RPM_BUILD_ROOT%{_datadir}/festival/lib
  for f in *.scm festival.el *.ent *.gram *.dtd *.ngrambin speech.properties ; do
    install -m 644 $f $RPM_BUILD_ROOT%{_datadir}/festival/lib/
  done
  mkdir -p $RPM_BUILD_ROOT%{_datadir}/festival/lib/multisyn/
  install -m 644 multisyn/*.scm $RPM_BUILD_ROOT%{_datadir}/festival/lib/multisyn/
popd 

mv -f %{buildroot}/%{_datadir}/%{name}/lib/etc/unknown_RedHatLinux/audsp %{buildroot}/%{_bindir}
rm -Rf %{buildroot}/%{_datadir}/%{name}/lib/etc/
rm -f %{buildroot}%{_datadir}/%{name}/lib/VCLocalRules


# the actual /etc. :)
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/festival
# use our version of this file
rm $RPM_BUILD_ROOT%{_datadir}/festival/lib/siteinit.scm 
install -m 644 %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/festival/siteinit.scm
install -m 644 %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/festival/sitevars.scm

sed -i -e 's,/projects/festival/lib,%{_datadir}/%{name},g' %{buildroot}/%{_datadir}/%{name}/lib/lexicons.scm

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
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
%{_libdir}/libFestival.so.%{festivalversion}*
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
%{_datadir}/festival/examples/intro.text
%{_mandir}/man1/*
%config(noreplace) %{_sysconfdir}/festival

%files devel
%defattr(-,root,root)
%doc festdoc-1.4.2/speech_tools
%{_libdir}/libFestival.so
%{_includedir}/festival
%{_datadir}/festival/config

%files -n speech_tools
%defattr(-,root,root)
%doc speech_tools/INSTALL speech_tools/README
%{_bindir}/ch_track
%{_bindir}/ch_wave
%{_bindir}/make_wagon_desc
%{_bindir}/na_play
%{_bindir}/na_record
%{_bindir}/pitchmark
%{_bindir}/pm
%{_bindir}/sig2fv
%{_bindir}/wagon
%{_bindir}/wagon_test
%{_bindir}/wfst_run
%{_bindir}/wfst_build
%{_datadir}/festival/examples

%files -n %{libname}
%defattr(-,root,root)
%doc speech_tools/README
%{_libdir}/libestbase.so.%{major}*
%{_libdir}/libestools.so.%{major}*
%{_libdir}/libeststring.so.%{major}*

%files -n %{libnamedevel}
%defattr(-,root,root)
%{_includedir}/EST
%{_libdir}/libestbase.so
%{_libdir}/libestools.so
%{_libdir}/libeststring.so
