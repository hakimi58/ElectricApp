[app]

# (str) Title of your application
title = Expert Electric

# (str) Package name
package.name = expertelectric

# (str) Package domain (needed for android packaging)
package.domain = org.expert

# (str) Source code where the main.py is located
source.dir = .

# (list) Source files to include
source.include_exts = py,png,jpg,kv,atlas

# (str) Application versioning
version = 0.1

# (list) Application requirements
# زدنا المكتبات الأساسية لضمان الاستقرار
requirements = python3,kivy==2.3.0,android,hostpython3

# (str) Icon of the application
# خليناها فارغة مؤقتا باش نتجاوزو مشكلة المسار ونضمنو الـ Build يكمل
icon.filename = 

# (str) Supported orientations
orientation = portrait

# (bool) Indicate if the application should be fullscreen
fullscreen = 1

# (list) Permissions
android.permissions = INTERNET

# (int) Android API to use
android.api = 31

# (int) Minimum API your APK will support
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (bool) If True, then automatically accept SDK license
android.accept_sdk_license = True

# (str) The Android arch to build for
android.archs = arm64-v8a

[buildozer]

# (int) Log level (2 يعطيك كل التفاصيل لو صارت غلطة)
log_level = 2

# (int) Display warning if buildozer is run as root
warn_on_root = 1
