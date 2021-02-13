import os
import shutil
import datetime
import colorsys
import random
from PIL import Image
from PIL import ImageColor


def make_folder(folder_name):
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)

def delete_folder(path):
    if os.path.exists(path):
        shutil.rmtree(path)

def list_to_sh(target_list, filename):
    with open(filename, 'w') as f:
        f.write('\n'.join(target_list))

def make_version():
    today = datetime.date.today()

    year = today.year
    month = today.month
    day = today.day

    year -= 1999
    month = month*8 + 3
    day = day*3+3

    return "%02d.%02d.%02d" % (year, month, day)

def get_random_color():
	r, g, b = colorsys.hls_to_rgb(random.random(), 0.8, 0.8)
	r = int(r*255)
	g = int(g*255)
	b = int(b*255)
	return '#%02x%02x%02x' % (r, g, b)


def Artboard(size, color):
	artboard = Image.new(mode="RGB", size=size, color=ImageColor.getrgb(color))
	return artboard

# s1.png
def take_first_screenshot(im):
	s_ratio = 1280/720
	w, h = im.size
	im_ratio = w/h

	height = h
	width = round(height/s_ratio)

	crop_point = (
			round((w-width)/2),
			0,
			round((w+width)/2),
			h)
	cropped = im.crop(crop_point)
	resized = cropped.resize((720,1280))

	return resized


# s2.png
def take_second_screenshot(im):
	artboard = Image.new("RGB", (1080, 1920), "white")
	galaxy_note8 = Image.open("galaxy_note8.png")
	phone_layer = Image.new("RGB", galaxy_note8.size, "white")
	W, H = artboard.size
	w, h = galaxy_note8.size


	s_ratio = 1400/720
	mw, mh = im.size
	im_ratio = mw/mh
	
	mw = round(mw/2)
	mh = round(mh/2)

	height = mh
	width = round(height/s_ratio)

	ran_h = random.randint(0,round(mh/2))
	ran_w = random.randint(0,round(mw/2))


	crop_point = (
			round((mw-width)/2)+ran_w,
			ran_h,
			round((mw+width)/2)+ran_w,
			mh+ran_h)
	cropped = im.crop(crop_point)
	resized = cropped.resize((w-40,int((w-40)*1400/720)))

	phone_layer.paste(resized, (20, 94))
	phone_layer.paste(galaxy_note8, (0, 0), mask=galaxy_note8)

	x = int((W - w) / 2)
	y = int(200)

	artboard.paste(phone_layer, (x, y))
	

	return artboard


# gi.png
def take_graphic_image(im):
	s_ratio = 1024/500
	w, h = im.size
	im_ratio = w/h

	width = w
	height = round(width/s_ratio)

	crop_point = (
			0,
			round((h-height)/2),
			w,
			round((h+height)/2),
			)
	cropped = im.crop(crop_point)
	resized = cropped.resize((1024,500))

	return resized