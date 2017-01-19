#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# 2017 Louie Lu <me at louie.lu>
#
# This is free and unencumbered software released into the public domain.
#
# Anyone is free to copy, modify, publish, use, compile, sell, or
# distribute this software, either in source code form or as a compiled
# binary, for any purpose, commercial or non-commercial, and by any
# means.
#
# In jurisdictions that recognize copyright laws, the author or authors
# of this software dedicate any and all copyright interest in the
# software to the public domain. We make this dedication for the benefit
# of the public at large and to the detriment of our heirs and
# successors. We intend this dedication to be an overt act of
# relinquishment in perpetuity of all present and future rights to this
# software under copyright law.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# For more information, please refer to <http://unlicense.org/>
#

import logging
import os
import shutil
import zipfile
import tempfile
import urllib3

CHUNK_SIZE = 2048
CONFIG_FILE = 'crucial-fw.cfg'
GRUB_FILE = '/etc/grub.d/45_crucial_fw'
BOOT_ISO_DIR = '/boot/crucial-fw'
DOWNLOAD_DIR = tempfile.mkdtemp()


def read_config(path):
    f = open(path).readlines()
    f = filter(lambda x: not x.startswith('#'), f)
    f = filter(lambda x: not x.startswith('\n'), f)
    f = filter(lambda x: not x.startswith('\n\r'), f)
    f = list(map(lambda x: x.strip('\n\r').split('\t'), f))

    return f


def open_custom_grub_config():
    f = open(GRUB_FILE, 'w')
    f.write("#!/bin/sh\nexec tail -n +3 $0\nsubmenu 'Crucial Firmware Update'{\n")

    return f


def download_firmware_zip(name, url):
    logging.info('    [*] Downloading...')
    http = urllib3.PoolManager()
    r = http.request('GET', url, preload_content=False)

    path = '%s/%s.zip' % (DOWNLOAD_DIR, name)
    with open(path, 'wb') as f:
        while True:
            data = r.read(CHUNK_SIZE)
            if not data:
                break
            f.write(data)
    r.release_conn()
    return path


def extract_zip_to_iso(path):
    logging.info('    [*] Uncompressing...')
    z = zipfile.ZipFile(path, 'r')

    iso = z.namelist()[0]
    z.extractall(DOWNLOAD_DIR)
    z.close()

    return iso


def move_iso_to_boot(iso):
    logging.info('    [*] Moving iso to %s' % (BOOT_ISO_DIR))
    if not os.path.isdir(BOOT_ISO_DIR):
        os.mkdir(BOOT_ISO_DIR)
    if os.path.isfile('%s/%s' % (BOOT_ISO_DIR, iso)):
        os.remove('%s/%s' % (BOOT_ISO_DIR, iso))

    shutil.move('%s/%s' % (DOWNLOAD_DIR, iso), BOOT_ISO_DIR)


def parse_isolinux_config(path):
    with open('%s/boot/isolinux/isolinux.cfg' % (path)) as f:
        for n in f.readlines():
            if n.startswith('APPEND'):
                return ' '.join(n.strip('\n').split(' ')[1:])

    return ''


def make_grub_menuentry(fgb, name, iso):
    with tempfile.TemporaryDirectory() as mount_dir:
        logging.debug('Mount dir: ', mount_dir)
        logging.info('    Grub mode:')
        os.system('mount -o loop %s/%s %s 2>/dev/null' % (BOOT_ISO_DIR, iso, mount_dir))
        fgb.write(
            '''menuentry "%s FW" {
            insmod loopback
            set isofile="%s/%s"
            search -sf $isofile
            loopback loop $isofile
            ''' % (name, BOOT_ISO_DIR, iso))

        if (os.path.isfile('%s/boot/isolinux/memdisk' % (mount_dir)) and
                os.path.isfile('%s/boot/isolinux/boot2880.img' % (mount_dir))):
            logging.info('        linux16')
            fgb.write(
                '''linux16 (loop)/boot/isolinux/memdisk
                initrd16 (loop)/boot/isolinux/boot2880.img\n''')
        elif (os.path.isfile('%s/boot/vmlinuz' % (mount_dir)) and
                os.path.isfile('%s/boot/core.gz' % (mount_dir))):
            logging.info('        initrd')
            append = parse_isolinux_config(mount_dir)
            fgb.write(
                '''linux (loop)/boot/vmlinuz %s
                initrd (loop)/boot/core.gz\n''' % (append))
        else:
            logging.info('        Unknow type, failed')
        fgb.write('}\n')
        os.system('umount %s' % (mount_dir))


if __name__ == '__main__':
    logging.basicConfig(level='INFO')
    logging.debug('Download dir: %s' % (DOWNLOAD_DIR))
    firmwares = read_config(CONFIG_FILE)

    fgb = open_custom_grub_config()
    for name, url in firmwares:
        logging.info('Target: %s' % (name))
        zp = download_firmware_zip(name, url)
        iso = extract_zip_to_iso(zp)
        move_iso_to_boot(iso)
        make_grub_menuentry(fgb, name, iso)
    fgb.write('}\n')
    fgb.close()
    os.chmod(GRUB_FILE, 0o755)
    shutil.rmtree(DOWNLOAD_DIR)

    print('Generate GRUB rules in: %s' % (GRUB_FILE))
    print('                ISO in: %s' % (BOOT_ISO_DIR))
    print('Please run "update-grub2" or "grub-mkconfig -o /boot/grub/grub.cfg')
    print('to generate new grub file.')
    print('And reboot to choose "Crucial Firmware Update in GRUB2.\n')
