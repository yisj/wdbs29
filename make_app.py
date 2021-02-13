import os
import sys
from utils import make_folder, list_to_sh
from apps import apps


def make_app(app):
    print("make app:", target_app_id)
    # making /working folder
    make_folder('working')
    make_folder('play')
    
    steps = list()
    step1 = list()
    step2 = list()
    step4 = list()


    step1.append('cordova create working/%s com.gaedog.%s metroapp' % (app.app_id, app.app_id))

    step2.append('cd working/%s' % app.app_id)
    step2.append('cordova platform add android@9.0.0')
    step2.append('cordova plugin add cordova-plugin-admob-free@0.27.0 --variable ADMOB_APP_ID="%s"' % app.admob_app_id )
    step2.append('cd ../..')

    step4.append('cd working/%s' % app.app_id)
    step4.append('cordova build android --release')


    steps.append('sh step1.sh')
    steps.append('sh step2.sh')
    steps.append('python3 step3.py %s' % app.app_id)
    steps.append('sh step4.sh')
    steps.append('python3 step5.py %s' % app.app_id)
    steps.append('sh step6.sh')

    list_to_sh(step1, 'step1.sh')
    list_to_sh(step2, 'step2.sh')
    list_to_sh(step4, 'step4.sh')
    list_to_sh(steps, 'steps.sh')

    os.system('sh steps.sh')



if __name__ == "__main__":

    if len(sys.argv) == 2:
        target_app_id = sys.argv[1]

        target_app = None
        for app in apps:
            if app.app_id == target_app_id:
                target_app = app


        can_make_app = True
        if target_app == None:
            can_make_app = False
        if can_make_app:
            make_app(target_app)
