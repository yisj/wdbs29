import os
import sys
from apps import apps
from utils import *

def sign_app(app):
    make_folder('apks')
    step6 = list()
    release = 'working/%s/platforms/android/app/build/outputs/apk/release' % app.app_id
    unsigned = '%s/app-release-unsigned.apk' % release
    zipaligned = '%s/app-release-zipaligned.apk' % release
    if os.path.exists('keys/%s.jks' % app.app_id):
        step6.append('zipalign -f -v 4 %s %s' % (unsigned, zipaligned))
        step6.append("printf 'tmdwotnwls' | apksigner sign --ks keys/%s.jks --out apks/%s-%s.apk %s" % (
            app.app_id,
            make_version(),
            app.app_id,
            zipaligned
        ))
    else:
        step6.append('jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore wonderever.keystore -storepass tmdwotnwlstndus %s wondereverkey' % unsigned)
        step6.append('zipalign -f -v 4 %s apks/%s-%s.apk' % (unsigned, make_version(), app.app_id))

    list_to_sh(step6, 'step6.sh')


if __name__ == "__main__":
    if len(sys.argv) == 2:
        target_app_id = sys.argv[1]
        print("target app id:", target_app_id)

        there_is_app_id = False
        target_app = None
        for app in apps:
            if app.app_id == target_app_id:
                there_is_app_id = True
                target_app = app
        
        if there_is_app_id:
            sign_app(target_app)