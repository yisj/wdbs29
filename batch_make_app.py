import os
from utils import delete_folder

targets = ["taichung_taiwan","taoyuan_taiwan","kaohsiung_taiwan"]

for target_app_id in targets:
    delete_folder('working/%s' % target_app_id)
    os.system('python3 make_app.py %s' % target_app_id)
