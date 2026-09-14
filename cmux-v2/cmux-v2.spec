%global debug_package %{nil}

Name:       cmux-v2
Version:    151.0.7922.64
Release:    1%{?dist}
Summary:    Browser and terminal workspace from Manaflow

License:    GPL-3.0-only
URL:        https://github.com/manaflow-ai/cmux-v2
Source0:    %{url}/releases/download/nightly/cmux-linux-x64.deb#/%{name}-%{version}.deb
Source1:    %{url}/releases/download/nightly/SHA256SUMS#/%{name}-%{version}-SHA256SUMS

ExclusiveArch: x86_64

BuildRequires: binutils
BuildRequires: coreutils
BuildRequires: tar
BuildRequires: zstd

Requires: bash
Requires: ca-certificates
Requires: gtk3
Requires: hicolor-icon-theme
Requires: liberation-fonts
Requires: xdg-utils

Provides: cmux-browser = %{version}-%{release}
Provides: webclient

%description
cmux combines a Chromium browser and Ghostty terminal surfaces in one
workspace. This package tracks the upstream Linux x86_64 nightly build.


%prep
%setup -q -c -T
grep '  cmux-linux-x64.deb$' %{SOURCE1} | \
  sed 's|  cmux-linux-x64.deb$|  %{SOURCE0}|' | \
  sha256sum --check -

package_version="$({ ar p %{SOURCE0} control.tar.zst | \
  tar --zstd -xOf - ./control; } | sed -n 's/^Version: \(.*\)-1$/\1/p')"
test "$package_version" = "%{version}"

ar p %{SOURCE0} data.tar.zst | tar --zstd -xf -


%install
mkdir -p %{buildroot}
cp -a opt usr %{buildroot}/

install -dm755 %{buildroot}%{_bindir}
ln -s cmux-browser-stable %{buildroot}%{_bindir}/cmux-browser

install -dm755 %{buildroot}%{_metainfodir}
mv %{buildroot}%{_datadir}/appdata/cmux-browser.appdata.xml \
  %{buildroot}%{_metainfodir}/cmux-browser.metainfo.xml
rmdir %{buildroot}%{_datadir}/appdata

for size in 16 24 32 48 64 128 256; do
  install -Dm644 opt/cmux/browser/product_logo_${size}.png \
    %{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps/cmux-browser.png
done


%files
%license opt/cmux/browser/cmux-licenses/LICENSE
/opt/cmux/
%{_bindir}/cmux-browser
%{_bindir}/cmux-browser-stable
%{_datadir}/applications/cmux-browser.desktop
%{_datadir}/applications/com.cmux.app.desktop
%{_datadir}/gnome-control-center/default-apps/cmux-browser.xml
%{_datadir}/icons/hicolor/*/apps/cmux-browser.png
%{_mandir}/man1/cmux-browser.1*
%{_mandir}/man1/cmux-browser-stable.1*
%{_metainfodir}/cmux-browser.metainfo.xml
%doc %{_docdir}/cmux-browser-stable/
