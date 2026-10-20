#!/usr/bin/env bash
# Dosya Yolu: scripts/repackage_and_publish.sh
# 3. Aşama: Upstream RPM dosyalarını indirir, rpm2cpio ile açar,
# paketleme numarasını (+1) uygulayarak Fedora Copr .spec dosyalarıyla SRPM üretir ve
# https://copr.fedorainfracloud.org/coprs/universish/Vikunja../ deposuna yayınlar.

set -euo pipefail

VERSION="${1:?Kullanım: $0 <X.Y.Z> [stage1|stage2] [paket-numarasi]}"
VERSION="${VERSION#v}"
SOURCE_STAGE="${2:-stage1}"
RELEASE_NUM="${3:-}"

# Eğer dışarıdan RELEASE_NUM verilmediyse RELEASE_NUMBER dosyasından okuyup +1 artır
if [ -z "${RELEASE_NUM}" ]; then
  CURRENT_REL=0
  if [ -f "RELEASE_NUMBER" ]; then
    RAW_REL=$(tr -d '[:space:]' < RELEASE_NUMBER || echo "0")
    if [[ "${RAW_REL}" =~ ^[0-9]+$ ]]; then
      CURRENT_REL="${RAW_REL}"
    fi
  fi
  RELEASE_NUM=$((CURRENT_REL + 1))
fi

COPR_REPO="${COPR_REPO:-universish/Vikunja..}"
GH_RELEASE_BASE="https://github.com/go-vikunja/vikunja/releases/download/v${VERSION}"
DL_BASE="https://dl.vikunja.io"

# Hedef dağıtımlar ve işlemci mimarileri (Chroots)
TARGET_CHROOTS=(
  "opensuse-tumbleweed-x86_64"
  "opensuse-leap-16.0-x86_64"
  "opensuse-tumbleweed-aarch64"
  "opensuse-leap-16.0-aarch64"
  "fedora-rawhide-x86_64"
  "fedora-rawhide-aarch64"
  "fedora-45-x86_64"
  "fedora-44-x86_64"
  "fedora-45-aarch64"
  "fedora-44-aarch64"
)

WORKDIR="$(mktemp -d)"
DOWNLOAD_DIR="${WORKDIR}/downloads"
EXTRACT_DIR="${WORKDIR}/extract"
RPMBUILD_DIR="${HOME}/rpmbuild"

mkdir -p "${DOWNLOAD_DIR}" "${EXTRACT_DIR}"
rpmdev-setuptree

echo "=================================================================="
echo "Vikunja v${VERSION}-${RELEASE_NUM} 3. Aşama Başlatıldı (Kaynak: ${SOURCE_STAGE})"
echo "Paket Sürüm Formatı: vikunja-v${VERSION}-${RELEASE_NUM}"
echo "Hedef Copr Deposu: ${COPR_REPO}"
echo "=================================================================="

# Yardımcı fonksiyon: Birden fazla olası URL'den dosya indirme
download_with_fallback() {
  local output_file="$1"
  shift
  for url in "$@"; do
    echo "İndirme deneniyor: ${url}"
    if curl -fL --retry 3 --retry-delay 2 -o "${output_file}" "${url}"; then
      echo "Başarıyla indirildi: $(basename "${output_file}")"
      return 0
    fi
  done
  echo "::error::$(basename "${output_file}") hiçbir adresten indirilemedi!"
  return 1
}

# 1. Yedi RPM dosyasını indir
# 1.1 Vikunja Desktop-vX.Y.Z.rpm
download_with_fallback "${DOWNLOAD_DIR}/Vikunja Desktop-v${VERSION}.rpm" \
  "${GH_RELEASE_BASE}/Vikunja%20Desktop-v${VERSION}.rpm" \
  "${GH_RELEASE_BASE}/Vikunja.Desktop-v${VERSION}.rpm" \
  "${DL_BASE}/desktop/v${VERSION}/Vikunja%20Desktop-v${VERSION}.rpm"

# 1.2 vikunja-vX.Y.Z-{x86_64,armv7,aarch64}.rpm
for arch in x86_64 armv7 aarch64; do
  download_with_fallback "${DOWNLOAD_DIR}/vikunja-v${VERSION}-${arch}.rpm" \
    "${GH_RELEASE_BASE}/vikunja-v${VERSION}-${arch}.rpm" \
    "${DL_BASE}/vikunja/v${VERSION}/vikunja-v${VERSION}-${arch}.rpm"
done

# 1.3 veans-vX.Y.Z-{x86_64,armv7,aarch64}.rpm
for arch in x86_64 armv7 aarch64; do
  download_with_fallback "${DOWNLOAD_DIR}/veans-v${VERSION}-${arch}.rpm" \
    "${GH_RELEASE_BASE}/veans-v${VERSION}-${arch}.rpm" \
    "${DL_BASE}/veans/v${VERSION}-${arch}.rpm" \
    "${DL_BASE}/veans/v${VERSION}/veans-v${VERSION}-${arch}.rpm"
done

# 2. İndirilen RPM dosyalarını aç (rpm2cpio | cpio) ve tar.gz kaynak arşivlerine dönüştür
unpack_rpm_to_tarball() {
  local rpm_path="$1"
  local tarball_name="$2"
  local pkg_extract_dir="${EXTRACT_DIR}/${tarball_name%.tar.gz}"

  echo "RPM açılıyor: $(basename "${rpm_path}") -> ${tarball_name}"
  rm -rf "${pkg_extract_dir}"
  mkdir -p "${pkg_extract_dir}"

  (
    cd "${pkg_extract_dir}"
    rpm2cpio "${rpm_path}" | cpio -idmv --no-absolute-filenames
    rm -rf usr/lib/.build-id
    tar -czf "${RPMBUILD_DIR}/SOURCES/${tarball_name}" .
  )
}

# 2.1 Vikunja Desktop RPM açma
unpack_rpm_to_tarball \
  "${DOWNLOAD_DIR}/Vikunja Desktop-v${VERSION}.rpm" \
  "vikunja-desktop-${VERSION}.tar.gz"

# 2.2 vikunja (x86_64, armv7, aarch64) RPM açma
for arch in x86_64 armv7 aarch64; do
  unpack_rpm_to_tarball \
    "${DOWNLOAD_DIR}/vikunja-v${VERSION}-${arch}.rpm" \
    "vikunja-${VERSION}-${arch}.tar.gz"
done

# 2.3 veans (x86_64, armv7, aarch64) RPM açma
for arch in x86_64 armv7 aarch64; do
  unpack_rpm_to_tarball \
    "${DOWNLOAD_DIR}/veans-v${VERSION}-${arch}.rpm" \
    "veans-${VERSION}-${arch}.tar.gz"
done

# 3. Spec dosyaları ile SRPM (.src.rpm) paketlerini oluştur
# ÖNEMLİ: PWA paketi için ikon dosyasını SOURCES dizinine kopyalayın (yolu deponuza göre ayarlayın)
cp vikunja.png "${RPMBUILD_DIR}/SOURCES/"

cp specs/vikunja.spec specs/vikunja-desktop.spec specs/veans.spec specs/vikunja-pwa-webui.spec "${RPMBUILD_DIR}/SPECS/"

for spec_name in vikunja vikunja-desktop veans vikunja-pwa-webui; do
  echo "SRPM oluşturuluyor: ${spec_name}"
  rpmbuild -bs \
    --define "_version ${VERSION}" \
    --define "_release ${RELEASE_NUM}" \
    "${RPMBUILD_DIR}/SPECS/${spec_name}.spec"
done

echo "Oluşturulan SRPM paketleri:"
ls -lh "${RPMBUILD_DIR}/SRPMS/"

# 4. Fedora Copr deposunda hedef dağıtım/mimari chroot'larını etkinleştir
CHROOT_ARGS=()
for chroot in "${TARGET_CHROOTS[@]}"; do
  CHROOT_ARGS+=("-r" "${chroot}")
done

echo "Fedora Copr (${COPR_REPO}) chroot yapılandırması güncelleniyor..."
copr-cli modify "${CHROOT_ARGS[@]}" "${COPR_REPO}" || \
  echo "::warning::copr-cli modify komutu atlandı veya chroot'lar zaten tanımlı."

# 5. SRPM paketlerini Fedora Copr deposuna gönder ve yayınla
# PWA paketinin spec içindeki asıl adı 'vikunja-webui-pwa' olduğu için listeye bu isimle ekliyoruz
for pkg_name in vikunja vikunja-desktop veans vikunja-webui-pwa; do
  # PWA paketinin versiyon isimlendirmesi (1.0.0-1) diğerlerinden farklı olabileceği için find komutunu daha genel tutuyoruz
  srpm_file=$(find "${RPMBUILD_DIR}/SRPMS" -maxdepth 1 -name "${pkg_name}-*.src.rpm" | head -n 1)
  
  if [ -z "${srpm_file}" ]; then
    echo "::error::${pkg_name} için SRPM dosyası bulunamadı!"
    exit 1
  fi

  echo "Fedora Copr üzerine gönderiliyor: ${srpm_file}"
  copr-cli build \
    --nowait \
    "${CHROOT_ARGS[@]}" \
    "${COPR_REPO}" \
    "${srpm_file}"
done

echo "=================================================================="
echo "Tüm paketler (vikunja, vikunja-desktop, veans v${VERSION}-${RELEASE_NUM})"
echo "https://copr.fedorainfracloud.org/coprs/${COPR_REPO}/ deposuna gönderildi!"
echo "=================================================================="
