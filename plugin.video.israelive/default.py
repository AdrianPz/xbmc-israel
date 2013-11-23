# -*- coding: utf-8 -*-
#code by o2ri \ avigdor based on benny123 project in navix.
import urllib,urllib2,sys,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc,os
AddonID = 'plugin.video.israelive'
libDir = os.path.join(xbmc.translatePath("special://home/addons/"), AddonID, 'resources', 'lib')
sys.path.insert(0, libDir)
import myFilmon,commonlive
from commonlive import *

def CATEGORIES():
    Announcements()
    addDir('עידן פלוס','https://dl.dropbox.com/u/94071174/Online/wow/DTT%2B.plx',2,'http://ftp5.bizportal.co.il/web/giflib/news/idan_plus_gay.jpg','')
    addDir('רדיו','https://dl.dropboxusercontent.com/u/94071174/Online/wow/SUB/Entertainment/IL%20Radio.plx',2,'http://www.binamica.co.il/english/data/images/Image/radio.jpg','')
    addDir('ילדים','https://dl.dropbox.com/u/94071174/Online/wow/Kids.plx',2,'http://4hdwall.com/wp-content/uploads/2012/09/HD-cartoon-wallpaper.jpg','')
    addDir('בידור','https://dl.dropboxusercontent.com/u/94071174/Online/wow/Entertainment.plx',2,'http://digitalmediafilms.webs.com/Variety%20of%20Your%20Favortie%20Channels.jpg','')
    addDir('סרטים','https://dl.dropbox.com/u/94071174/Online/wow/Movies.plx',2,'http://www.attractherdateher.com/wp-content/uploads/2012/08/movie_night.jpg','')
    addDir('מוזיקה','https://dl.dropbox.com/u/94071174/Online/wow/Music.plx',2,'http://www.hdwallpapers.in/wallpapers/dance_with_me_hd_wide-1920x1200.jpg','')
    addDir('חדשות','https://dl.dropbox.com/u/94071174/Online/wow/News.plx',2,'http://www.realtrends.com/application/view/theme/default/docs/scroll/blog6.jpg','')
    addDir('מדע וטבע','https://dl.dropbox.com/u/94071174/Online/wow/Science%20%26%20Nature.plx',2,'http://wallpapers.free-review.net/wallpapers/23/Nature_-_Wallpaper_for_Windows_7.jpg','')
    addDir('ספורט','https://dl.dropbox.com/u/94071174/Online/wow/Sport.plx',2,'http://4vector.com/i/free-vector-sport-vector-pack_098139_sportsvector%20pack.jpg','')
    addDir('עולם','https://dl.dropbox.com/u/94071174/Online/wow/World.plx',2,'http://www.icangiveyouhouse.com/audio/2010/09/world-in-black-and-white-hands-1.jpg','')

    if   os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.movie25'):
        addDir('iLive.to','plugin://plugin.video.movie25/?iconimage=https%3a%2f%2fraw.github.com%2fmash2k3%2fMashupArtwork%2fmaster%2fart%2filive.png&mode=119&name=iLive%20Streams&url=ilive',7,'https://raw.github.com/mash2k3/MashupArtwork/master/art/ilive.png','')
    else:
        addDir('[COLOR yellow]לחץ כאן להתקנת תוסף חסר[/COLOR]' ,'https://github.com/o2ri/xbmc-israel/blob/master/mash.zip?raw=true',8,'http://blog.missionmode.com/storage/post-images/critical-factor-missing.jpg','Mash23 addon')
            
    if    not os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.teledunet'):
         addDir('[COLOR yellow]לחץ כאן להתקנת תוסף חסר[/COLOR]' ,'http://mirrors.xmission.com/superrepo/Frodo/Video/plugin.video.teledunet/plugin.video.teledunet-1.1.0.zip',6,'http://blog.missionmode.com/storage/post-images/critical-factor-missing.jpg','Teleduent')
         
        

def update_view(url):

    ok=True        
    xbmc.executebuiltin('XBMC.Container.Update(%s)' % url )
    return ok
        
    
   
def ListLive(url):
        link=OPEN_URL(url)
        link=unescape(link)
        #print link
        matches1=re.compile('pe=(.*?)#',re.I+re.M+re.U+re.S).findall(link)
        print str(matches1[0]) + '\n'
        for match in matches1 :
            print "match=" + str(match)
            match=match+'#'
            if match.find('playlist') != 0 :
                regex='name=(.*?)URL=(.*?)#'
                matches=re.compile(regex,re.I+re.M+re.U+re.S).findall(match)
                print str(matches)
                for name,url in  matches:
                    thumb=''
                    i=name.find('thumb')
                    if i>0:
                        thumb=name[i+6:]
                        name=name[0:i]
		    print url
                    i=url.find('plugin.video.MyFilmOn')
		    if i >0:
                        addDir('[COLOR yellow]' +name+'[/COLOR]',url,3,thumb,'')
                    else:
                        addLink('[COLOR yellow]'+ name+'[/COLOR]',url,thumb,'')  
                
            else:
                regex='name=(.*?)URL=(.*?).plx'
                matches=re.compile(regex,re.I+re.M+re.U+re.S).findall(match)
                for name,url in matches:
                    url=url+'.plx'
                    if name.find('Radio') < 0 :
                        addDir('[COLOR blue]'+name+'[/COLOR]',url,2,'','')
               
        #setView('tvshows', 'default')

def play_Filmon(url):
    direct,fullName = myFilmon.GetUrlStream(url)
    playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
    playlist.clear()
    liz = xbmcgui.ListItem(fullName, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title":fullName} )
    liz.setProperty("IsPlayable","true")
    playlist.add(direct,liz)
    if not xbmc.Player().isPlayingVideo():
                xbmc.Player(xbmc.PLAYER_CORE_MPLAYER).play(playlist)



params=get_params()
url=None
name=None
mode=None
iconimage=None
description=None


try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:        
        mode=int(params["mode"])
except:
        pass
try:        
        description=urllib.unquote_plus(params["description"])
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "IconImage: "+str(iconimage)
   
        
#these are the modes which tells the plugin where to go
if mode==None or url==None or len(url)<1:
        CATEGORIES()

elif mode==2:
    ListLive(url)
elif mode==3:
    play_Filmon(url)
elif mode==4:
     downloader_is( )
elif mode==6:
        downloader_is('http://mirrors.xmission.com/superrepo/Frodo/Video/plugin.video.teledunet/plugin.video.teledunet-1.1.0.zip','Teleduent')
        downloader_is('https://github.com/downloads/hadynz/repository.arabic.xbmc-addons/repository.arabic.xbmc-addons-1.0.0.zip','Teleduent repo')
        CATEGORIES()
elif mode==7:
           update_view(url) 
elif mode==8:
           downloader_is(url,description)      
           CATEGORIES()
xbmcplugin.endOfDirectory(int(sys.argv[1]))
