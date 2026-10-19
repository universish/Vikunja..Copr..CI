# Vikunja..Copr..CI

This repository ([`universish/Vikunja..Copr..CI`](https://github.com/universish/Vikunja..Copr..CI)) automatically scans the [`go-vikunja/vikunja`](https://github.com/go-vikunja/vikunja/releases) and [`dl.vikunja.io`] (https://dl.vikunja.io/desktop/) automatically twice a day (at noon and at the end of the workday, according to the time in **Lübeck, Germany**, where the Vikunja headquarters is located) to repackage **Vikunja Desktop** (`vikunja-desktop`), **Vikunja Server** (`vikunja`), and **Veans CLI** (`veans`) RPM packages and publishes them to the [`universish/Vikunja..` Fedora COPR](https://copr.fedorainfracloud.org/coprs/universish/Vikunja../) repository.

After each packaging run, the RPM package number (`Release`) is automatically **incremented by +1** (`vikunja-v<version>-<package-number>`). This ensures that when a packaging error is fixed and the package is recompiled for the same version, `dnf` and `zypper` immediately recognize the new package as an update.

## About Vikunja

### The task manager you actually own.

**Vikunja** is open-source task management with lists, Kanban, Gantt, and more. Self-host it or let us run it for you.
*Made and hosted in the EU. Plan with the elegance of a sloth on a sunny day.*

* **Your data, your server:** Run Vikunja on your own infrastructure. Your tasks, your projects, your rules. Open-source under the AGPLv3 — you can read every line of code.
* **Grows with your team:** Start with your personal to-do list. When your team needs it too, share projects, assign tasks, and collaborate — without switching to a different tool.
* **List, Kanban, Gantt, Table:** Four ways to view your tasks. Use whatever fits how your brain works — or switch between views whenever you need to.
* **Built-in Migration Support:** Vikunja has built-in migration support for Todoist, Trello, Microsoft To-Do, and other platforms. You can import your existing tasks and projects directly from the Vikunja interface.

> "Getting more organized is hard. I built Vikunja because there was no good Open-Source Tool to do what I wanted. Privacy is important. For me, you should be able to look at the code of a piece of software you use a lot. Especially if it is something like a to-do app you use daily.
>
> Vikunja Cloud is the best way for me to make sure the project can continue to live on and be self-sustainable. Being completely bootstrapped, the users of the software are the top priority and not some VC."
>
> — **Konrad**, Founder of Vikunja

Vikunja is an open-source, self-hostable to-do app. It helps you organize your tasks and projects with features like list, kanban, gantt, and table views — all while keeping your data under your control.

Vikunja is licensed under the AGPLv3 and completely free to self-host. If you prefer not to manage your own server, [Vikunja Cloud](https://app.vikunja.cloud/?redirectToProvider=true) offers a paid hosted option. You can install Vikunja using Docker/Podman, native binaries/packages for your platform, or sign up for [Vikunja Cloud](https://app.vikunja.cloud/?redirectToProvider=true). Use the [install wizard](https://vikunja.io/install) for a guided setup. While self-hosting is a great option, Vikunja Cloud gives you a fully managed instance with automatic updates, backups, and zero maintenance. It's the easiest way to get started and directly supports the continued development of Vikunja.

## Supported Distributions and Processor Architectures (Chroots)

| Distribution | `x86_64` Chroot | `aarch64` Chroot |
| :--- | :--- | :--- |
| **Fedora Rawhide** | `fedora-rawhide-x86_64` | `fedora-rawhide-aarch64` |
| **Fedora 45** | `fedora-45-x86_64` | `fedora-45-aarch64` |
| **Fedora 44** | `fedora-44-x86_64` | `fedora-44-aarch64` |
| **openSUSE Tumbleweed** | `opensuse-tumbleweed-x86_64` | `opensuse-tumbleweed-aarch64` |
| **openSUSE Leap 16.0** | `opensuse-leap-16.0-x86_64` | `opensuse-leap-16.0-aarch64` |

## Installation, Update, and Removal Commands (Fedora & openSUSE)

### 1. Fedora (44, 45, Rawhide) Commands

#### Add Repository (Enable Repository)

```bash
sudo dnf copr enable -y universish/Vikunja..

```

#### Installing Software (Install Packages)

To install all packages (`vikunja`, `vikunja-desktop`, `veans`) together or individually:

```bash
# To install all packages:
sudo dnf install -y vikunja vikunja-desktop veans

# To install only the desktop client:
sudo dnf install -y vikunja-desktop

# To install only the Vikunja server:
sudo dnf install -y vikunja

# To install only the Veans CLI tool:
sudo dnf install -y veans

```

#### Package Update and Metadata Cache Bypass (Bypass Metadata Cache & Upgrade)

To bypass local metadata caching and immediately pull new builds or packaging revisions (`vikunja-v<version>-<package-number>`):

```bash
sudo dnf upgrade --refresh -y vikunja vikunja-desktop veans

```

If package metadata does not resolve immediately:

```bash
sudo dnf clean all && sudo dnf makecache
sudo dnf install -y vikunja vikunja-desktop veans
# or to upgrade installed packages to the latest package version:
sudo dnf distro-sync --refresh -y vikunja vikunja-desktop veans

```

#### Uninstalling Software (Uninstall Packages)

```bash
sudo dnf remove -y vikunja vikunja-desktop veans

```

#### Disabling and Removing the Repository

```bash
# To temporarily disable the repository:
sudo dnf copr disable universish/Vikunja..

# To completely remove the repository from the system:
sudo dnf copr remove universish/Vikunja..

```

### 2. openSUSE (Tumbleweed & Leap 16.0) Commands

#### Adding the Repository (Add Repository)

**For openSUSE Tumbleweed (`x86_64` & `aarch64`):**

```bash
sudo zypper addrepo -f https://copr.fedorainfracloud.org/coprs/universish/Vikunja../repo/opensuse-tumbleweed/universish-Vikunja..-opensuse-tumbleweed.repo
sudo zypper --gpg-auto-import-keys refresh

```

**For openSUSE Leap 16.0 (`x86_64` & `aarch64`):**

```bash
sudo zypper addrepo -f https://copr.fedorainfracloud.org/coprs/universish/Vikunja../repo/opensuse-leap-16.0/universish-Vikunja..-opensuse-leap-16.0.repo
sudo zypper --gpg-auto-import-keys refresh

```

#### Installing Software (Install Packages)

```bash
# To install all packages:
sudo zypper install -y vikunja vikunja-desktop veans

# To install only the desktop client:
sudo zypper install -y vikunja-desktop

# To install only the Vikunja server:
sudo zypper install -y vikunja

# To install only the Veans CLI tool:
sudo zypper install -y veans

```

#### Bypassing the Metadata Cache and Updating Packages

To bypass local metadata caching and immediately pull new builds or packaging revisions (`vikunja-v<version>-<package-number>`):

```bash
sudo zypper refresh -f && sudo zypper update -y vikunja vikunja-desktop veans

```

If package metadata does not resolve immediately:

```bash
sudo zypper clean --all && sudo zypper --gpg-auto-import-keys refresh -f
sudo zypper install -y vikunja vikunja-desktop veans

```

#### Uninstalling Packages

```bash
sudo zypper remove -y vikunja vikunja-desktop veans

```

#### Disabling and Removing the Repository

```bash
# To temporarily disable the repository:
sudo zypper modifyrepo -d copr:copr.fedorainfracloud.org:universish:Vikunja..

# To completely remove the repository from the system:
sudo zypper removerepo copr:copr.fedorainfracloud.org:universish:Vikunja..

```

## Podman Container Installation (Fedora & openSUSE)

If you want to run the Vikunja server as an isolated **Podman** container instead of an RPM package, you can follow the steps below directly on Fedora and openSUSE.

### 1. Podman Installation

**On Fedora:**
```bash
sudo dnf install -y podman

```

**On openSUSE (Tumbleweed / Leap 16.0):**
```bash
sudo zypper install -y podman

```

### 2. Preparing Data and Database Directories (Rootless Podman + SELinux-Compatible)

The Vikunja container runs with UID `1000` by default. To avoid SELinux permission issues on Fedora and openSUSE, use the `:Z` flag and the `podman unshare` command:

```bash
mkdir -p ~/vikunja-container/files ~/vikunja-container/db
cd ~/vikunja-container

# Assign directory ownership to UID 1000 in the Rootless Podman namespace:
podman unshare chown -R 1000:1000 ./files ./db

```

### 3. Running the Vikunja Container

```bash
podman run -d \
  --name vikunja \
  -p 3456:3456 \
  -e VIKUNJA_SERVICE_PUBLICURL="http://localhost:3456/" \
  -v ~/vikunja-container/files:/app/vikunja/files:Z \
  -v ~/vikunja-container/db:/db:Z \
  --restart unless-stopped \
  docker.io/vikunja/vikunja:latest

```

* You can access the Vikunja interface by going to `http://localhost:3456` in your browser.
* If you want to verify the image signature (`cosign`):

  ```bash
  cosign verify docker.io/vikunja/vikunja:latest \
    --certificate-oidc-issuer https://token.actions.githubusercontent.com \
    --certificate-identity-regexp ‘^https://github.com/go-vikunja/vikunja/\.github/workflows/release\.yml@refs/tags/v’

  ```

### 4. Automatic Startup with Systemd Quadlet (Fedora & openSUSE)

To have the container start and update automatically at system boot, you can create a Podman Quadlet (`~/.config/containers/systemd/vikunja.container`):

```bash
mkdir -p ~/.config/containers/systemd
```

```
cat << ‘EOF’ > ~/.config/containers/systemd/vikunja.container
[Unit]
Description=Vikunja Task Manager Podman Container
After=network-online.target
Wants=network-online.target

[Container]
Image=docker.io/vikunja/vikunja:latest
ContainerName=vikunja
AutoUpdate=registry
PublishPort=3456:3456
Environment=VIKUNJA_SERVICE_PUBLICURL=http://localhost:3456/
Volume=%h/vikunja-container/files:/app/vikunja/files:Z
Volume=%h/vikunja-container/db:/db:Z

[Service]
Restart=always
TimeoutStartSec=300

[Install]
WantedBy=default.target
EOF
```
```
systemctl --user daemon-reload
systemctl --user enable --now vikunja.service
sudo loginctl enable-linger “$USER”

```



## Directory and File Structure (Repository Directory and File Structure)



```text

Vikunja..Copr..CI/
├── .github/
│   └── workflows/
│       └── vikunja-copr-ci.yml      # 3-stage automated GitHub Actions workflow (twice daily, Lübeck time)
├── scripts/
│   └── repackage_and_publish.sh     # Script that downloads 7 RPM files, extracts them using rpm2cpio, generates an SRPM with an incremented package number, and uploads it to Copr
├── specs/
│   ├── vikunja.spec                 # Vikunja Server/API RPM spec template (x86_64, aarch64, armv7)
│   ├── vikunja-desktop.spec         # Vikunja Desktop RPM spec template (Vikunja Desktop-vX.Y.Z.rpm)
│   └── veans.spec                   # Veans CLI RPM spec template (x86_64, aarch64, armv7)
├── LAST_VERSION                     # Status file containing the version number (X.Y.Z) of the most recently packaged Vikunja release
├── RELEASE_NUMBER                   # RPM packaging number that increments by +1 after each build (vikunja-vX.Y.Z-<RELEASE_NUMBER>)
└── README.md                        # Repository documentation, Fedora/openSUSE installation, and Podman guide

```

| File Path in Repository | Description |
| :--- | :--- |
| `.github/workflows/vikunja-copr-ci.yml` | A 3-stage GitHub Actions workflow running twice daily (Lübeck time) |
| `scripts/repackage_and_publish.sh` | Script to download RPMs, extract them using `rpm2cpio`, generate an SRPM with a package number incremented by `+1`, and publish to Copr |
| `specs/vikunja.spec` | `vikunja` server/API RPM `.spec` file (`x86_64`, `aarch64`, `armv7`) |
| `specs/vikunja-desktop.spec` | `vikunja-desktop` client RPM `.spec` file (`Vikunja Desktop-vX.Y.Z.rpm`) |
| `specs/veans.spec` | `veans` CLI tool RPM `.spec` file (`x86_64`, `aarch64`, `armv7`) |
| `LAST_VERSION` | Status file tracking the latest released version number (`0.0.0` on first installation) |
| `RELEASE_NUMBER` | Package revision number automatically incremented by `+1` after each build (`0` on first installation) |

## Workflow Stages and Automatic Package Number Increment (+1) Logic

1. **Stage 1 (`stage1_github_releases`)**:
   - Runs twice daily based on Lübeck, Germany (`Europe/Berlin`) time (**11:00 UTC** at lunchtime and **16:00 UTC** at the end of the workday).
   - Searches for the following 7 files at [`go-vikunja/vikunja/releases`](https://github.com/go-vikunja/vikunja/releases):
     - `Vikunja Desktop-vX.Y.Z.rpm`
     - `vikunja-vX.Y.Z-x86_64.rpm`
     - `vikunja-vX.Y.Z-armv7.rpm`
     - `vikunja-vX.Y.Z-aarch64.rpm`
     - `veans-vX.Y.Z-x86_64.rpm`
     - `veans-vX.Y.Z-armv7.rpm`
     - `veans-vX.Y.Z-aarch64.rpm`
   - If the new update and files are verified, **skip step 2 and proceed directly to step 3**. If they are not verified, **proceed to step 2**.

2. **Stage 2 (`stage2_dl_vikunja`)**:
   - This stage is triggered only if a new update was not verified in Stage 1.
   - `https://dl.vikunja.io/desktop/vX. Y.Z/Vikunja%20Desktop-vX.Y.Z.rpm` (e.g., `https://dl.vikunja.io/desktop/v2.7.0/Vikunja%20Desktop-v2.7.0.rpm` → `Vikunja Desktop-v2.7.0.rpm`).
   - If the new version is validated, it **proceeds to stage 3**.
  
3. **Stage 3 (`stage3_repackage_and_publish`)**:
   - Reads the value in the `RELEASE_NUMBER` file and **increment it by 1** (`NEXT_RELEASE = CURRENT_RELEASE + 1`). This results in a package name of `vikunja-v<version>-<package-number>` (for example, `vikunja-2.7.0-1`; in the next repackaging, `vikunja-2.7.0-2`), ensuring that when a potential repackaging error is fixed, `dnf upgrade --refresh` / `zypper update` will retrieve the new package without issues.
   - It downloads the upstream `.rpm` packages inside the Fedora container and extracts them using `rpm2cpio | cpio -idmv`.
   - It repackages them as `.src.rpm` (SRPM) files using the `specs/*.spec` files and pushes them to the [`universish/Vikunja..`](https://copr.fedorainfracloud.org/coprs/universish/Vikunja../) repository using `copr-cli`.
   - Commits the updated `LAST_VERSION` and `RELEASE_NUMBER` files to the repository.

----
----

Bu depo ([`universish/Vikunja..Copr..CI`](https://github.com/universish/Vikunja..Copr..CI)), [`go-vikunja/vikunja`](https://github.com/go-vikunja/vikunja/releases) ve [`dl.vikunja.io`](https://dl.vikunja.io/desktop/) kaynaklarını günde iki kez (Vikunja merkezi olan **Lübeck, Almanya** saatiyle öğle arasında ve iş çıkışında) otomatik olarak tarayarak **Vikunja Desktop** (`vikunja-desktop`), **Vikunja Server** (`vikunja`) ve **Veans CLI** (`veans`) RPM paketlerini yeniden paketler ve [`universish/Vikunja..` Fedora Copr](https://copr.fedorainfracloud.org/coprs/universish/Vikunja../) deposunda yayınlar.

Her paketleme işleminden sonra RPM paket numarası (`Release`) otomatik olarak **+1 artırılır** (`vikunja-v<sürüm>-<paket-numarası>`). Bu sayede aynı sürüm üzerinde bir paketleme hatası düzeltilip yeniden derleme alındığında `dnf` ve `zypper` yeni paketi anında güncelleme olarak algılar.

## Vikunja Hakkında

### Gerçekten size ait olan görev yöneticisi.

**Vikunja**, listeler, Kanban, Gantt ve daha fazlasını içeren açık kaynaklı bir görev yönetim sistemidir. Kendiniz barındırın ya da sizin için bizim barındırmamıza izin verin.
*AB'de geliştirilmiş ve barındırılmaktadır. Güneşli bir günde bir tembel hayvanın zarafetiyle plan yapın.*

* **Verileriniz, sunucunuz:** Vikunja'yı kendi altyapınızda çalıştırın. Görevleriniz, projeleriniz, kurallarınız. AGPLv3 lisansı altında açık kaynaklıdır — kodun her satırını okuyabilirsiniz.
* **Ekibinizle birlikte büyür:** Kişisel yapılacaklar listenizle başlayın. Ekibinizin de buna ihtiyacı olduğunda, farklı bir araca geçmeden projeleri paylaşın, görevleri atayın ve işbirliği yapın.
* **Liste, Kanban, Gantt, Tablo:** Görevlerinizi görüntülemek için dört farklı yol. Beyninizin çalışma şekline en uygun olanı kullanın — ya da ihtiyaç duyduğunuzda görünümler arasında geçiş yapın.
* **Yerleşik Taşıma Desteği:** Vikunja, Todoist, Trello, Microsoft To-Do ve diğer platformlar için yerleşik taşıma desteğine sahiptir. Mevcut görevlerinizi ve projelerinizi doğrudan Vikunja arayüzünden içe aktarabilirsiniz.

> "Daha düzenli olmak zor. Vikunja’yı geliştirdim çünkü istediğim şeyi yapabilecek iyi bir açık kaynaklı araç yoktu. Gizlilik önemlidir. Bana göre, sık kullandığınız bir yazılımın koduna göz atabilmelisiniz. Özellikle de günlük olarak kullandığınız bir yapılacaklar listesi uygulaması gibi bir şeyse.
>
> Vikunja Cloud, projenin devamlılığını sağlamak ve kendi kendini sürdürebilir hale getirmek için benim için en iyi yol. Tamamen kendi imkanlarımızla geliştirildiğinden, önceliğimiz risk sermayesi şirketleri değil, yazılımın kullanıcılarıdır."
>
> — **Konrad**, Vikunja Kurucusu

Vikunja, açık kaynaklı ve kendi sunucunuzda barındırabileceğiniz bir yapılacaklar listesi uygulamasıdır. Liste, kanban, gantt ve tablo görünümleri gibi özelliklerle görevlerinizi ve projelerinizi düzenlemenize yardımcı olur; tüm bunlar olurken verileriniz de tamamen sizin kontrolünüz altında kalır.

Vikunja, AGPLv3 lisansı altında dağıtılır ve kendi sunucunuzda barındırmak tamamen ücretsizdir. Kendi sunucunuzu yönetmek istemiyorsanız, [Vikunja Cloud](https://app.vikunja.cloud/?redirectToProvider=true) ücretli bir barındırma seçeneği sunar. Vikunja'yı Docker/Podman, platformunuza özel yerel ikili dosyalar/paketler kullanarak yükleyebilir veya [Vikunja Cloud](https://app.vikunja.cloud/?redirectToProvider=true) hizmetine kaydolabilirsiniz. Kılavuzlu kurulum için [kurulum sihirbazını](https://vikunja.io/install) kullanın. Kendi sunucunuzda barındırma harika bir seçenek olsa da, Vikunja Cloud size otomatik güncellemeler, yedeklemeler ve sıfır bakım gerektiren, tam olarak yönetilen bir örnek sunar. Bu, kullanmaya başlamanın en kolay yoludur ve Vikunja'nın sürekli geliştirilmesini doğrudan destekler.

## Desteklenen Dağıtımlar ve İşlemci Mimarileri (Chroots)

| Dağıtım | `x86_64` Chroot | `aarch64` Chroot |
| :--- | :--- | :--- |
| **Fedora Rawhide** | `fedora-rawhide-x86_64` | `fedora-rawhide-aarch64` |
| **Fedora 45** | `fedora-45-x86_64` | `fedora-45-aarch64` |
| **Fedora 44** | `fedora-44-x86_64` | `fedora-44-aarch64` |
| **openSUSE Tumbleweed** | `opensuse-tumbleweed-x86_64` | `opensuse-tumbleweed-aarch64` |
| **openSUSE Leap 16.0** | `opensuse-leap-16.0-x86_64` | `opensuse-leap-16.0-aarch64` |

## Kurulum, Güncelleme ve Kaldırma Komutları (Fedora & openSUSE)

### 1. Fedora (44, 45, Rawhide) Komutları

#### Depoyu Ekleme (Enable Repository)
```bash
sudo dnf copr enable -y universish/Vikunja..
```

#### Yazılımların Kurulumu (Install Packages)
Tüm paketleri (`vikunja`, `vikunja-desktop`, `veans`) birlikte veya tek tek kurmak için:
```bash
# Tüm paketleri kurmak için:
sudo dnf install -y vikunja vikunja-desktop veans

# Yalnızca masaüstü istemcisini kurmak için:
sudo dnf install -y vikunja-desktop

# Yalnızca Vikunja sunucusunu kurmak için:
sudo dnf install -y vikunja

# Yalnızca Veans CLI aracını kurmak için:
sudo dnf install -y veans
```

#### Paket Güncelleme ve Önbellek Aşma (Bypass Metadata Cache & Upgrade)
To bypass local metadata caching and immediately pull new builds or packaging revisions (`vikunja-v<sürüm>-<paket-numarası>`):
```bash
sudo dnf upgrade --refresh -y vikunja vikunja-desktop veans
```

If package metadata does not resolve immediately:
```bash
sudo dnf clean all && sudo dnf makecache
sudo dnf install -y vikunja vikunja-desktop veans
# veya kurulu paketleri en son paketleme numarasına yükseltmek için:
sudo dnf distro-sync --refresh -y vikunja vikunja-desktop veans
```

#### Yazılımları Silme (Uninstall Packages)
```bash
sudo dnf remove -y vikunja vikunja-desktop veans
```

#### Depoyu Devre Dışı Bırakma ve Silme (Disable & Remove Repository)
```bash
# Depoyu geçici olarak devre dışı bırakmak için:
sudo dnf copr disable universish/Vikunja..

# Depoyu sistemden tamamen silmek için:
sudo dnf copr remove universish/Vikunja..
```

### 2. openSUSE (Tumbleweed & Leap 16.0) Komutları

#### Depoyu Ekleme (Add Repository)
**openSUSE Tumbleweed (`x86_64` & `aarch64`) için:**
```bash
sudo zypper addrepo -f https://copr.fedorainfracloud.org/coprs/universish/Vikunja../repo/opensuse-tumbleweed/universish-Vikunja..-opensuse-tumbleweed.repo
sudo zypper --gpg-auto-import-keys refresh
```

**openSUSE Leap 16.0 (`x86_64` & `aarch64`) için:**
```bash
sudo zypper addrepo -f https://copr.fedorainfracloud.org/coprs/universish/Vikunja../repo/opensuse-leap-16.0/universish-Vikunja..-opensuse-leap-16.0.repo
sudo zypper --gpg-auto-import-keys refresh
```

#### Yazılımların Kurulumu (Install Packages)
```bash
# Tüm paketleri kurmak için:
sudo zypper install -y vikunja vikunja-desktop veans

# Yalnızca masaüstü istemcisini kurmak için:
sudo zypper install -y vikunja-desktop

# Yalnızca Vikunja sunucusunu kurmak için:
sudo zypper install -y vikunja

# Yalnızca Veans CLI aracını kurmak için:
sudo zypper install -y veans
```

#### Paket Güncelleme ve Önbellek Aşma (Bypass Metadata Cache & Update)
To bypass local metadata caching and immediately pull new builds or packaging revisions (`vikunja-v<sürüm>-<paket-numarası>`):
```bash
sudo zypper refresh -f && sudo zypper update -y vikunja vikunja-desktop veans
```

If package metadata does not resolve immediately:
```bash
sudo zypper clean --all && sudo zypper --gpg-auto-import-keys refresh -f
sudo zypper install -y vikunja vikunja-desktop veans
```

#### Yazılımları Silme (Uninstall Packages)
```bash
sudo zypper remove -y vikunja vikunja-desktop veans
```

#### Depoyu Devre Dışı Bırakma ve Silme (Disable & Remove Repository)
```bash
# Depoyu geçici olarak devre dışı bırakmak için:
sudo zypper modifyrepo -d copr:copr.fedorainfracloud.org:universish:Vikunja..

# Depoyu sistemden tamamen silmek için:
sudo zypper removerepo copr:copr.fedorainfracloud.org:universish:Vikunja..
```

## Podman Konteyner Kurulumu (Fedora & openSUSE)

Vikunja sunucusunu RPM paketi yerine izole bir **Podman** konteyneri olarak çalıştırmak isterseniz aşağıdaki adımları Fedora ve openSUSE üzerinde doğrudan uygulayabilirsiniz.

### 1. Podman Kurulumu

**Fedora üzerinde:**
```bash
sudo dnf install -y podman
```

**openSUSE (Tumbleweed / Leap 16.0) üzerinde:**
```bash
sudo zypper install -y podman
```

### 2. Veri ve Veritabanı Dizinlerini Hazırlama (Rootless Podman + SELinux Uyumlu)

Vikunja konteyneri varsayılan olarak `1000` UID'si ile çalışır. Fedora ve openSUSE üzerinde SELinux izin sorunları yaşamamak için `:Z` bayrağını ve `podman unshare` komutunu kullanın:

```bash
mkdir -p ~/vikunja-container/files ~/vikunja-container/db
cd ~/vikunja-container

# Rootless Podman isim alanında dizin sahipliğini UID 1000'e ata:
podman unshare chown -R 1000:1000 ./files ./db
```

### 3. Vikunja Konteynerini Çalıştırma

```bash
podman run -d \
  --name vikunja \
  -p 3456:3456 \
  -e VIKUNJA_SERVICE_PUBLICURL="http://localhost:3456/" \
  -v ~/vikunja-container/files:/app/vikunja/files:Z \
  -v ~/vikunja-container/db:/db:Z \
  --restart unless-stopped \
  docker.io/vikunja/vikunja:latest
```

* Tarayıcınızdan `http://localhost:3456` adresine giderek Vikunja arayüzüne erişebilirsiniz.
* İmaj imzasını doğrulamak isterseniz (`cosign`):
  ```bash
  cosign verify docker.io/vikunja/vikunja:latest \
    --certificate-oidc-issuer https://token.actions.githubusercontent.com \
    --certificate-identity-regexp '^https://github.com/go-vikunja/vikunja/\.github/workflows/release\.yml@refs/tags/v'
  ```

### 4. Systemd Quadlet ile Başlangıçta Otomatik Çalıştırma (Fedora & openSUSE)

Konteynerin sistem açılışında otomatik başlaması ve güncellenmesi için Podman Quadlet (`~/.config/containers/systemd/vikunja.container`) oluşturabilirsiniz:

```bash
mkdir -p ~/.config/containers/systemd

cat << 'EOF' > ~/.config/containers/systemd/vikunja.container
[Unit]
Description=Vikunja Task Manager Podman Container
After=network-online.target
Wants=network-online.target

[Container]
Image=docker.io/vikunja/vikunja:latest
ContainerName=vikunja
AutoUpdate=registry
PublishPort=3456:3456
Environment=VIKUNJA_SERVICE_PUBLICURL=http://localhost:3456/
Volume=%h/vikunja-container/files:/app/vikunja/files:Z
Volume=%h/vikunja-container/db:/db:Z

[Service]
Restart=always
TimeoutStartSec=300

[Install]
WantedBy=default.target
EOF

systemctl --user daemon-reload
systemctl --user enable --now vikunja.service
sudo loginctl enable-linger "$USER"
```

## Directory and File Structure (Depo Dizin ve Dosya Yapısı)

```text
Vikunja..Copr..CI/
├── .github/
│   └── workflows/
│       └── vikunja-copr-ci.yml      # 3 aşamalı otomatik GitHub Actions iş akışı (Lübeck saatiyle günde 2 kez)
├── scripts/
│   └── repackage_and_publish.sh     # 7 RPM dosyasını indiren, rpm2cpio ile açan, +1 paket numarasıyla SRPM üreten ve Copr'a yükleyen betik
├── specs/
│   ├── vikunja.spec                 # Vikunja Server/API RPM spec şablonu (x86_64, aarch64, armv7)
│   ├── vikunja-desktop.spec         # Vikunja Desktop RPM spec şablonu (Vikunja Desktop-vX.Y.Z.rpm)
│   └── veans.spec                   # Veans CLI RPM spec şablonu (x86_64, aarch64, armv7)
├── LAST_VERSION                     # Son paketlenen Vikunja sürüm numarasını (X.Y.Z) tutan durum dosyası
├── RELEASE_NUMBER                   # Her paketlemeden sonra +1 artan RPM paketleme numarası (vikunja-vX.Y.Z-<RELEASE_NUMBER>)
└── README.md                        # Depo dokümantasyonu, Fedora/openSUSE kurulum ve Podman kılavuzu
```

| Depo İçi Dosya Yolu | Açıklama |
| :--- | :--- |
| `.github/workflows/vikunja-copr-ci.yml` | Lübeck saatiyle günde 2 kez çalışan 3 aşamalı GitHub Actions iş akışı |
| `scripts/repackage_and_publish.sh` | RPM indirme, `rpm2cpio` ile açma, `+1` paket numarası ile SRPM üretme ve Copr yayınlama betiği |
| `specs/vikunja.spec` | `vikunja` sunucu/API RPM `.spec` dosyası (`x86_64`, `aarch64`, `armv7`) |
| `specs/vikunja-desktop.spec` | `vikunja-desktop` istemci RPM `.spec` dosyası (`Vikunja Desktop-vX.Y.Z.rpm`) |
| `specs/veans.spec` | `veans` CLI aracı RPM `.spec` dosyası (`x86_64`, `aarch64`, `armv7`) |
| `LAST_VERSION` | Son yayınlanan sürüm numarasını takip eden durum dosyası (ilk kurulumda `0.0.0`) |
| `RELEASE_NUMBER` | Her paketlemeden sonra otomatik `+1` artırılan paket revizyon numarası (ilk kurulumda `0`) |

## İş Akışı Aşamaları ve Otomatik Paket Numarası (+1) Mantığı

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
   - `RELEASE_NUMBER` dosyasındaki değeri okuyup **+1 artırır** (`NEXT_RELEASE = CURRENT_RELEASE + 1`). Böylece paket adı `vikunja-v<sürüm>-<paket-numarası>` (örneğin `vikunja-2.7.0-1`, sonraki paketlemede `vikunja-2.7.0-2`) olur ve olası bir paketleme hatası düzeltildiğinde `dnf upgrade --refresh` / `zypper update` yeni paketi sorunsuz çeker.
   - Fedora konteyneri içinde upstream `.rpm` paketlerini indirir ve `rpm2cpio | cpio -idmv` ile açar.
   - `specs/*.spec` dosyalarıyla `.src.rpm` (SRPM) olarak yeniden paketler ve `copr-cli` ile [`universish/Vikunja..`](https://copr.fedorainfracloud.org/coprs/universish/Vikunja../) deposuna gönderir.
   - Güncellenen `LAST_VERSION` ve `RELEASE_NUMBER` dosyalarını depoya commit eder.



