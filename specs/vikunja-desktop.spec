# Dosya Yolu: specs/vikunja-desktop.spec
# Fedora Copr (Fedora 44, 45, Rawhide & openSUSE Leap 16.0, Tumbleweed) için Vikunja Desktop Paketi

%global debug_package %{nil}
%global _build_id_links none
%global _missing_build_ids_terminate_build 0
%global _binaries_in_noarch_packages_terminate_build 0
%global __strip /bin/true
%global __objdump /bin/true

Name:           vikunja-desktop
Version:        %{?_version}%{!?_version:2.7.0}
Release:        1%{?dist}
Summary:        Vikunja Desktop Application
License:        GPL-3.0-or-later
URL:            https://vikunja.io
Source0:        %{name}-%{version}.tar.gz

ExclusiveArch:  x86_64 aarch64
AutoReqProv:    no

%description
Official desktop client for Vikunja, the open-source, self-hostable to-do app.
Repackaged from upstream Vikunja Desktop-v%{version}.rpm for Fedora and openSUSE.

%prep
%setup -q -c -T

%build
# Önceden derlenmiş upstream Vikunja Desktop-vX.Y.Z.rpm içeriği kullanılır.

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}
tar -xzf %{SOURCE0} -C %{buildroot}

# Çakışmaları önlemek için upstream .build-id bağlarını temizle
rm -rf %{buildroot}/usr/lib/.build-id

# Çıkarılan RPM içeriğinden dinamik dosya listesi oluştur (boşluklu dosya adlarını destekler)
> %{_builddir}/filelist.txt
find %{buildroot} \( -type f -o -type l \) | while read -r item; do
    rel_path="${item#%{buildroot}}"
    echo "\"${rel_path}\"" >> %{_builddir}/filelist.txt
done

find %{buildroot} -type d | while read -r dir_item; do
    rel_dir="${dir_item#%{buildroot}}"
    case "${rel_dir}" in
        ""|"/"|"/usr"|"/usr/bin"|"/usr/lib"|"/usr/share"|"/usr/share/applications"|"/usr/share/icons"|"/usr/share/icons/hicolor"|"/usr/share/icons/hicolor/*"|"/usr/share/doc"|"/usr/share/licenses"|"/etc"|"/opt")
            ;;
        *)
            echo "%dir \"${rel_dir}\"" >> %{_builddir}/filelist.txt
            ;;
    esac
done

%files -f %{_builddir}/filelist.txt

%changelog
* Mon Oct 19 2026 universish <universish@users.noreply.github.com> - %{version}-1
- Automated Copr repackaging of upstream Vikunja Desktop-v%{version}.rpm
