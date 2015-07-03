import re
import random
import jinja2
import markdown
import smartypants as sp
# from chicagoclimateonline.constants import *


def smartypants(text):
    return sp.smartypants(text)


def safe_markdown(text):
    return jinja2.Markup(markdown.markdown(text))


def search_markdown(text):
    text = re.sub(r'\[([^\]]+)\]\s*\(\S+(?=\))', r'\1', text)
    text = re.sub(r'\[([^\]]+)\]\s*\(\S+', r'\1', text)
    text = re.sub(r'([^\[]+)\]\([^\)]+\)?', r'\1', text)
    text = safe_markdown(text)
    return text


def nbsp(text):
    text = re.sub(r' ', '&nbsp;', text)
    return jinja2.Markup(text)


def format_currency(value):
    return "${:,.2f}".format(value)