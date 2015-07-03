import itertools
import cookielib
import urllib
import urllib2


TYPES = [129, 102, 109, 100, 107, 124, 126, 101, 105, 104, 108, 103, ]
YEARS = [1905 + y for y in range(110)]
FOO = [
    (100, [1948, 1965, ] + [1981 + y for y in range(2015-1981)]),       #Book
    (101, [1982] + [1992 + y for y in range(2015-1992)]),               #Chapter
    (102, [1905, 1921, 1928] + [1969 + y for y in range(2015-1969)]),   #Journal
    (103, [1995, 2007, 2009]),                                          #Conf paper
    (104, [1995 + y for y in range(2015-1995)]),                        #Conf proceeding
    (105, [2001, 2009, 2010]),                                          #Newspaper
    (107, [2001 + y for y in range(2015-2001)]),                        #Magazine
    (108, [2009, ]),                                                    #
    (109, [1991 + y for y in range(2015-1991)]),                        #Report
    (124, [1996 + y for y in range(2015-1996)]),                        #Unpublished
    (126, [2004 + y for y in range(2015-2004)]),                        #Govt report
    (129, [1991 + y for y in range(2015-1991)]),                        #
                                                                        #Manuscript 121
]
URL = 'http://chicagoclimateonline.org/'


cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)
authentication_url = URL + 'homepage'
payload = {
    'op': 'Log in',
    'name': 'njmattes',
    'pass': 'ffVd2aK$$*2@',
    'form_build_id': 'form-b84d04d8132f2e2a5484f6f5a42563b9',
    'form_id':  'user_login_block',
}
data = urllib.urlencode(payload)
request = urllib2.Request(authentication_url, data)
response = urllib2.urlopen(request)

with open('utils/c2o_bibtex.bib', 'w') as f:
    for ty in itertools.product(TYPES, YEARS):
        urllib2.urlopen(URL+'Records/type/{}/year/{}/'.format(ty[0], ty[1]))
        bibtex = urllib2.urlopen(URL+'Records/export/bibtex/').read()
        print(len(bibtex), ty)
        f.write(bibtex)