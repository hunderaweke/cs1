import random as _random
import string as _string
import base64 as _base64

try:
    unicode
except NameError:
    basestring = unicode = str

_permanent_uid = dict()


def _generate_uid():
    _letters = _string.ascii_letters + _string.digits
    return ''.join((_random.choice(_letters) for _ in range(16)))


def print_image_permanent(name, content):
    if name not in _permanent_uid:
        _permanent_uid[name] = _generate_uid()

    if not isinstance(content, basestring):
        content = content.decode('utf-8')

    uid = _permanent_uid[name]
    print('<image ' + uid + '>' + content + '</' + uid + '>')


def print_image(content):
    uid = _generate_uid()

    if not isinstance(content, basestring):
        content = content.decode('utf-8')

    print('<image ' + uid + '>' + content + '</' + uid + '>')
