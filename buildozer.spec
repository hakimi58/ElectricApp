[app]

# (str) Title of your application
title = Expert Electric

# (str) Package name
package.name = expertelectric

# (str) Package domain (needed for android packaging)
package.domain = org.expert

# (str) Full name including the version
version = 0.1

# (str) Source code where the main.py is located
source.dir = .

# (list) Source files to include
source.include_exts = py,png,jpg,kv,atlas,ttf

# (list) Application requirements
requirements = python3,kivy==2.3.0,android,hostpython3,arabic-reshaper,python-bidi

# (str) Supported orientations
orientation = portrait

# (list) Permissions
android.permissions = INTERNET

# (int) Target Android API
android.api = 33

# (int) Minimum API support
android.minapi = 21

# (str) Android logcat filters to use
android.logcat_filters = *:S python:D

# (str) The directory where the Android resources are located
# هذا السطر هو اللي باش يخلي أيقونات الـ mipmap تظهر
android.res_dir = res

# (bool) Use --private data storage
android.private_storage = True

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2

# (int) Display warning if buildozer is run as root
warn_on_root = 1

# (str) Path to build artifacts
bin_dir = ./bin
