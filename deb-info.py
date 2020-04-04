from deb_pkg_tools.package import inspect_package_fields
import hashlib
import os
import json


def gen_package(filepath):
    deb_info = inspect_package_fields(filepath)
    ret = 'Package: {}\n'.format(deb_info.get('Package'))
    ret += 'Name: {}\n'.format(deb_info.get('Name'))
    ret += 'Description: {}\n'.format(deb_info.get('Description'))
    ret += 'Section: {}\n'.format(deb_info.get('Section'))
    ret += 'Depends: {}\n'.format(deb_info.get('Depends'))
    ret += 'Conflicts: {}\n'.format(deb_info.get('Conflicts'))
    ret += 'Priority: {}\n'.format(deb_info.get('Priority'))
    ret += 'Architecture: {}\n'.format(deb_info.get('Architecture'))
    ret += 'Author: {}\n'.format(deb_info.get('Author'))
    ret += 'Homepage: {}\n'.format(deb_info.get('Homepage'))
    ret += 'Maintainer: {}\n'.format(deb_info.get('Maintainer'))
    ret += 'Version: {}\n'.format(deb_info.get('Version'))
    ret += 'Filename: ./{}\n'.format(filepath)
    with open(filepath, 'rb') as f:
        ret += 'MD5sum: {}\n'.format(hashlib.md5(f.read()).hexdigest())
    ret += 'Depiction: https://bwat.ph03nix.club/description.html?id={}\n'.format(deb_info.get('Package'))
    ret += 'Size: {}\n'.format(os.path.getsize(filepath))
    info = {
        "name": deb_info.get('Name'),
        "description": deb_info.get('Description')
    }
    folder = 'packageinfo'
    with open(os.path.join(folder, deb_info.get('Package')), 'w') as f:
        f.write(json.dumps(info))
    return ret
files = []
for r, d, f in os.walk('debs'):
    for file in f:
        if '.deb' in file:
            files.append(os.path.join(r, file))
with open('Packages', 'w') as f:
    for fp in files:
        f.write(gen_package(fp) + '\n')
# print(gen_package('com.blackwings.autotouch_5.1.5_iphoneos-arm.deb'))


# with open('com.blackwings.autotouch_5.1.5_iphoneos-arm.deb', "rb") as f:
#     bytes = f.read()  # read file as bytes
#     readable_hash = hashlib.md5(bytes).hexdigest();
#     print(readable_hash)
# import os
# print(os.path.getsize('com.blackwings.autotouch_5.1.5_iphoneos-arm.deb'))
'''
Package: com.blackwings.autotouch
Name: AutoTouch
Description: Record and playback touch operations, play macro scripts automatically.
Section: Utilities
Depends: firmware (>= 8.0), mobilesubstrate, com.rpetrich.rocketbootstrap (>= 1.0.2)
Conflicts: com.repo.xarold.com.autotouch8, repo.biteyourapple.net.autotouch8, repo.biteyourapple.net.autotouch, com.hackyouriphone.autotouch8, me.autotouch.AutoTouch.ios8
Priority: optional
Architecture: iphoneos-arm
Author: Kent Krantz <kentkrantz@gmail.com>
Homepage: https://bwat.ph03nix.club
Maintainer: Kent Krantz <kentkrantz@gmail.com>
Version: 5.1.5
Filename: ./com.blackwings.autotouch_5.1.5_iphoneos-arm.deb
Depiction: https://bwat.ph03nix.club/description.html?id=com.blackwings.autotouch
MD5sum: 7646f3470981d0608a789f9e45900144
Size: 45149698
'''