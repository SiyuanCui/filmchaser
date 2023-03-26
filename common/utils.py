import time
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.shortcuts import render
from django.conf import settings
import hashlib

import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter


def viewImage(obj, src):
    return mark_safe('<img src="%s" style="width:50px" />' % (src,))


def viewImages(obj, src):
    return mark_safe('<img src="%s" style="width:50px" />' % (src,))


def getID():
    itme_id = str(int(time.time() * 1000)) + str(int(time.perf_counter() / 1000))
    return itme_id


def getDate():
    d1 = timezone.now()
    return d1


def getDateStr():
    d1 = timezone.now()
    return d1.strftime("%Y-%m-%d")


def getTimeStr():
    d1 = timezone.now()
    return d1.strftime("%H:%M:%S")


def getDateTimeStr():
    d1 = timezone.now()
    return d1.strftime("%Y-%m-%d %H:%M:%S")


def input(request, name, default=None):
    if name in request.GET:
        return request.GET.get(name, default)
    if name in request.POST:
        return request.POST.get(name, default)
    return default


def inputlist(request, name, default=None):
    if name in request.GET:
        return request.GET.getlist(name, default)
    if name in request.POST:
        return request.POST.getlist(name, default)
    return default


def session(request, name):
    if name in request.session:
        return request.session[name]
    return ""


def checkLogin(request):
    if "username" in request.session:
        return True
    return False


def showMessage(request, message, code=0, href='javascript:history.go(-1);', icon=None, auto_redirect=True,
                auto_time=3):
    content = {
        'data': message,
        'code': code,
        'msg': message,
        'href': href,
        'icon': icon,
        'auto_redirect': auto_redirect,
        'auto_time': auto_time
    }
    if icon == None:
        if code > 0:
            content['icon'] = 'error'
        else:
            content['icon'] = 'success'

    return render(request, 'message.html', content)


def showSuccess(request, message, href=None, icon=None, auto_redirect=True):
    if href == None:
        href = request.headers['referer']
    return showMessage(request, message, 0, href, icon=icon, auto_redirect=auto_redirect)


def showError(request, message, href='javascript:history.go(-1);', icon=None, auto_redirect=True):
    return showMessage(request, message, 0, href, icon=icon, auto_redirect=auto_redirect)


def md5(str):
    m = hashlib.md5()
    m.update(str.encode("utf8"))
    print(m.hexdigest())
    return m.hexdigest()


def parseName(name):
    result = ''
    isUpper = False
    for index, name_char in enumerate(name):
        if index == 0:
            result += str(name_char).upper()
        elif str(name_char) == '_':
            isUpper = True
        else:
            if isUpper:
                result += str(name_char).upper()
            else:
                result += str(name_char)

    return result


class LazyImport(object):
    """
    Dynamic import module
    """

    def __init__(self, module_name, module_class):
        """
        :param module_name:
        :param module_class:
        :return: equals form module_name import module_class
        """
        self.module_name = module_name
        self.module_class = module_class
        self.module = None

    def __getattr__(self, name):
        if self.module is None:
            self.module = __import__(self.module_name, fromlist=[self.module_class])
        return getattr(self.module, name)


def imports(filename, clsname):
    importmodule = LazyImport(filename, clsname)
    is_true = hasattr(importmodule, clsname)
    if is_true:
        classname = getattr(importmodule, clsname)
        return classname
    return None


_letter_cases = "123456789"
_upper_cases = _letter_cases.upper()
_numbers = ''.join(map(str, range(3, 10)))
init_chars = ''.join((_letter_cases, _upper_cases, _numbers))


# Create verification code
def create_validate_code(size=(120, 30),
                         chars=init_chars,
                         img_type="PNG",
                         mode="RGB",
                         bg_color=(255, 255, 255),
                         fg_color=(0, 0, 255),
                         font_size=18,
                         font_type="Arial.ttf",
                         length=4,
                         draw_lines=True,
                         n_line=(1, 2),
                         draw_points=True,
                         point_chance=2):
    width, height = size
    # Create Drawings
    img = Image.new(mode, size, bg_color)
    draw = ImageDraw.Draw(img)  # Create a brush

    def get_chars():
        """Generates a string of a given length and returns the list format"""
        return random.sample(chars, length)

    def create_lines():
        """Draw interference line"""
        line_num = random.randint(*n_line)  # Number of interference lines

        for i in range(line_num):
            begin = (random.randint(0, size[0]), random.randint(0, size[1]))
            end = (random.randint(0, size[0]), random.randint(0, size[1]))
            draw.line([begin, end], fill=(0, 0, 0))

    def create_points():
        """Draw interference points"""
        chance = min(100, max(0, int(point_chance)))  # Size is limited to [0, 100]

        for w in range(width):
            for h in range(height):
                tmp = random.randint(0, 100)
                if tmp > 100 - chance:
                    draw.point((w, h), fill=(0, 0, 0))

    def create_strs():
        """Draw verification code characters"""
        c_chars = get_chars()
        strs = ' %s ' % ' '.join(c_chars)  # Each character is separated by a space

        font = ImageFont.truetype(font_type, font_size)
        font_width, font_height = font.getsize(strs)

        draw.text(((width - font_width) / 3, (height - font_height) / 3),
                  strs, font=font, fill=fg_color)

        return ''.join(c_chars)

    if draw_lines:
        create_lines()
    if draw_points:
        create_points()
    strs = create_strs()

    # Shape Warp Parameters
    params = [1 - float(random.randint(1, 2)) / 100,
              0,
              0,
              0,
              1 - float(random.randint(1, 10)) / 100,
              float(random.randint(1, 2)) / 500,
              0.001,
              float(random.randint(1, 2)) / 500
              ]
    # img = img.transform(size, Image.PERSPECTIVE, params)  # Create a twist
    # img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)  # Filter, boundary enhancement (higher threshold)
    return img, strs


# import decimal
# import json
# class DecimalEncoder(json.JSONEncoder):
#    def default(self, o):
#        if isinstance(o, decimal.Decimal):
#            return float(o)
#        super(DecimalEncoder, self).default(o)


import decimal
import json
import datetime
from django.core.serializers.json import DjangoJSONEncoder


class DecimalEncoder(DjangoJSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        if isinstance(o, datetime.datetime):
            return o.strftime("%Y-%m-%d %H:%M:%S")
        super(DecimalEncoder, self).default(o)
