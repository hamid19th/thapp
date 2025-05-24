[app]
title = Python Quiz
package.name = pythonquiz
package.domain = org.pythonquiz
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
source.include_patterns = assets/*,images/*,credentials.json
version = 0.1
requirements = python3,kivy==2.3.1,kivymd==1.1.1,pillow,gspread,oauth2client,google-auth,google-auth-oauthlib,google-auth-httplib2,google-api-python-client
orientation = portrait
fullscreen = 0
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE
android.archs = arm64-v8a,armeabi-v7a
android.api = 33
android.minapi = 21
android.ndk = 25b
android.sdk = 33
android.accept_sdk_license = True
p4a.branch = master
p4a.bootstrap = sdl2
android.presplash_color = #FFFFFF

[buildozer]
log_level = 2
warn_on_root = 1
build_dir = ./.buildozer
bin_dir = ./bin
