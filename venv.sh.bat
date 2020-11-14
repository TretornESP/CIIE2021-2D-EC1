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

set -e

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
        . /etc/os-release
        OS=$NAME
        VER=$VERSION_ID
    elif type lsb_release >/dev/null 2>&1; then
        OS=$(lsb_release -si)
        VER=$(lsb_release -sr)
    elif [ -f /etc/lsb-release ]; then
        . /etc/lsb-release
        OS=$DISTRIB_ID
        VER=$DISTRIB_RELEASE
    elif [ -f /etc/debian_version ]; then
        OS=Debian
        VER=$(cat /etc/debian_version)
    elif [ -f /etc/SuSe-release ]; then
        OS="Suse"
    elif [ -f /etc/redhat-release ]; then
        OS="Red Hat Old"
    else
        OS=$(uname -s)
        VER=$(uname -r)
    fi

    echo "LOL $OS"

    if [ "$OS" = "Arch Linux" ]; then
        echo "Arch Linux detected"

        while true; do
            stty echo
            printf "Update repos? [y/n] "
            read yn
            stty echo
            case $yn in
                [Yy]* ) sudo pacman -Syy; break;;
                [Nn]* ) break;;
                * ) echo "Please answer yes or no.";;
            esac
        done

        while true; do
            stty echo
            printf "Install dependencies? [y/n] "
            read yn
            stty echo
            case $yn in
                [Yy]* ) sudo pacman -S python-pygame --needed; break;;
                [Nn]* ) break;;
                * ) echo "Please answer yes or no.";;
            esac
        done
    elif [ "$OS" = "Ubuntu" ]; then
        echo "Ubuntu detected"

        while true; do
            stty echo
            printf "Update repos? [y/n] "
            read yn
            stty echo
            case $yn in
                [Yy]* ) sudo apt-get update; break;;
                [Nn]* ) break;;
                * ) echo "Please answer yes or no.";;
            esac
        done

        while true; do
            stty echo
            printf "Install dependencies? [y/n] "
            read yn
            stty echo
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
    pip install wheel
    pip install -r requirements.txt
fi

echo "******************************************************************"
echo "* You have just succesfully configured your virtual environment! *"
echo "* To play the game just type ./main.py                           *"
echo "* When you are done playing, just close the terminal or type     *"
echo "* \"deactivate\" to exit the virtual environment.                *"
echo "*                                                                *"
echo "*    Have fun and stay safe!                                     *"
echo "******************************************************************"

# bash stuff
return # Exit script on *NIX






: # WINDOWS CMD SCRIPT # : [cosas de xabi]

:WINDOWS
virtualenv test
call .\test\Scripts\activate
pip install pygame
pip install -r requirements.txt
python main.py