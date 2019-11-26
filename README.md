# nemty
Welcome to Nemty, a headless Raspberry Pi 4 running ArchLinux ARM for always-on services! This document lists some of the current ongoing work on the device, and general ways someone interested in a similar setup could get started.

## Init

- [X] Install base OS from [here](https://archlinuxarm.org/platforms/armv6/raspberry-pi).

## Base system

- [X] Setup service user, with appropriate permissions. Remove - or at the _very_ least disable - defaults.
- [X] Setup wireless access.

The RPi 4 wireless chip (Cyprus) which isn't visible via `lspci` or `lsusb`, but can be checked using `ip link`. [This](https://raspberrypi.stackexchange.com/a/7992) link is useful for setting up the wireless profile. It is also useful to obfuscate the key using a PSK via `wpa_passphrase` (as described [here](https://wiki.archlinux.org/index.php/Netctl#Wireless)). Also recommended is enabling on startup using `netctl enable <profile-name>`.

- [X] Setup auto-mount for data partition.
 
 Check `man 5 fstab`. Simple :)
 
- [X] Setup keys and email config.

  For email config, I'd recommend using [msmtp](https://wiki.archlinux.org/index.php/Msmtp#Installing). If  you're using a GMail service account, you might need to set up [app passwords](https://support.google.com/accounts/answer/185833?hl=en).
- [X] Setup crontab with updates.

  I'd recommend using `fcrontab`, and setting up `msmtp` to work with crontab (as shown [here](https://websistent.com/msmtp-cron/)).
  
- [X] Setup external non-flash storage.

  Using `auto,nofail,noatime,rw,user` as the options is recommended in `/etc/fstab`.
- [ ] Setup repo auto-update on change.

## Health checks
- [ ] Temperature check
- [ ] Change all log storage and access to external storage.
- [ ] Change flash mounts to read-only. This is primarily to protect against premature SD card failure, unexpected shutdowns (which can cause arbitrary write failures). This is also long and painful but highly recommended.

Recommended reading is [here](https://k3a.me/how-to-make-raspberrypi-truly-read-only-reliable-and-trouble-free/).

## External access

Most of this section is descriptive, please refer to your ToS of your DNS provider and/or cloud provider to ensure you're not in violation of laws.

- [X] Bind IP to the DNS and/or setup reverse tunnel.
- [ ] Disable all non-key access.
- [ ] Install and configure `ufw`.
- [ ] Install and configure `fail2ban`.
