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

  Using `auto,nofail,noatime,rw,exec` as the options is recommended in `/etc/fstab`.
- [X] Bind-mount logs (`/var/log`) to external disk.
- [ ] Configure log rotation policy.
- [ ] Setup repo auto-update on change.

## Health checks
- [ ] Temperature check
- [ ] Change all log storage and access to external storage.
- [ ] Change flash mounts to read-only. This is primarily to protect against premature SD card failure, unexpected shutdowns (which can cause arbitrary write failures). This is also long and painful but highly recommended.

Recommended reading is [here](https://k3a.me/how-to-make-raspberrypi-truly-read-only-reliable-and-trouble-free/).

## VPN Access through split tunnel

- [X] Install `openvpn` and setup config (either from 3rd-party VPN client config, or from the default).
- [X] Setup file-based auth pull.

In the client config, in place of `auth-user-pass`, use `auth-user-pass <fname>`, where `<fname>` is a plain text file with 2 lines, the first one being the username and the second the password. Make sure that the running client/group is something that is accessible by the default service user! (This can be easily checked by running `curl --interface tun0 -vvv -4 icanhazip.com` and checking that the call doesn't timeout.)

- [ ] Setup starting as a service.
- [X] Test it out!
- [X] Disable default publishing of gateway redirection rules, and setup routing rules for the TUN interface.

  I found [this](https://superuser.com/questions/1292106/avoid-openvpn-client-to-act-as-default-gateway) link helpful to understand the tunneling setup. Starting the openvpn client shouldn't publish the default gateway override rules anymore. The actual rule itself is `pull-filter ignore redirect-gateway`. However, this doesn't establish the rules needed for routing from/to the TUN interface correctly. As it turns out, this is a little more involved than it appears at first sight, and the following linkes are helpful in figuring out the setup
    * The TUN routing setup as explained [here](https://community.openvpn.net/openvpn/wiki/BridgingAndRouting).
    * Routing with multiple uplinks as explained [here](https://lartc.org/howto/lartc.rpdb.multiple-links.html) for policy-based routing.
    * A setup for routing that worked in my context, as given [here](https://unix.stackexchange.com/a/373987).
    * A more detailed guide to setting it up, as explained [here](http://www.georgiecasey.com/2013/07/26/how-to-use-overplay-and-other-vpns-as-a-curl-proxy/).
    * Cleaning up the `route-up` script, as explained [here](https://forums.openvpn.net/viewtopic.php?t=25256).
  After this reading, the following changes to the config worked for me:
  ```bash
  # openvpn_config.conf
  pull-filter ignore redirect-gateway
  script-security 2
  route-up /etc/openvpn/client/tun0_up.sh
  ``` 
  where the `tun0_up.sh` script essentially sets up the routes as :
  ```bash
   # setup "vpn" routing table beforehand by running echo "1000 vpn" >> /etc/iproute2/rt_tables
   vpn_rt_tablename="vpn"
   tun_device="tun0"
   tun_subnet_range="24"

   tun0_ip_address=$(/usr/bin/ifconfig ${tun_device} | /usr/bin/grep 'inet ' | /usr/bin/awk -F' ' '{print $2}')

   /usr/bin/ip route add default via ${tun0_ip_address} dev ${tun_device} table ${vpn_rt_tablename}
   /usr/bin/ip rule add from ${tun0_ip_address}/${tun_subnet_range} table ${vpn_rt_tablename}
   /usr/bin/ip rule add to ${tun0_ip_address}/${tun_subnet_range} table ${vpn_rt_tablename}
   /usr/bin/ip route flush cache

   exit 0
   ```
  If the configuration works out correctly, `ip route show table vpn` should list the default gateway as the `tun0` IP (`ifconfig tun0 | grep 'inet '`), and `curl --interface tun0 -vvv -4 icanhazip.com` should succeed.
  Also, if running as a `systemd` daemon, the `LimitNPROC` might need to be increased from the default of 10 (in the `systemd` service unit file under `/etc/systemd/system/multi-user.target.wants/openvpn***`) to `infinity` or a number greater than 10.

- [ ] Verify/setup clean up script when route goes down.
- [ ] Setup a new linux network namespace for applications that need to be isolated and need to use the VPN connection.
- [ ] Setup veth pair with one end inside the namespace, and the peer end in the default/global namespace with the physical/TUN intefaces.
- [ ] Setup a linux bridge from the peer veth end to the tun connection.
- [ ] Bind the application to use the newly created network namespace.


## External access

Most of this section is descriptive, please refer to your ToS of your DNS provider and/or cloud provider to ensure you're not in violation of laws.

- [X] Bind IP to the DNS and/or setup reverse tunnel.
- [X] Disable all non-key access.
- [X] Install and configure `ufw`.
- [X] Setup a Telegram bot framework [`rascal`] ([this](https://core.telegram.org/bots/api) link is helpful, and so is the unfortunately-archived pip package [telepot](https://telepot.readthedocs.io/en/latest/) - its insanely easy, and provides a useful way to control/access Nemty)

  [This](https://www.raspberrypi.org/documentation/configuration/security.md) link might be helpful. Don't forget to allow access from the local network!
- [ ] Install and configure `fail2ban`.

## `rascal`: Telegram bot framework

- [X] Setup basic framework, with user-ID-based service denial
- [ ] Setup control, notifications

- [ ] Setup intent identification model
- [ ] Setup basic actions based off of intent identification
- [ ] Setup active learning for improving existing intents

## Pi-hole Wireless AP

- [ ] Setup wireless AP
- [ ] Setup subnet for Nemty-connected devices
- [ ] Setup bridge between wireless interface and internet-connected interface (such as ethernet) for NAT
- [ ] Setup Pi-hole standalone service (via `dnsmasq`)
