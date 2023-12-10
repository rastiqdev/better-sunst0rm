#!/bin/bash
trap exit INT

cecho() {
  RED="\033[0;31m"
  GREEN="\033[0;32m"  # <-- [0 means not bold
  YELLOW="\033[0;33m" # <-- [1 means bold
  CYAN="\033[0;36m"
  # ... Add more colors if you like

  NC="\033[0m" # No Color

  # printf "${(P)1}${2} ${NC}\n" # <-- zsh
  printf "${!1}${2} ${NC}\n" # <-- bash
}

error_exit() {
  cecho "RED" "Error: $1"
  exit 1
}

macOSversion=$(sw_vers | head -n2 | tail -n1 | cut -c 17-)
verscheck=$(bc <<<"${macOSversion} < 10.14")

if [ "$(uname)" = "Darwin" ]; then
  cecho "CYAN" "[!] macOS detected!"
  if [[ $(sysctl -n machdep.cpu.brand_string) =~ "Apple" ]]; then
    cecho "CYAN" "[!] Apple Silicon detected"
    OS="macOS-arm64"
  elif [[ $(sysctl -n machdep.cpu.brand_string) =~ "Intel" ]]; then
    cecho "CYAN" "[!] Intel mac detected!"
    OS="macOS-x86_64"
  fi
else
  cecho "RED" "Not running on macOS... exiting..."
  exit 2
fi

if command -v brew >/dev/null; then
  cecho "GREEN" "[!] Homebrew is installed!"
else
  cecho "YELLOW" "[!] Homebrew not found. Install instructions can be found at https://brew.sh"
  exit 3
fi

if ! command -v python3 >/dev/null; then
  cecho "YELLOW" "[!] python3 not found. Installing..."
  $pkg install python3
else
  cecho "GREEN" "[!] python3 is installed!"
fi

if python3 -m pip | grep "No module named pip"; then
  cecho "YELLOW" "[!] pip not found. installing"
  python3 -m ensurepip
else
  cecho "GREEN" "[!] pip is installed!."
fi

if [ "$(python3 -m pip list | grep -c "pyimg4")" == 0 ]; then
  cecho "YELLOW" "[!] pyimg4 not found. Installing..."
  python3 -m pip install pyimg4 || error_exit "[!] pyimg4 failed to install"
else
  cecho "GREEN" "[!] pyimg4 is installed!"
fi

cd bin

chmod 755 *
xattr -dr com.apple.quarantine *

cd ../

cecho "GREEN" "### Dependency installation finished ###"
touch .requirements_done
