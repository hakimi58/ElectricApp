[app]
title = Expert Electric
package.name = expertelectric
package.domain = org.expert
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy==2.3.0,android,hostpython3

# أيقونة فارغة لتفادي المشاكل حالياً
icon.filename = 

orientation = portrait
fullscreen = 1
android.permissions = INTERNET
android.api = 31
android.ndk = 25b
android.ndk_api = 21
android.accept_sdk_license = True
android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1
