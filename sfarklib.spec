%define major	0
%define libname	%mklibname sfark %{major}
%define devname	%mklibname sfark -d

Name:		sfarklib
Version:	2.24
Release:	2
Summary:	Library for decompressing sfArk sound fonts
License:	GPLv3
Group:		System/Libraries
URL:		https://github.com/raboof/sfArkLib
Source0:	https://github.com/raboof/sfArkLib/archive/%{version}.tar.gz
BuildRequires:	pkgconfig(zlib)

%description
Library for decompressing sfArk sound fonts

%package -n	%{devname}
Summary:	Library for decompressing sfArk sound fonts
Group:		Development/C++
Provides:	%{name}-devel = %{EVRD}
Requires:	%{libname} = %{EVRD}
Requires:	pkgconfig(zlib)

%description -n	%{devname}
Library for decompressing sfArk sound fonts

%prep
%setup -qn sfArkLib-%{version}
chmod -x *

%build
# The makefile is rather broken (wrong soname and all).
# Let's just do the right thing ourselves.
for i in *.cpp; do
	%{__cc} %{optflags} -fPIC -o ${i/.cpp/.o} -c ${i}
done
%{__cc} %{optflags} -fPIC -o libsfark.so.%{major} -shared -Wl,-soname,libsfark.so.%{major} *.o -lz

%install
mkdir -p %{buildroot}%{_libdir} %{buildroot}%{_includedir}
cp *.so.%{major} %{buildroot}%{_libdir}/
ln -s *.so.%{major} %{buildroot}%{_libdir}/libsfark.so
cp sfArkLib.h %{buildroot}%{_includedir}/

%libpackage sfark %{major}

%files -n %{devname}
%{_libdir}/*.so
%{_includedir}/*
