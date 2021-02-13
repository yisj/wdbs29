from tabulate import tabulate
import sys
import os

class App:
    def __init__(self, app_id):
        self.app_id = app_id
        self.admob_id = ""
        self.app_name = ""
        self.admob_app_id = ""
        self.there_is_map = False
    
    def set_admob_id(self, admob_id):
        self.admob_id = admob_id
    
    def set_app_name(self, app_name):
        self.app_name = app_name
    
    def set_admob_app_id(self, admob_app_id):
        self.admob_app_id = admob_app_id

    def set_there_is_map(self):
        self.there_is_map = True


# apps
apps = list()

# app ids
app_ids = list()
with open('data/appids.csv') as f:
    for line in f:
        app_id = line.strip()
        app_ids.append(app_id)
        apps.append(App(app_id))

# admob ids
with open('data/admobunitids.csv') as f:
    for line in f:
        data = line.strip().split(',')
        app_id = data[0].strip()
        admob_id = data[1].strip()
        for app in apps:
            if app.app_id == app_id:
                app.set_admob_id(admob_id)

# app names
with open('data/appnames.csv') as f:
    for line in f:
        data = line.strip().split(',')
        app_id = data[0].strip()
        app_name = data[1].strip()
        for app in apps:
            if app.app_id == app_id:
                app.set_app_name(app_name)

with open('data/admobappids.csv') as f:
    for line in f:
        data = line.strip().split(',')
        app_id = data[0].strip()
        admob_app_id = data[1].strip()
        for app in apps:
            if app.app_id == app_id:
                app.set_admob_app_id(admob_app_id)




if __name__ == "__main__":
    header = ['app id', 'unit id', 'map', 'app name']
    if len(sys.argv) == 1:
        table = list()
        for app in apps:
            table.append([app.app_id, app.admob_id,
                'O' if os.path.exists('maps/%s.png' % app.app_id) else 'X',
                app.app_name
            ])
        print(tabulate(table, header))
    
    if len(sys.argv) == 2:
        keyword = sys.argv[1]
        app_ids = list()
        table = list()
        for app in apps:
            if keyword in app.app_id:
                table.append([app.app_id, app.admob_id,
                    'O' if os.path.exists('maps/%s.png' % app.app_id) else 'X', 
                    app.app_name
                ])
                app_ids.append(app.app_id)
        print(tabulate(table, header))
        print('[%s]' % ','.join(['"%s"' % a for a in app_ids ]))
