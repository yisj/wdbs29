import os
import sys
import math
import shutil

from PIL import Image
from PIL import ImageColor

from itertools import accumulate

from apps import apps
from utils import make_version
from utils import *
from collections import namedtuple

import random



def make_config(app):
    config_template = '''
<?xml version='1.0' encoding='utf-8'?>
<widget id="com.gaedog.{APP_ID}" version="{VERSION}" xmlns="http://www.w3.org/ns/widgets" xmlns:cdv="http://cordova.apache.org/ns/1.0">
    <name>{APP_NAME}</name>
    <description>
        WONDEREVER METRO APP.
    </description>
    <author>
        WONDEREVER
    </author>
    <content src="index.html" />
    <plugin name="cordova-plugin-whitelist" spec="1" />
    <access origin="*" />
    <allow-intent href="http://*/*" />
    <allow-intent href="https://*/*" />
    <allow-intent href="tel:*" />
    <allow-intent href="sms:*" />
    <allow-intent href="mailto:*" />
    <allow-intent href="geo:*" />
    <platform name="android">
        <allow-intent href="market:*" />
    </platform>
    <platform name="ios">
        <allow-intent href="itms:*" />
        <allow-intent href="itms-apps:*" />
    </platform>
</widget>
    '''
    config_content = config_template.format(
        APP_ID=app.app_id,
        APP_NAME=app.app_name,
        VERSION=make_version()
    )

    with open('working/%s/config.xml' % app.app_id, 'w') as f:
        f.write(config_content)






def make_www(app):
    www = 'working/%s/www' % app.app_id

    if os.path.exists(www):
        shutil.rmtree(www)
        os.mkdir(www)
    
    target_image = 'maps/%s.png' % app.app_id
    im = Image.open(target_image)
    
    w,h = im.size
    div = 10
    w_rem = w % div
    h_rem = w % div
    w_width = math.floor(w/div)
    h_width = math.floor(h/div)

    w_list = list()
    h_list = list()

    for _ in range(div):
        w_list.append(w_width)
        h_list.append(h_width)

    for w in range(w_rem):
        w_list[w] += 1
    for h in range(h_rem):
        h_list[h] += 1

    s = 'working/%s/www/s' % app.app_id
    if not os.path.exists(s):
        os.mkdir(s)

    w_a_list = list(accumulate(w_list))
    h_a_list = list(accumulate(h_list))
    w_a_list = [0] + w_a_list
    h_a_list = [0] + h_a_list

    for I in range(div):
        for J in range(div):
            cropped = im.crop((w_a_list[I],h_a_list[J],w_a_list[I+1],h_a_list[J+1]))
            cropped.save('%s/%d%d.png' % (s, I, J))
    table = list()
    table.append('<table cellspacing="0" cellpadding="0">')
    for J in range(div):
        table.append('<tr>')
        for I in range(div):
            table.append('<td><img src="s/%d%d.png" /></td>' % (I,J))
        table.append('</tr>')
    table.append('</table>')
    table = ''.join(table)

    index = list()
    index.append('<html><head><meta content="user-scalable=yes, initial-scale=0.2, maximum-scale=2.5, minimum-scale=0.01, width=device-width" name="viewport"/>')
    index.append('<script src="cordova.js"></script></head><body onload="o()"><script>')
    index.append("function o(){document.addEventListener('deviceready',i,false);}")
    index.append("function i(){admob.banner.config({id:'%s',isTesting:false,autoShow:true});admob.banner.prepare();}" % app.admob_id)
    index.append('</script><div>%s</div></body></html>'% table)

    with open('working/%s/www/index.html' % app.app_id, 'w') as f:
        f.write(''.join(index))




def get_shape(app):
    Shape = namedtuple('Shape', ['app_id', 'shape'])
    shapes = list()
    with open('data/shapes.csv') as f:
        for line in f:
            data = line.strip().split(',')
            app_id = data[0].strip()
            shape = data[1].strip()
            shapes.append(Shape(app_id, shape))

    for shape in shapes:
        if shape.app_id == app.app_id:
            return Image.open(shape.shape).convert('RGBA')

    shapes = list()
    for file in os.listdir('shapes'):
        if file.endswith('.png'):
            shapes.append(file)
    return Image.open('shapes/%s' % random.choice(shapes)).convert('RGBA')


def get_icon(app):
    icon_path = 'icons/%s.png' % app.app_id
    if os.path.exists(icon_path):
        icon = Image.open(icon_path)
        foreground = icon
        background = icon
    else:
        color = get_random_color()
        shape_path = 'shape/%s.png' % app.app_id
        ios7 = Image.open('ios7.png').convert('L')
        if os.path.exists(shape_path):
            shape = Image.open(shape_path).convert('RGBA')
        else:
            shape = get_shape(app)
        foreground = shape
        background = Artboard((512,512), color)
        icon = Artboard((512,512), color)
        icon.paste(shape, mask=shape)
        icon.putalpha(ios7)
    return (icon, foreground, background)


def make_screenshots(app):

    make_folder('play')
    play_folder = 'play/%s' % app.app_id
    make_folder(play_folder)

    im = Image.open('maps/%s.png' % app.app_id)
    s1 = take_second_screenshot(im)
    s2 = take_second_screenshot(im)
    s3 = take_second_screenshot(im)
    s4 = take_second_screenshot(im)
    s5 = take_second_screenshot(im)
    s6 = take_second_screenshot(im)
    s7 = take_second_screenshot(im)
    s8 = take_second_screenshot(im)
    gi = take_graphic_image(im)

    s1.save('%s/s1.png' % play_folder)
    s2.save('%s/s2.png' % play_folder)
    s3.save('%s/s3.png' % play_folder)
    s4.save('%s/s4.png' % play_folder)
    s5.save('%s/s5.png' % play_folder)
    s6.save('%s/s6.png' % play_folder)
    s7.save('%s/s7.png' % play_folder)
    s8.save('%s/s8.png' % play_folder)
    gi.save('%s/gi.png' % play_folder)


def make_icons(app):
    icon, foreground, background = get_icon(app)

    make_folder('play/%s' % app.app_id)
    icon.save('play/%s/icon.png' % app.app_id)
    icon.save('icons/%s.png' % app.app_id)

    android_res = 'working/%s/platforms/android/app/src/main/res/' % app.app_id

    for sub in os.listdir(android_res):
        if 'drawable' in sub:
            shutil.rmtree(os.path.join(android_res, sub))
        if 'mipmap' in sub:
            files = os.listdir(os.path.join(android_res, sub))
            for f in files:
                if f.endswith('.png'):
                    if 'foreground' in f:
                        target_path = os.path.join(android_res, sub, f)
                        w, h = Image.open(target_path).size
                        resized_foreground = foreground.resize((w, h))
                        resized_foreground.save(target_path)
                    elif 'background' in f:
                        target_path = os.path.join(android_res, sub, f)
                        w, h = Image.open(target_path).size
                        resized_background = background.resize((w, h))
                        resized_background.save(target_path)
                    else:
                        target_path = os.path.join(android_res, sub, f)
                        w, h = Image.open(target_path).size
                        resized_icon = icon.resize((w, h))
                        resized_icon.save(target_path)


def make_java(app):
    java_template = '''
package com.gaedog.{APP_ID};

import android.os.Bundle;
import org.apache.cordova.*;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebSettings.ZoomDensity;

public class MainActivity extends CordovaActivity
{{
    @Override
    public void onCreate(Bundle savedInstanceState)
    {{
        super.onCreate(savedInstanceState);

        Bundle extras = getIntent().getExtras();
        if (extras != null && extras.getBoolean("cdvStartInBackground", false)) {{
            moveTaskToBack(true);
        }}

        loadUrl(launchUrl);
        WebView webView = (WebView) appView.getEngine().getView();
        WebSettings settings = webView.getSettings();
        settings.setBuiltInZoomControls(true);
        settings.setSupportZoom(true);
        settings.setUseWideViewPort(true);
    }}
}}
'''
    java_content = java_template.format(
        APP_ID = app.app_id
    )
    package_id = 'com.gaedog.%s' % app.app_id
    path = 'working/%s/platforms/android/app/src/main/java/%s' % (
        app.app_id,
        package_id.replace('.', '/')
    )
    with open('%s/MainActivity.java' % path, 'w') as f:
        f.write(java_content)


def make_app(app):
    make_config(app)
    make_www(app)
    make_icons(app)
    make_screenshots(app)
    make_java(app)


    

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
            make_app(target_app)