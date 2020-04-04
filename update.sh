#!/bin/sh
python3 deb-info.py
bzip2 -c9k ./Packages > ./Packages.bz2
printf "Origin: BlackWings's Repo\nLabel: BlackWings\nSuite: stable\nVersion: 1.0\nCodename: BlackWings\nArchitecture: iphoneos-arm\nComponents: main\nDescription: BlackWings's Repo\nMD5Sum:\n "$(cat ./Packages | md5 | cut -d ' ' -f 1)" "$(stat -f%z ./Packages)" Packages\n "$(cat ./Packages.bz2 | md5 | cut -d ' ' -f 1)" "$(stat -f%z ./Packages.bz2)" Packages.bz2\n" >Release;
exit 0
