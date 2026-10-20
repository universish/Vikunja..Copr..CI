%global debug_package %{nil}

Name:           vikunja-webui-pwa
Version:        1.0.0
Release:        1%{?dist}
Summary:        Vikunja WebUI (Smart PWA Launcher)
License:        AGPL-3.0-or-later
URL:            https://vikunja.io
BuildArch:      noarch

Source0:        vikunja.png

Requires:       pciutils
Requires:       xdg-utils
Requires:       hicolor-icon-theme

%description
Smart PWA wrapper for Vikunja Task Management Web UI. Launches the local interface (http://localhost:3456/) as a standalone borderless PWA window in the user's preferred browser, automatically injecting optimal Wayland and GPU acceleration flags without Electron dependencies.

%prep

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_libexecdir}
mkdir -p %{buildroot}%{_datadir}/applications
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/512x512/apps
mkdir -p %{buildroot}%{_datadir}/pixmaps

# 1. AKILLI TARAYICI SARMALAYICISI (İzole PWA Modu Başlatıcısı)
cat << 'EOF' > %{buildroot}%{_libexecdir}/vikunja-browser-wrapper
#!/usr/bin/env bash
URL="$1"
[ -z "$URL" ] && URL="http://localhost:3456/"

PWA_PROFILE_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/vikunja-pwa-profile"
mkdir -p "$PWA_PROFILE_DIR"

# GPU Tespiti ve İzole PWA Chromium Bayrakları
CHROMIUM_FLAGS="--ozone-platform-hint=auto --user-data-dir=$PWA_PROFILE_DIR --class=VikunjaPWA --no-first-run --no-default-browser-check"

if lspci -k 2>/dev/null | grep -iA 2 "VGA" | grep -i "nvidia" > /dev/null; then
    CHROMIUM_FLAGS="$CHROMIUM_FLAGS --disable-features=Vulkan"
else
    CHROMIUM_FLAGS="$CHROMIUM_FLAGS --enable-features=Vulkan"
fi

export MOZ_ENABLE_WAYLAND=1

find_browser_bin() {
    for bin in "$@"; do
        if command -v "$bin" >/dev/null 2>&1; then
            echo "$bin"
            return 0
        fi
    done
    return 1
}

launch_firefox_pwa() {
    local ff_bin="$1"
    local ff_profile="$PWA_PROFILE_DIR/firefox-pwa"
    mkdir -p "$ff_profile/chrome"

    # Firefox/Zen/LibreWolf için adres çubuğu ve sekmeleri gizleyen PWA yapılandırması
    cat << 'USERJS' > "$ff_profile/user.js"
user_pref("toolkit.legacyUserProfileCustomizations.stylesheets", true);
user_pref("browser.tabs.warnOnClose", false);
user_pref("browser.shell.checkDefaultBrowser", false);
USERJS

    cat << 'CSS' > "$ff_profile/chrome/userChrome.css"
#TabsToolbar, #nav-bar, #PersonalToolbar, #sidebar-box, #sidebar-splitter {
    visibility: collapse !important;
}
CSS

    exec "$ff_bin" --profile "$ff_profile" --no-remote --class "VikunjaPWA" --new-window "$URL"
}

DEFAULT_BROWSER=$(xdg-settings get default-web-browser 2>/dev/null || xdg-mime query default x-scheme-handler/http 2>/dev/null)
DEFAULT_BROWSER=$(echo "$DEFAULT_BROWSER" | tr '[:upper:]' '[:lower:]')

# 1. Varsayılan tarayıcıya göre PWA başlat
if [[ "$DEFAULT_BROWSER" == *"helium"* ]] && BIN=$(find_browser_bin helium helium-browser); then
    exec "$BIN" --app="$URL" $CHROMIUM_FLAGS
elif [[ "$DEFAULT_BROWSER" == *"cromite"* ]] && BIN=$(find_browser_bin cromite cromite-browser); then
    exec "$BIN" --app="$URL" $CHROMIUM_FLAGS
elif [[ "$DEFAULT_BROWSER" == *"thorium"* ]] && BIN=$(find_browser_bin thorium-browser thorium); then
    exec "$BIN" --app="$URL" $CHROMIUM_FLAGS
elif [[ "$DEFAULT_BROWSER" == *"brave"* ]] && BIN=$(find_browser_bin brave-browser brave); then
    exec "$BIN" --app="$URL" $CHROMIUM_FLAGS
elif [[ "$DEFAULT_BROWSER" == *"chrome"* ]] && BIN=$(find_browser_bin google-chrome google-chrome-stable); then
    exec "$BIN" --app="$URL" $CHROMIUM_FLAGS
elif [[ "$DEFAULT_BROWSER" == *"chromium"* ]] && BIN=$(find_browser_bin chromium-browser chromium); then
    exec "$BIN" --app="$URL" $CHROMIUM_FLAGS
elif [[ "$DEFAULT_BROWSER" == *"edge"* ]] && BIN=$(find_browser_bin microsoft-edge microsoft-edge-stable); then
    exec "$BIN" --app="$URL" $CHROMIUM_FLAGS
elif [[ "$DEFAULT_BROWSER" == *"vivaldi"* ]] && BIN=$(find_browser_bin vivaldi vivaldi-stable); then
    exec "$BIN" --app="$URL" $CHROMIUM_FLAGS
fi

# 2. Varsayılan tarayıcı Chromium tabanlı değilse bile sistemde yüklü olanları tercih et
if BIN=$(find_browser_bin helium helium-browser cromite thorium-browser thorium brave-browser brave chromium-browser chromium google-chrome google-chrome-stable microsoft-edge vivaldi); then
    exec "$BIN" --app="$URL" $CHROMIUM_FLAGS
fi

# 3. Yalnızca Firefox / Zen / LibreWolf yüklüyse
if BIN=$(find_browser_bin zen zen-browser librewolf firefox); then
    launch_firefox_pwa "$BIN"
fi

exec xdg-open "$URL"
EOF
chmod +x %{buildroot}%{_libexecdir}/vikunja-browser-wrapper

# 2. ANA BAŞLATICI (Doğrudan Vikunja Localhost URL'sini açar)
cat << 'EOF' > %{buildroot}%{_bindir}/vikunja-webui
#!/usr/bin/env bash
TARGET_URL="http://localhost:3456/"
exec %{_libexecdir}/vikunja-browser-wrapper "$TARGET_URL"
EOF
chmod +x %{buildroot}%{_bindir}/vikunja-webui

# 3. MASAÜSTÜ KISAYOLU (.desktop)
cat << 'EOF' > %{buildroot}%{_datadir}/applications/vikunja-webui.desktop
[Desktop Entry]
Name=Vikunja WebUI
Comment=Vikunja Task Management (PWA Mode)
GenericName=Task Manager
Exec=/usr/bin/vikunja-webui
Icon=vikunja-webui
Type=Application
StartupNotify=true
StartupWMClass=VikunjaPWA
Terminal=false
Categories=Office;Utility;Network;
EOF

# 4. İKON DOSYALARI (İkon dosyasının adı repoda vikunja.png olmalıdır)
install -m 0644 %{SOURCE0} %{buildroot}%{_datadir}/icons/hicolor/512x512/apps/vikunja-webui.png
install -m 0644 %{SOURCE0} %{buildroot}%{_datadir}/pixmaps/vikunja-webui.png

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
    %{_bindir}/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi
/usr/bin/update-desktop-database &>/dev/null || :

%postun
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
    %{_bindir}/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi
/usr/bin/update-desktop-database &>/dev/null || :

%files
%{_bindir}/vikunja-webui
%{_libexecdir}/vikunja-browser-wrapper
%{_datadir}/applications/vikunja-webui.desktop
%dir %{_datadir}/icons/hicolor
%dir %{_datadir}/icons/hicolor/512x512
%dir %{_datadir}/icons/hicolor/512x512/apps
%{_datadir}/icons/hicolor/512x512/apps/vikunja-webui.png
%{_datadir}/pixmaps/vikunja-webui.png

%changelog
* Tue Oct 20 2026 Saffet Yavuz <universish@tutamail.com> - 1.0.0-1
- Initial PWA wrapper for Vikunja Task Management.
- Added browser isolation and localhost injection.
