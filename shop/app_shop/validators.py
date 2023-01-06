import xml.etree.cElementTree as et


def is_svg(file):
    tag = None
    try:
        for event, el in et.iterparse(file, ('start',)):
            tag = el.tag
            break
    except et.ParseError:
        pass
    return tag == '{http://www.w3.org/2000/svg}svg'
