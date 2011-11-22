# Copyright (c) 2000-2005, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%define base_name easymock

Name:           %{base_name}2
Version:        2.0
Release:        %mkrel 2.0.5-1
Epoch:          0
Summary:        Easy mock objects

Group:          Development/Java
License:        MIT
URL:            http://www.easymock.org/
Source0:        easymock-2.0-src.tar.gz
# cvs -d:pserver:anonymous@cvs.sourceforge.net:/cvsroot/easymock login
# cvs -z3 -d:pserver:anonymous@cvs.sourceforge.net:/cvsroot/easymock export -r EasyMock2_0 easymock

Patch0:		easymock-2.0-build_xml.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

BuildArch:      noarch
BuildRequires:  java-rpmbuild 
BuildRequires:  jpackage-utils >= 0:1.6
BuildRequires:  ant >= 0:1.6
BuildRequires:	ant-junit >= 0:1.6
BuildRequires:	junit >= 0:3.8.1
BuildRequires:  java-devel >= 0:1.5.0
Requires:  java >= 0:1.5.0
Provides:   easymock

%description
EasyMock provides Mock Objects for interfaces in JUnit tests by generating 
them on the fly using Java's proxy mechanism. Due to EasyMock's unique style 
of recording expectations, most refactorings will not affect the Mock Objects. 
So EasyMock is a perfect fit for Test-Driven Development.

%package        javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description    javadoc
Javadoc for %{name}


%prep
%setup -q -n %{base_name}
mkdir lib
pushd lib
ln -sf $(build-classpath junit) .
popd
echo "java\ 1.5=%{_jvmdir}/java-rpmbuild/bin/java" >> easymockbuild.properties
echo "java\ compiler=%{_jvmdir}/java-rpmbuild/bin/javac" >> easymockbuild.properties

%patch0 -b .sav

%build
export OPT_JAR_LIST="ant/ant-junit junit"
export CLASSPATH=
%{ant} -Dbuild.sysclasspath=first


%install
rm -rf $RPM_BUILD_ROOT
unzip %{base_name}%{version}.zip
install -dm 755 $RPM_BUILD_ROOT%{_javadir}

install -pm 644 %{base_name}%{version}/%{base_name}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
ln -s %{name}-%{version}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}.jar

# javadoc
install -dm 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr %{base_name}%{version}/javadoc/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name} 

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_javadir}/*.jar
%doc %{base_name}%{version}/{Documentation,License}.html

%files javadoc
%defattr(-,root,root,-)
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}
