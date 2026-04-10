[app]

# (str) Title of your application
title = Expert Electric

# (str) Package name
package.name = expertelectric

# (str) Package domain
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

# (int) Target Android API
android.api = 33

# (int) Minimum API support
android.minapi = 21

# (str) The directory where the Android resources are located
# التعديل الأهم هنا
android.res_dir = res

# (bool) Use --private data storage
android.private_storage = True

[buildozer]
log_level = 2
warn_on_root = 1
bin_dir = ./bin
