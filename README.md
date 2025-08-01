# Bauti's dotfiles (test)
Minimal & functional Hyprland setup on Arch Linux. Focused on simplicity, performance, and clean aesthetics.

## 📦 Required Packages

Make sure to install these packages before applying the dotfiles:

```bash
# Base system
sudo pacman -S git stow zsh base-devel

# Wayland core
sudo pacman -S hyprland hyprpaper wl-clipboard xdg-desktop-portal-hyprland \
               xdg-desktop-portal-gtk qt5-wayland qt6-wayland gtk3 gtk4

# Tools & UI
sudo pacman -S kitty dolphin rofi waybar swww brightnessctl dunst \
               network-manager-applet pavucontrol polkit-kde-agent grim slurp

# Audio
sudo pacman -S pipewire pipewire-audio pipewire-pulse pipewire-alsa wireplumber \
               alsa-utils

# Optional extras
sudo pacman -S neofetch btop unzip noto-fonts noto-fonts-emoji ttf-jetbrains-mono-nerd