[app]

# (str) Title of your application
title = 施工现场罚款系统

# (str) Package name
package.name = fineapp

# (str) Package domain (needed for android/ios packaging)
package.domain = org.finesystem

# (str) Source files where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,json,csv

# (list) List of inclusions using pattern matching
#source.include_patterns = assets/*,images/*.png

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy,kivymd,requests,fpdf,Pillow,plyer

# (str) Presplash of the application
#presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
#icon.filename = %(source.dir)s/data/icon.png

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (list) List of service to declare
#services = NAME:ENTRYPOINT_TO_PY,NAME:ENTRYPOINT_TO_PY

#
# OSX Specific
#

#
# Android specific
#

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (string) Presplash background color (for android toolchain only)
#presplash.color = #FFFFFF

# (list) Permissions
android.permissions = CAMERA, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, INTERNET

# (int) Target Android API, should be as high as possible.
#android.api = 31
#android.minapi = 21

# (str) NDK version to use
#android.ndk = 23b

# (int) Android NDK API to use. This is the minimum API your app will support, it should usually match android.minapi.
#android.ndk_api = 21

# (bool) If True, then skip trying to update the Android sdk
# This can be useful to avoid excess Internet downloads or save time
# when an update is due and you just want to test/build your package
# android.skip_update = False

# (str) Android entry point, default must be 'org.kivy.android.PythonActivity'
android.entrypoint = org.kivy.android.PythonActivity

# (list) Android architecture to build
android.archs = arm64-v8a,armeabi-v7a

# (bool) Indicate whether the screen should remain on while your application
# is visible. This defaults to False (screen may be turned off).
#android.wakelock = False

# (list) Android's libmodlue settings
#android.libmodlue =

# (bool) Enable Android VM multitasking feature.
#android.multidex = False

#
# iOS specific
#

# (str) Path to a custom kivy-ios folder
#ios.kivy_ios_dir = ../kivy-ios
# Alternately, specify the Python module to import instead of the Kivy module.
#ios.kivy_ios_module = kivy_ios

# (bool) Force project to use specific Python version
#ios.kivy_ios_python_version = 3.7.2

# (str) Targeted iOS version
#ios.ios_version = 10.3

# iOS Kivy project settings
#ios.codesign.debug = 'iPhone Developer'
#ios.codesign.release = 'iPhone Distribution'

# iOS additional frameworks
#ios.frameworks =

# iOS Kivy project plist
#ios.plist =

#
# macOS specific
#

#
# Windows specific
#

#
# General
#

# (bool) Indicate if the application should be debug or not
debug = False

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy,requests,fpdf,Pillow,plyer

# (list) Garden requirements
#garden_requirements =

# (str) Presplash filename
#presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon filename
#icon.filename = %(source.dir)s/data/icon.png

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (bool) Android's ndk version
#android.ndk =

#
# Android specific
#

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (str) Presplash background color (for android toolchain only)
#presplash.color = #FFFFFF

# (list) Permissions
android.permissions = CAMERA, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, INTERNET

# (int) Target Android API, should be as high as possible.
#android.api = 31
#android.minapi = 21

# (str) NDK version to use
#android.ndk = 23b

# (int) Android NDK API to use. This is the minimum API your app will support, it should usually match android.minapi.
#android.ndk_api = 21

# (bool) If True, then skip trying to update the Android sdk
# This can be useful to avoid excess Internet downloads or save time
# when an update is due and you just want to test/build your package
# android.skip_update = False

# (str) Android entry point, default must be 'org.kivy.android.PythonActivity'
android.entrypoint = org.kivy.android.PythonActivity

# (list) Android architecture to build
android.archs = arm64-v8a,armeabi-v7a

# (bool) Indicate whether the screen should remain on while your application
# is visible. This defaults to False (screen may be turned off).
#android.wakelock = False

# (list) Android's libmodlue settings
#android.libmodlue =

# (bool) Enable Android VM multitasking feature.
#android.multidex = False
