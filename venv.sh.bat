: # This is a special script which intermixes both sh
: # and cmd code. It is written this way because it is
: # used in system() shell-outs directly in otherwise
: # portable code.
: # Script by Alonso Rodriguez. CHS 1920.

:; if [ -z 0 ]; then
  @echo off
  goto :WINDOWS
fi


: # UNIX SHELL SCRIPT # :

#!/usr/bin/env sh

sourced=0
if [ -n "$ZSH_EVAL_CONTEXT" ]; then 
  case $ZSH_EVAL_CONTEXT in *:file) sourced=1;; esac
elif [ -n "$KSH_VERSION" ]; then
  [ "$(cd $(dirname -- $0) && pwd -P)/$(basename -- $0)" != "$(cd $(dirname -- ${.sh.file}) && pwd -P)/$(basename -- ${.sh.file})" ] && sourced=1
elif [ -n "$BASH_VERSION" ]; then
  (return 0 2>/dev/null) && sourced=1 
else # All other shells: examine $0 for known shell binary filenames
  # Detects `sh` and `dash`; add additional shell filenames as needed.
  case ${0##*/} in sh|dash) sourced=1;; esac
fi

if [ "$sourced" -eq "0" ]; then
    echo "ERROR, THE SCRIPT IS NOT SOURCED. YOU MUST EXECUTE:"
    echo "  source ./venv.sh.bat"
    echo
    exit
fi


# Else, if everything succeeded
echo "Initializing venv..."

set -e # exit on error

postinstall=0
if [ ! -f "./bin/activate" ]; then
    echo "Setting up venv for the first time!"
    python3 -m venv .
    postinstall=1
fi

echo "source ./bin/activate"
source ./bin/activate

if [ "$postinstall" -eq "1" ]; then
    echo "Installing python requirements!"

    if [ -f /etc/os-release ]; then
        # freedesktop.org and systemd
        . /etc/os-release
        OS=$NAME
        VER=$VERSION_ID
    elif type lsb_release >/dev/null 2>&1; then
        # linuxbase.org
        OS=$(lsb_release -si)
        VER=$(lsb_release -sr)
    elif [ -f /etc/lsb-release ]; then
        # For some versions of Debian/Ubuntu without lsb_release command
        . /etc/lsb-release
        OS=$DISTRIB_ID
        VER=$DISTRIB_RELEASE
    elif [ -f /etc/debian_version ]; then
        # Older Debian/Ubuntu/etc.
        OS=Debian
        VER=$(cat /etc/debian_version)
    elif [ -f /etc/SuSe-release ]; then
        # Older SuSE/etc.
        #...
        OS="Suse"
    elif [ -f /etc/redhat-release ]; then
        # Older Red Hat, CentOS, etc.
        #...
        OS="Red Hat Old"
    else
        # Fall back to uname, e.g. "Linux <version>", also works for BSD, etc.
        OS=$(uname -s)
        VER=$(uname -r)
    fi

    echo "LOL $OS"

    if [ "$OS" = "Arch Linux" ]; then
        echo "Arch Linux detected"

        while true; do
            read -p "Update repos? [y/n]" yn
            case $yn in
                [Yy]* ) sudo pacman -Syy; break;;
                [Nn]* ) break;;
                * ) echo "Please answer yes or no.";;
            esac
        done

        while true; do
            read -p "Install dependencies? [y/n]" yn
            case $yn in
                [Yy]* ) sudo pacman -S python-pygame --needed; break;;
                [Nn]* ) break;;
                * ) echo "Please answer yes or no.";;
            esac
        done
    elif [ "$OS" = "Ubuntu" ]; then
        echo "Ubuntu detected"

        while true; do
            read -p "Update repos? [y/n]" yn
            case $yn in
                [Yy]* ) sudo apt-get update; break;;
                [Nn]* ) break;;
                * ) echo "Please answer yes or no.";;
            esac
        done

        while true; do
            read -p "Install dependencies? [y/n]" yn
            case $yn in
                [Yy]* ) sudo apt-get install python3-pygame; break;;
                [Nn]* ) break;;
                * ) echo "Please answer yes or no.";;
            esac
        done
    else
        echo "Unsupported distribution detected. Please contact developer team"
    fi
    
    # Finally configure venv
    pip install -r requirements.txt
fi

# bash stuff
return # Exis script on *NIX






: # WINDOWS CMD SCRIPT # : [cosas de xabi]

:WINDOWS

@echo off

echo "NOT IMPLEMENTED" || goto :EOF

python -m venv "%~dp0" || goto :error
:: ni idea de como se continua lol

:error
exit /b %errorlevel%
