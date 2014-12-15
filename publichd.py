
import bs4
from koditorrent import mechanize
import urllib2
import cookielib
import re
from koditorrent import plugin
from koditorrent.scrapers import scraper
from koditorrent.ga import tracked
from koditorrent.caching import cached_route
from koditorrent.utils import ensure_fanart
from koditorrent.library import library_context

username = "nom3kop"
password = "proyo1"
base_url = "https://publichd.to"

br = mechanize.Browser()
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

br.addheaders = [('User-agent', 'Chrome')]

br.open("%s/auth/login"%base_url)

br.select_form(nr=0)

br.form['username'] = "%s" % username
br.form['password'] = "%s" % password

br.submit()

@scraper("%s"%plugin.get_setting("publichd_label"), "%s"%plugin.get_setting("publichd_picture"))
@plugin.route("/publichd")
@ensure_fanart
@tracked


def publichd_index():
    yield{
            "label": "Movies",
            "path": plugin.url_for("get_movie_name", pageNumber=0),
            "is_playable": False,
          }

def get_movie_name(pageNumber):  
    soup = bs4.BeautifulSoup(br.open("%s/movies?/page=%s" % (base_url, pageNumber)).read())
    titles =[a.attrs.get('title') for a in soup.select('div.caption a[title]')]
    names = soup.findAll('div',{'class': 'caption'})
    new_titles =[]
    for title in titles:
        new_titles.append(title.rsplit(' ', 1)[0])
    for title in new_titles:
        yield{
              "label": "%s" % title,
              "path": "this is fake",
              "is_playable": False,
              }
    #return new_titles
'''
def get_movie_page_urls(pageNumber):
    soup = bs4.BeautifulSoup(br.open("%s/movies?/page=%s" % (base_url, pageNumber)).read())
    links = [a.attrs.get('href') for a in soup.select('div.caption a[href^=https://publichd]') ]
    return links

def get_movie_name(pageNumber):  
    soup = bs4.BeautifulSoup(br.open("%s/movies?/page=%s" % (base_url, pageNumber)).read())
    titles =[a.attrs.get('title') for a in soup.select('div.caption a[title]')]
    names = soup.findAll('div',{'class': 'caption'})
    new_titles =[]
    for title in titles:
        new_titles.append(title.rsplit(' ', 1)[0])
    return new_titles

def get_torrents_for_movie(link):
    soup = bs4.BeautifulSoup(br.open("%s" % link).read())
    links = [a.attrs.get('href') for a in soup.select('div.torrent-filename a[href^=https://publichd]') ]
    return links

def get_torrents_for_movie_name(link):
    titles=[]
    i=0
    html = br.open("%s" % link).read()
    soup = bs4.BeautifulSoup(html)
    names = soup.findAll('div',{'class': 'torrent-filename'})
    for name in names:
        size = soup.find("tbody").findAll("tr")[i].findAll("td")[3].getText()
        seeds = soup.find("tbody").findAll("tr")[i].findAll("td")[6].getText()
        leech = soup.find("tbody").findAll("tr")[i].findAll("td")[7].getText()
        titles.append(name.getText().replace("\n","") + " (%s) (S:%s) (L:%s)" % (size, seeds, leech))
        i=i+1
    return titles

def get_torrent_uri(link):
    html = br.open("%s" % link).read()
    soup = bs4.BeautifulSoup(html)
    links = [a.attrs.get('href') for a in soup.select('table.table.torrent-desc a[href^=magnet:?]')][0]
    print links
    return links
    
    
print(get_movie_page_urls(0))
print
print
print
print
print(get_movie_name(0))
links = get_movie_page_urls(0)
print
print
print links[0]
print(get_torrents_for_movie(links[0]))
print
print
print
print get_torrents_for_movie_name(links[0])

links1 = get_torrents_for_movie(links[0])
print get_torrent_uri(links1[0])
'''

