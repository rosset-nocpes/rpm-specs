%global debug_package %{nil}

Name:       hydroxide
Version:    0.2.32
Release:    1%{?dist}
Summary:    A third-party, open-source ProtonMail CardDAV, IMAP and SMTP bridge

License:    MIT
URL:        https://codeberg.org/emersion/hydroxide
Source0:    %{url}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:    hydroxide.sysusers
Source2:    system.service
Source3:    user.service

BuildRequires: gcc
BuildRequires: golang >= 1.24
BuildRequires: systemd-rpm-macros

Requires: glibc

%description
Hydroxide is a third-party, open-source ProtonMail bridge. It is a server
that translates standard protocols (SMTP, IMAP and CardDAV) into ProtonMail
API requests, allowing the use of regular e-mail clients with ProtonMail. It
provides only a CLI, so it runs in headless environments.


%prep
%autosetup -p1 -n %{name}


%build
export CGO_CPPFLAGS="%{optflags}"
export CGO_CFLAGS="%{optflags}"
export CGO_CXXFLAGS="%{optflags}"
export CGO_LDFLAGS="%{__global_ldflags}"
export GOFLAGS="-buildmode=pie -trimpath -mod=readonly -modcacherw"
go build -o hydroxide ./cmd/hydroxide


%install
install -Dm755 hydroxide %{buildroot}%{_bindir}/hydroxide
strip --strip-all %{buildroot}%{_bindir}/hydroxide

install -Dm644 %{SOURCE1} %{buildroot}%{_sysusersdir}/hydroxide.conf
install -Dm644 %{SOURCE2} %{buildroot}%{_unitdir}/hydroxide.service
install -Dm644 %{SOURCE3} %{buildroot}%{_userunitdir}/hydroxide.service


%files
%license LICENSE
%doc README.md
%{_bindir}/hydroxide
%{_unitdir}/hydroxide.service
%{_userunitdir}/hydroxide.service
%{_sysusersdir}/hydroxide.conf
