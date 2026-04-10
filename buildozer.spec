[app]

# (str) Title of your application
title = Expert Electric

# (str) Package name
package.name = expertelectric

# (str) Package domain (needed for android packaging)
package.domain = org.expert

# (str) Source code where the main.py is located
source.dir = .

# (list) Source files to include (let's include everything needed)
source.include_exts = py,png,jpg,kv,atlas,ttf

# (list) Application requirements
# زدنا مكتبات العربي هنا باش يخدم مريڨل
requirements = python3,kivy==2.3.0,android,hostpython3,arabic-reshaper,python-bidi

# (str) Application version
# بدلناها لـ 0.2 باش التليفون يعرف إلي هو تحديث جديد
version = 0.2

# (str) Supported orientations
orientation = portrait

# (int) Target Android API
android.api = 33

# (int) Minimum API support
android.minapi = 21

# (str) The directory where the Android resources are located
# هذا السطر هو اللي باش يقرى الأيقونات من مجلد res اللي صورتهولي
android.res_dir = res

# (bool) Use --private data storage (True is standard)
android.private_storage = True

# (str) Android logcat filters
android.logcat_filters = *:S python:D

# (str) Android entry point
android.entrypoint = main

# (list) Permissions
android.permissions = INTERNET

[buildozer]

# (int) Log level (2 = values and info)
log_level = 2

# (int) Display warning if buildozer is run as root
warn_on_root = 1

# (str) Path to build artifacts
bin_dir = ./bin
