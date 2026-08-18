%global debug_package %{nil}

Name:       codexbar-cli
Version:    0.52.0
Release:    1%{?dist}
Summary:    AI coding provider usage tracker CLI

License:    MIT
URL:        https://github.com/steipete/CodexBar
Source0:    %{url}/archive/refs/tags/v%{version}.tar.gz

BuildRequires: clang
BuildRequires: git-core
BuildRequires: sqlite-devel
BuildRequires: swift-lang >= 6.2

%description
CodexBar CLI shows usage limits and reset times for AI coding providers.


%prep
%autosetup -n CodexBar-%{version} -p1


%build
CC=clang CXX=clang++ swift build -c release --product CodexBarCLI


%install
install -Dm755 .build/release/CodexBarCLI \
    %{buildroot}%{_libexecdir}/%{name}/codexbar
install -dm755 %{buildroot}%{_bindir}
printf '#!/bin/sh\nexec %{_libexecdir}/%{name}/codexbar "$@"\n' \
    > %{buildroot}%{_bindir}/codexbar
chmod 755 %{buildroot}%{_bindir}/codexbar
printf '%s\n' '%{version}' \
    > %{buildroot}%{_libexecdir}/%{name}/VERSION
strip --strip-all %{buildroot}%{_libexecdir}/%{name}/codexbar


%files
%license LICENSE
%doc README.md
%{_bindir}/codexbar
%{_libexecdir}/%{name}/
