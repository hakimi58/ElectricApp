[app]

# (str) Title of your application
title = Expert Electric

# (str) Package name
package.name = expertelectric

# (str) Package domain (needed for android packaging)
package.domain = org.expert

# (str) Source code where the main.py is located
source.dir = .

# (list) Source files to include (let's include python files and icons)
source.include_exts = py,png,jpg,kv,atlas

# (str) Application versioning
version = 0.1

# (list) Application requirements
# الأندرويد يستحق المكتبات هاذي باش يخدم الكود متاعك
requirements = python3,kivy,android

# (str) Icon of the application
icon.filename = %(source.dir)s/mipmap-xxxhdpi/ic_launcher.png

# (str) Supported orientations
orientation = portrait

# (bool) Indicate if the application should be fullscreen
fullscreen = 1

# (list) Permissions
android.permissions = INTERNET

# (int) Android API to use (نسخة حديثة ومستقرة)
android.api = 31

# (int) Minimum API your APK will support
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (bool) If True, then automatically accept SDK license
# السطر هذا هو اللي يخلي الـ Build ما يوقفش
android.accept_sdk_license = True

# (str) The Android arch to build for
android.archs = arm64-v8a

[buildozer]

# (int) Log level (2 يعني يعطيك تفاصيل كاملة لو صار غلط)
log_level = 2

# (int) Display warning if buildozer is run as root
warn_on_root = 1
