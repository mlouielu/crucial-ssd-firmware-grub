# Crucial FW

This is a python version that help Linux user to download Curcial SSD firmware
bootable ISO and generate correspond GRUB2 config file.

### How to used

WARNING: You must run as `root`, if you don't trust the script,
read it or don't use.

```sh
$ sudo ./crucial-fw.py
INFO:root:Target: BX200
INFO:root:    [*] Downloading...
INFO:root:    [*] Uncompressing...
INFO:root:    [*] Moving iso to /boot/crucial-fw
INFO:root:    Grub mode:
INFO:root:        initrd
INFO:root:Target: BX100
INFO:root:    [*] Downloading...
INFO:root:    [*] Uncompressing...
INFO:root:    [*] Moving iso to /boot/crucial-fw
INFO:root:    Grub mode:
INFO:root:        initrd
INFO:root:Target: M550
INFO:root:    [*] Downloading...
INFO:root:    [*] Uncompressing...
INFO:root:    [*] Moving iso to /boot/crucial-fw
INFO:root:    Grub mode:
INFO:root:        initrd
INFO:root:Target: M500
INFO:root:    [*] Downloading...
INFO:root:    [*] Uncompressing...
INFO:root:    [*] Moving iso to /boot/crucial-fw
INFO:root:    Grub mode:
INFO:root:        linux16
INFO:root:Target: MX200
INFO:root:    [*] Downloading...
INFO:root:    [*] Uncompressing...
INFO:root:    [*] Moving iso to /boot/crucial-fw
INFO:root:    Grub mode:
INFO:root:        initrd
INFO:root:Target: MX100
INFO:root:    [*] Downloading...
INFO:root:    [*] Uncompressing...
INFO:root:    [*] Moving iso to /boot/crucial-fw
INFO:root:    Grub mode:
INFO:root:        initrd
INFO:root:Target: M4
INFO:root:    [*] Downloading...
INFO:root:    [*] Uncompressing...
INFO:root:    [*] Moving iso to /boot/crucial-fw
INFO:root:    Grub mode:
INFO:root:        linux16
INFO:root:Target: M4_mSATA
INFO:root:    [*] Downloading...
INFO:root:    [*] Uncompressing...
INFO:root:    [*] Moving iso to /boot/crucial-fw
INFO:root:    Grub mode:
INFO:root:        linux16
INFO:root:Target: C300
INFO:root:    [*] Downloading...
INFO:root:    [*] Uncompressing...
INFO:root:    [*] Moving iso to /boot/crucial-fw
INFO:root:    Grub mode:
INFO:root:        linux16
Generate GRUB rules in: /etc/grub.d/45_crucial_fw
                ISO in: /boot/crucial-fw
Please run "update-grub2" or "grub-mkconfig -o /boot/grub/grub.cfg
to generate new grub file.
And reboot to choose "Crucial Firmware Update in GRUB2.
```

### Config

You can easily config which SSD firmware you need to used by editing
`crucial-fw.cfg`, if you want to add a new firmware, add a newline and split
name and url by tab. If you don want the firmware, simply delete the line or
using `#` to comment out.

### Remove

After upgrading your firmware, you may want to remove the iso and grub file.

Simply remove directory `/boot/crucial-fw` and `/etc/grub.d/45_crucial_fw`,
then regenerate GRUB2 by `update-grub2` or `grub-mkconfig`, well done.

### Thanks

This work is based on [guillaume Update any crucial ssd firmware from linux/grub](http://guillaumeplayground.net/update-crucial-ssd-firmware/)
