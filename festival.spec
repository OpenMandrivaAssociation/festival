Summary: 	A free speech synthesizer 
Name:  		festival
Version: 	1.96
Release: 	%mkrel 1
License: 	BSD
Group: 		Sound
URL:		http://www.festvox.org/festival/index.html
Source: 	%{name}-%{version}-beta.tar.bz2
Source2: 	festdoc-1.4.2.tar.bz2
Source3: 	speech_tools-config
Source5: 	festival-1.4.3-config
# (nonotor) Code from speech_utils 1.2.95 needed
# We should merge speech_utils and festival source rpm...
Source6:	base_class.tar.bz2
# Fix up various locations to be more FSSTND compliant
Patch:		festival-1.4.1-fsstnd.patch
#Patch2:         %{name}-config.patch
# Set defaults to American English instead of British English - the OALD
# dictionary (free for non-commercial use only) is needed for BE support
Patch1:		festival-american.patch
Patch3:		festival-1.4.3-config.patch
# Translate this strange pseudocode to real C++
Patch21:	festival-1.4.2-c++.patch
Patch22:	festival-1.4.3-gcc3_4.patch
# needed by the asterisk pbx software
Patch23:	festival-1.4.3-asterisk.diff
Patch24:	festival-1.95-findlibs.patch
# http://qa.mandriva.com/show_bug.cgi?id=27646
Patch25:	festival-fix-gcc4.1.2.patch
Patch26:	festival-finnish.patch
BuildRequires:	perl
BuildRequires:	libtermcap-devel
BuildRequires:	speech_tools-devel
Requires:	festival-voice
BuildRoot: 	%{_tmppath}/%{name}-%{version}-root 

# Somebody please teach the source code what C++ looks like this millenium

%description
Festival is a general multi-lingual speech synthesis system developed
at CSTR. It offers a full text to speech system with various APIs, as
well as an environment for development and research of speech synthesis
techniques. It is written in C++ with a Scheme-based command interpreter
for general control.

%package	devel
Summary:	Static libraries and headers for festival text to speech
Group:		Development/C++
Requires:	%{name} = %{version}-%{release}
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
 
%prep

%setup -q -n festival -a 2 -a 6
#ln -sf festival/speech_tools ../speech_tools
#%patch -p1
%patch3 -p1
#patch1 -p1 -b .americandefault
#%patch21 -p1 -b .fv_c++
#%patch22 -p1 -b .gcc3_4
# needed by the asterisk pbx software
#%patch23 -p1 -b .asterisk
#%patch24 -p1 -b .findlib
#%patch25 -p1 -b .gcc4.1.2
%patch26 -p1

# zero length
rm festdoc-1.4.2/speech_tools/doc/index_html.jade
rm festdoc-1.4.2/speech_tools/doc/examples_gen/error_example_section.sgml
rm festdoc-1.4.2/speech_tools/doc/tex_stuff.jade

rm -f bin/VCLocalRules

# (gb) lib64 fixes, don't bother with a patch for now
perl -pi -e '/^REQUIRED_LIBRARY_DIR/ and s,/usr/lib,%{_libdir},' config/project.mak
# (nonotor) EST_THash.h in /usr/include/EST
#perl -pi -e 's|include\ \"EST_THash\.h\"|include\ \<EST\/EST_THash.h\>|' src/modules/MultiSyn/Diphone* src/modules/UniSyn_diphone/us_diphone.h

%build
%configure
make 

%install
rm -rf %{buildroot}
install -d %{buildroot}{%{_bindir},%{_datadir}/%{name}/{voices/english,dicts},%{_libdir},%{_includedir}/%{name},%{_mandir}/man1}

# bin
install bin/festival_server* bin/text2wave %{buildroot}%{_bindir}
install src/main/festival{,_client} %{buildroot}%{_bindir}

# devel
install src/lib/libFestival.a %{buildroot}%{_libdir}
install src/include/*.h %{buildroot}%{_includedir}/%{name}

# data
cp -r lib config examples %{buildroot}%{_datadir}/%{name}
find %{buildroot}%{_datadir}/%{name} -name Makefile -exec rm \{\} \;

install doc/festival{,_client}.1 %{buildroot}%{_mandir}/man1

mv -f %{buildroot}/%{_datadir}/%{name}/lib/etc/unknown_RedHatLinux/audsp %{buildroot}/%{_bindir}
rm -Rf %{buildroot}/%{_datadir}/%{name}/lib/etc/

perl -pi -e 's,/projects/festival/lib,%{_datadir}/%{name},g' %{buildroot}/%{_datadir}/%{name}/lib/lexicons.scm

find festdoc-1.4.2 -type d -name 'CVS' -exec rm -Rf {} \;|| true

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc ACKNOWLEDGMENTS COPYING INSTALL NEWS README*
%doc festdoc-1.4.2/festival/html/*html
%doc festdoc-1.4.2/festival/info
%doc festdoc-1.4.2/festival/festival.ps
%{_bindir}/*
%{_datadir}/festival
%{_mandir}/man1/*

%files devel
%defattr(-,root,root)
%doc festdoc-1.4.2/speech_tools
%{_libdir}/*.a
%dir %{_includedir}/festival
%{_includedir}/festival/*
