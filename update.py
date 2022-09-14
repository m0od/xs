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
    ret += 'Depends: {}\n'.format(deb_info.get('Depends') is not None and deb_info.get('Depends') or '')
    ret += 'Conflicts: {}\n'.format(deb_info.get('Conflicts') is not None and deb_info.get('Conflicts') or '')
    ret += 'Priority: {}\n'.format(deb_info.get('Priority') is not None and deb_info.get('Priority') or 'optional')
    ret += 'Architecture: {}\n'.format(deb_info.get('Architecture'))
    ret += 'Author: {}\n'.format(deb_info.get('Author'))
    ret += 'Homepage: {}\n'.format(deb_info.get('Homepage') is not None and deb_info.get('Homepage') or '')
    ret += 'Maintainer: {}\n'.format(deb_info.get('Maintainer'))
    ret += 'Version: {}\n'.format(deb_info.get('Version'))
    ret += 'Filename: ./{}\n'.format(filepath)
    ret += 'MD5sum: {}\n'.format(get_hash(filepath, 'md5'))
    ret += 'SHA1: {}\n'.format(get_hash(filepath, 'sha1'))
    ret += 'SHA256: {}\n'.format(get_hash(filepath, 'sha256'))
    ret += 'SHA512: {}\n'.format(get_hash(filepath, 'sha512'))
    ret += 'Depiction: https://m0od.github.io/xs/description.html?id={}\n'.format(deb_info.get('Package'))
    ret += 'Size: {}\n'.format(get_size(filepath))
    info = {
        "name": deb_info.get('Name'),
        "description": deb_info.get('Description')
    }
    folder = 'packageinfo'
    with open(os.path.join(folder, deb_info.get('Package')), 'w') as f:
        f.write(json.dumps(info))
    return ret


def get_hash(filepath, hash_type):
    fs = open(filepath, 'rb')
    hash_str = ''
    if hash_type == 'md5':
        hash_str = hashlib.md5(fs.read()).hexdigest()
    elif hash_type == 'sha1':
        hash_str = hashlib.sha1(fs.read()).hexdigest()
    elif hash_type == 'sha256':
        hash_str = hashlib.sha256(fs.read()).hexdigest()
    elif hash_type == 'sha512':
        hash_str = hashlib.sha512(fs.read()).hexdigest()
    fs.close()
    return hash_str


def get_size(filepath):
    return os.path.getsize(filepath)


def gen_release():
    os.system('bzip2 -c9k ./Packages > ./Packages.bz2')
    ret = "Origin: BlackWings XS Repo\n"
    ret += 'Label: BlackWings\n'
    ret += 'Suite: stablen\n'
    ret += 'Version: 1.0\n'
    ret += 'Codename: BlackWings\n'
    ret += 'Architecture: iphoneos-arm\n'
    ret += 'Components: main\n'
    ret += "Description: BlackWings XS Repo\n"
    ret += 'MD5Sum:\n'
    ret += ' {} {} Packages\n'.format(get_hash('Packages', 'md5'), get_size('Packages'))
    ret += ' {} {} Packages.bz2\n'.format(get_hash('Packages.bz2', 'md5'), get_size('Packages.bz2'))
    fw = open('Release', 'w')
    fw.write(ret)
    fw.close()


files = []
for r, d, f in os.walk('debs'):
    for file in f:
        if '.deb' in file:
            files.append(os.path.join(r, file))
with open('Packages', 'w') as f:
    pkg = ''
    for fp in files:
        pkg += gen_package(fp) + '\n'
    f.write(pkg.strip())
gen_release()
