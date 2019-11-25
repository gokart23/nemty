# nemty
Welcome to Nemty, a Raspberry Pi 4 running ArchLinux ARM for always-on services! This document lists some of the current ongoing work on the device, and general ways someone interested in a similar setup could get started.

## Init

- [X] Install base OS from [here](https://archlinuxarm.org/platforms/armv6/raspberry-pi).

## Base system

- [X] Setup service user, with appropriate permissions. Disable/restrict defaults.
- [X] Setup wireless access.

The RPi 4 wireless chip (Cyprus) which isn't visible via `lspci` or `lsusb`, but can be checked using `ip link`. [This](https://raspberrypi.stackexchange.com/a/7992) link is useful for setting up the wireless profile. It is also useful to obfuscate the key using a PSK via `wpa_passphrase` (as described [here](https://wiki.archlinux.org/index.php/Netctl#Wireless)). Also recommended is enabling on startup using `netctl enable <profile-name>`.

- [X] Setup auto-mount for data partition.
 
 Check `man 5 fstab`. Simple :)
 
- [ ] Setup keys and email config.
- [ ] Setup crontab with updates and health checks.
- [ ] Setup repo auto-update on change.

## External access

- [ ] Setup restricted external access.
