import sys
from utils import *


def make_screenshots(app_id):
    make_folder('play')
    play_folder = 'play/%s' % app_id
    make_folder(play_folder)

    im = Image.open('maps/%s.png' % app_id)
    s1 = take_second_screenshot(im)
    s2 = take_second_screenshot(im)
    s3 = take_second_screenshot(im)
    s4 = take_second_screenshot(im)
    s5 = take_second_screenshot(im)
    s6 = take_second_screenshot(im)
    s7 = take_second_screenshot(im)
    s8 = take_second_screenshot(im)

    s1.save('%s/s1.png' % play_folder)
    s2.save('%s/s2.png' % play_folder)
    s3.save('%s/s3.png' % play_folder)
    s4.save('%s/s4.png' % play_folder)
    s5.save('%s/s5.png' % play_folder)
    s6.save('%s/s6.png' % play_folder)
    s7.save('%s/s7.png' % play_folder)
    s8.save('%s/s8.png' % play_folder)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        target_app_id = sys.argv[1]
        make_screenshots(target_app_id)