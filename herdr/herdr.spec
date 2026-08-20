%global debug_package %{nil}
%global zig_version 0.15.2

%ifarch ppc64le
%global zig_arch powerpc64le
%else
%global zig_arch %{_arch}
%endif

Name:       herdr
Version:    0.8.2
Release:    1%{?dist}
Summary:    Terminal multiplexer for supervising coding agents

License:    Apache-2.0
URL:        https://github.com/herdrdev/herdr
Source0:    %{url}/archive/refs/tags/v%{version}.tar.gz

%if 0%{?el8}
%else
BuildRequires: cargo >= 1.96.1
BuildRequires: rust >= 1.96.1
%endif
BuildRequires: gcc
BuildRequires: cmake
%if 0%{?fedora} == 43 || 0%{?fedora} >= 45
BuildRequires: curl
%else
BuildRequires: zig = %{zig_version}
%endif

%description
Herdr is a terminal multiplexer for supervising multiple coding agents. It provides workspaces, tabs, panes, persistent sessions, and agent status tracking in a single terminal interface.


%prep
%autosetup -p1
%if 0%{?el8}
  curl https://sh.rustup.rs -sSf | sh -s -- --profile minimal -y
%endif
%if 0%{?fedora} == 43 || 0%{?fedora} >= 45
curl --fail --location --retry 3 \
  --output zig-%{zig_version}.tar.xz \
  https://ziglang.org/download/%{zig_version}/zig-%{zig_arch}-linux-%{zig_version}.tar.xz
tar -xf zig-%{zig_version}.tar.xz
%endif


%install
export CARGO_PROFILE_RELEASE_BUILD_OVERRIDE_OPT_LEVEL=3
export HERDR_BUILD_CHANNEL=stable
%if 0%{?fedora} == 43 || 0%{?fedora} >= 45
export PATH="$PWD/zig-%{zig_arch}-linux-%{zig_version}:$PATH"
%endif
%if 0%{?el8}
  $HOME/.cargo/bin/cargo install --locked --root=%{buildroot}%{_prefix} --path=.
%else
  cargo install --locked --root=%{buildroot}%{_prefix} --path=.
%endif

rm -f %{buildroot}%{_prefix}/.crates.toml \
    %{buildroot}%{_prefix}/.crates2.json
strip --strip-all %{buildroot}%{_bindir}/*


%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
