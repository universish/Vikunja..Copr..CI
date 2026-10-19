# Dosya Yolu: specs/vikunja.spec
# Fedora Copr (Fedora 44, 45, Rawhide & openSUSE Leap 16.0, Tumbleweed) için Vikunja Sunucu/API Paketi
# Paketleme numarası (_release) her CI çalışmasında otomatik olarak +1 artırılır.

%global debug_package %{nil}
%global _build_id_links none
%global _missing_build_ids_terminate_build 0
%global __strip /bin/true
%global __objdump /bin/true

Name:           vikunja
Version:        %{?_version}%{!?_version:2.7.0}
Release:        %{?_release}%{!?_release:1}%{?dist}
Summary:        The open-source, self-hostable to-do app (Server & Web UI)
License:        AGPL-3.0-or-later
URL:            https://vikunja.io
Source0:        %{name}-%{version}-x86_64.tar.gz
Source1:        %{name}-%{version}-aarch64.tar.gz
Source2:        %{name}-%{version}-armv7.tar.gz

ExclusiveArch:  x86_64 aarch64 armv7hl armv7l
AutoReqProv:    no
Requires:       shadow-utils

%description
Vikunja is an open-source, self-hosted task management application.
This package contains the upstream Vikunja server binary, configuration
template, and systemd unit repackaged for Fedora and openSUSE via Copr
(Build revision: %{name}-v%{version}-%{?_release}%{!?_release:1}).

%prep
%setup -q -c -T

%build
# Önceden derlenmiş upstream RPM içeriği kullanıldığından derleme adımı atlanır.

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

# Çakışmaları önlemek için upstream .build-id bağlarını temizle
rm -rf %{buildroot}/usr/lib/.build-id

# Çıkarılan RPM içeriğinden dinamik dosya listesi oluştur
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

# Özel dizinleri ekle (openSUSE ve Fedora dizin sahipliği uyumluluğu)
find %{buildroot} -type d | while read -r dir_item; do
    rel_dir="${dir_item#%{buildroot}}"
    case "${rel_dir}" in
        ""|"/"|"/usr"|"/usr/bin"|"/usr/lib"|"/usr/lib/systemd"|"/usr/lib/systemd/system"|"/usr/share"|"/usr/share/doc"|"/usr/share/licenses"|"/etc"|"/opt"|"/var"|"/var/lib")
            ;;
        *)
            echo "%dir \"${rel_dir}\"" >> %{_builddir}/filelist.txt
            ;;
    esac
done

%pre
getent group vikunja >/dev/null || groupadd -r vikunja
getent passwd vikunja >/dev/null || useradd -r -g vikunja -d /opt/vikunja -s /sbin/nologin -c "Vikunja Task Manager" vikunja
exit 0

%post
if [ $1 -eq 1 ] && [ -x /usr/bin/systemctl ]; then
    /usr/bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi

%preun
if [ $1 -eq 0 ] && [ -x /usr/bin/systemctl ]; then
    /usr/bin/systemctl --no-reload disable --now vikunja.service >/dev/null 2>&1 || :
fi

%postun
if [ $1 -ge 1 ] && [ -x /usr/bin/systemctl ]; then
    /usr/bin/systemctl try-restart vikunja.service >/dev/null 2>&1 || :
fi

%files -f %{_builddir}/filelist.txt

%changelog
* Mon Oct 19 2026 universish <universish@users.noreply.github.com> - %{version}-%{?_release}%{!?_release:1}
- Automated Copr repackaging of upstream Vikunja RPM (vikunja-v%{version}-%{?_release}%{!?_release:1})
