# Dosya Yolu: specs/veans.spec
# Fedora Copr (Fedora 44, 45, Rawhide & openSUSE Leap 16.0, Tumbleweed) için Veans CLI Paketi
# Paketleme numarası (_release) her CI çalışmasında otomatik olarak +1 artırılır.

%global debug_package %{nil}
%global _build_id_links none
%global _missing_build_ids_terminate_build 0
%global __strip /bin/true
%global __objdump /bin/true

Name:           veans
Version:        %{?_version}%{!?_version:2.7.0}
Release:        %{?_release}%{!?_release:1}%{?dist}
Summary:        Veans CLI - Command-line and agent tool for Vikunja
License:        AGPL-3.0-or-later
URL:            https://vikunja.io
Source0:        %{name}-%{version}-x86_64.tar.gz
Source1:        %{name}-%{version}-aarch64.tar.gz
Source2:        %{name}-%{version}-armv7.tar.gz

ExclusiveArch:  x86_64 aarch64 armv7hl armv7l
AutoReqProv:    no

%description
Veans is the official command-line and agent CLI tool for interacting with Vikunja.
Repackaged from upstream veans-v%{version} RPM releases for Fedora and openSUSE
(Build revision: %{name}-v%{version}-%{?_release}%{!?_release:1}).

%prep
%setup -q -c -T

%build
# Önceden derlenmiş upstream RPM içeriği kullanılır.

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}

%ifarch x86_64
tar -xzf %{SOURCE0} -C %{buildroot}
%endif
%ifarch aarch64
tar -xzf %{SOURCE1} -C %{buildroot}
%endif
%ifarch armv7hl armv7l
tar -xzf %{SOURCE2} -C %{buildroot}
%endif

rm -rf %{buildroot}/usr/lib/.build-id

> %{_builddir}/filelist.txt
find %{buildroot} \( -type f -o -type l \) | while read -r item; do
    rel_path="${item#%{buildroot}}"
    case "${rel_path}" in
        /etc/*)
            echo "%config(noreplace) \"${rel_path}\"" >> %{_builddir}/filelist.txt
            ;;
        *)
            echo "\"${rel_path}\"" >> %{_builddir}/filelist.txt
            ;;
    esac
done

find %{buildroot} -type d | while read -r dir_item; do
    rel_dir="${dir_item#%{buildroot}}"
    case "${rel_dir}" in
        ""|"/"|"/usr"|"/usr/bin"|"/usr/lib"|"/usr/share"|"/usr/share/doc"|"/usr/share/licenses"|"/usr/share/man"|"/etc"|"/opt")
            ;;
        *)
            echo "%dir \"${rel_dir}\"" >> %{_builddir}/filelist.txt
            ;;
    esac
done

%files -f %{_builddir}/filelist.txt

%changelog
* Mon Oct 19 2026 universish <universish@users.noreply.github.com> - %{version}-%{?_release}%{!?_release:1}
- Automated Copr repackaging of upstream veans RPM (veans-v%{version}-%{?_release}%{!?_release:1})
