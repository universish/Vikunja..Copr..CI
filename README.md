# Vikunja..Copr..CI

Bu depo ([`universish/Vikunja..Copr..CI`](https://github.com/universish/Vikunja..Copr..CI)), [`go-vikunja/vikunja`](https://github.com/go-vikunja/vikunja/releases) ve [`dl.vikunja.io`](https://dl.vikunja.io/desktop/) kaynaklarını günde iki kez (Vikunja merkezi olan **Lübeck, Almanya** saatiyle öğle arasında ve iş çıkışında) otomatik olarak tarayarak **Vikunja Desktop**, **vikunja** ve **veans** RPM paketlerini yeniden paketler ve [`universish/Vikunja..` Fedora Copr](https://copr.fedorainfracloud.org/coprs/universish/Vikunja../) deposunda yayınlar.

## Depo Dosya Yapısı

Dosyaları GitHub deponuza aşağıdaki dizin yapısıyla yerleştirin:

| Depo İçi Dosya Yolu | Açıklama |
| :--- | :--- |
| `.github/workflows/vikunja-copr-ci.yml` | 3 aşamalı otomatik GitHub Actions iş akışı |
| `scripts/repackage_and_publish.sh` | RPM indirme, `rpm2cpio` ile açma, SRPM üretme ve Copr yayınlama betiği |
| `specs/vikunja.spec` | `vikunja` sunucu/API RPM `.spec` dosyası (`x86_64`, `aarch64`, `armv7`) |
| `specs/vikunja-desktop.spec` | `vikunja-desktop` istemci RPM `.spec` dosyası (`Vikunja Desktop-vX.Y.Z.rpm`) |
| `specs/veans.spec` | `veans` CLI aracı RPM `.spec` dosyası (`x86_64`, `aarch64`, `armv7`) |
| `LAST_VERSION` | Son yayınlanan sürüm numarasını takip eden durum dosyası (ilk kurulumda `0.0.0` yazabilirsiniz) |

## İş Akışı Aşamaları

1. **1. Aşama (`stage1_github_releases`)**:
   - Lübeck, Almanya (`Europe/Berlin`) saatiyle günde iki kez (**11:00 UTC** öğle arası ve **16:00 UTC** iş çıkışı) çalışır.
   - [`go-vikunja/vikunja/releases`](https://github.com/go-vikunja/vikunja/releases) adresinde aşağıdaki 7 dosyayı arar:
     - `Vikunja Desktop-vX.Y.Z.rpm`
     - `vikunja-vX.Y.Z-x86_64.rpm`
     - `vikunja-vX.Y.Z-armv7.rpm`
     - `vikunja-vX.Y.Z-aarch64.rpm`
     - `veans-vX.Y.Z-x86_64.rpm`
     - `veans-vX.Y.Z-armv7.rpm`
     - `veans-vX.Y.Z-aarch64.rpm`
   - Yeni güncelleme ve dosyalar doğrulanırsa **2. aşamayı atlayarak direkt 3. aşamaya geçer**. Doğrulanmazsa **2. aşamaya geçer**.
2. **2. Aşama (`stage2_dl_vikunja`)**:
   - Yalnızca 1. aşamada yeni güncelleme doğrulanmadığında devreye girer.
   - `https://dl.vikunja.io/desktop/vX.Y.Z/Vikunja%20Desktop-vX.Y.Z.rpm` (örn. `https://dl.vikunja.io/desktop/v2.7.0/Vikunja%20Desktop-v2.7.0.rpm` -> `Vikunja Desktop-v2.7.0.rpm`) adresini kontrol eder.
   - Yeni sürüm doğrulanırsa **3. aşamaya geçer**.
3. **3. Aşama (`stage3_repackage_and_publish`)**:
   - Fedora konteyneri içinde upstream `.rpm` paketlerini indirir ve `rpm2cpio | cpio -idmv` ile açar.
   - `specs/*.spec` dosyalarıyla `.src.rpm` (SRPM) olarak yeniden paketler ve `copr-cli` ile [`universish/Vikunja..`](https://copr.fedorainfracloud.org/coprs/universish/Vikunja../) deposuna gönderir.
   - Paketlenen sürümü `LAST_VERSION` dosyasına kaydedip depoya commit eder.

## Desteklenen Dağıtımlar ve İşlemci Mimarileri (Chroots)

| Dağıtım | `x86_64` Chroot | `aarch64` Chroot |
| :--- | :--- | :--- |
| **openSUSE Tumbleweed** | `opensuse-tumbleweed-x86_64` | `opensuse-tumbleweed-aarch64` |
| **openSUSE Leap 16.0** | `opensuse-leap-16.0-x86_64` | `opensuse-leap-16.0-aarch64` |
| **Fedora Rawhide** | `fedora-rawhide-x86_64` | `fedora-rawhide-aarch64` |
| **Fedora 45** | `fedora-45-x86_64` | `fedora-45-aarch64` |
| **Fedora 44** | `fedora-44-x86_64` | `fedora-44-aarch64` |

## Kurulum ve GitHub Secret Yapılandırması

1. [Fedora Copr API](https://copr.fedorainfracloud.org/api/) sayfasına giriş yapın ve size özel üretilen `[copr-cli]` yapılandırma metnini kopyalayın:
   ```ini
   [copr-cli]
   login = ...
   username = universish
   token = ...
   copr_url = https://copr.fedorainfracloud.org
   ```
2. GitHub deponuzda **Settings -> Secrets and variables -> Actions -> New repository secret** adımlarını izleyin.
3. Secret adını `COPR_CONFIG` olarak belirleyin ve kopyaladığınız içeriği yapıştırıp kaydedin.
4. Deponuzda **Settings -> Actions -> General -> Workflow permissions** altından **Read and write permissions** seçeneğini etkinleştirin (`LAST_VERSION` dosyasının otomatik güncellenebilmesi için).
