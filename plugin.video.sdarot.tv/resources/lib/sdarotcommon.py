# -*- coding: utf-8 -*-

'''
Created on 30/04/2011

@author: shai
'''
#__USERAGENT__ = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1'
__USERAGENT__ = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36'

__REFERER__ = 'http://www.sdarot.tv/templates/frontend/blue_html5/player/jwplayer.flash.swf'


import urllib,urllib2,re,xbmc,xbmcplugin,xbmcgui,xbmcaddon,os,sys,time, socket
import StringIO
import gzip
from operator import itemgetter, attrgetter

__settings__ = xbmcaddon.Addon(id='plugin.video.sdarot.tv')
__cachePeriod__ = __settings__.getSetting("cache")
__PLUGIN_PATH__ = __settings__.getAddonInfo('path')
__DEBUG__ = __settings__.getSetting("DEBUG") == "true"

def enum(**enums):
        return type('Enum', (), enums)

def getMatches(url, pattern):
        page = getData(url)
        matches=re.compile(pattern).findall(page)
        return matches   

def getParams(arg):
        param=[]
        paramstring=arg
        if len(paramstring)>=2:
            params=arg
            cleanedparams=params.replace('?','')
            if (params[len(params)-1]=='/'):
                params=params[0:len(params)-2]
            pairsofparams=cleanedparams.split('&')
            param={}
            for i in range(len(pairsofparams)):
                splitparams={}
                splitparams=pairsofparams[i].split('=')
                if (len(splitparams))==2:    
                    param[splitparams[0]]=splitparams[1]
                                
        return param
    
def addDir(name, url, mode, iconimage='DefaultFolder.png', elementId=None, summary='', fanart=''):
        u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + name
        if not elementId == None and not elementId == '':
            u += "&module=" + urllib.quote_plus(elementId)
        liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
        liz.setInfo(type="Video", infoLabels={ "Title": urllib.unquote(name), "Plot": urllib.unquote(summary)})
        if not fanart == '':
            liz.setProperty("Fanart_Image", fanart)
        ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
        return ok

def addVideoLink(name, url, mode, iconimage='DefaultFolder.png', summary = ''):
        u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + name
        liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
        liz.setInfo(type="Video", infoLabels={ "Title": urllib.unquote(name), "Plot": urllib.unquote(summary)})    
        liz.setProperty('IsPlayable', 'true')
        ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=False)
        return ok
    
def addLink(name, url, iconimage='DefaultFolder.png', sub=''):
        liz = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo(type="Video", infoLabels={ "Title": urllib.unquote(name), "Plot": urllib.unquote(sub)})
        ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=liz)
        return ok

def extractFromZip(gzipData):
    
    data = StringIO.StringIO(gzipData)

    gzipper = gzip.GzipFile(fileobj=data)
    html = gzipper.read()
    gzipper.close()
    return html
    
def getData_attempt(url, timeout=__cachePeriod__, name='', postData=None,referer=__REFERER__):
        print 'getData: url --> ' + url + '\npostData-->' + str(postData)
        if __DEBUG__:
            print 'name --> ' + name
        #temporary disabled the cache - cause problems with headers    
        if timeout > 9999999:
            if name == '':
                cachePath = xbmc.translatePath(os.path.join(__PLUGIN_PATH__, 'cache', 'pages', urllib.quote(url,"")))
            else:
                cachePath = xbmc.translatePath(os.path.join(__PLUGIN_PATH__, 'cache', 'pages', name))
            if (os.path.exists(cachePath) and (time.time()-os.path.getmtime(cachePath))/60/60 <= float(timeout)):
                f = open(cachePath, 'r')
                ret = f.read()
                f.close()
                if __DEBUG__:
                    print 'returned data from cache'
                return ret
        socket.setdefaulttimeout(15)
        req = urllib2.Request(url)
        req.add_header('User-Agent', __USERAGENT__)   
        req.add_header('X-Requested-With','XMLHttpRequest')
        req.add_header('Accept','application/json, text/javascript, */*; q=0.01')
        req.add_header('Accept-Encoding','gzip,deflate,sdch')
        req.add_header('Content-Type','application/x-www-form-urlencoded; charset=UTF-8')
        req.add_header('Connection','keep-alive')
        req.add_header('Origin','http://www.sdarot.tv')
        if (postData):
            req.add_header('Content-Length',len(postData))
        
        if referer: 
            req.add_header ('Referer',referer)
            
        if __DEBUG__:
            print "sent headers:" + str(req.headers)     
        response = urllib2.urlopen(url=req,timeout=10,data=postData)
        
        if __DEBUG__:
            print "received headers:" + str(response.info());
        
        if response.info().get('Content-Encoding') == 'gzip':
            buf = StringIO.StringIO( response.read())
            f = gzip.GzipFile(fileobj=buf)
            data = f.read()
            print "received gzip len " + str(len(data))
           
        else:
            data = response.read()

        if data:
            data = data.replace("\n","").replace("\t","").replace("\r","")   
                     
        try:
            print sys.modules["__main__"].cookiejar
            sys.modules["__main__"].cookiejar.save()
            
        except Exception,e:
            print e       
        
        if __DEBUG__:
            print "recieved data:" + str(data)
                       
        response.close()
        
        try:
            if timeout > 999999:
                f = open(cachePath, 'wb')
                f.write(data)
                f.close()
            if __DEBUG__:
                print data
            return data
        except:
            return data
    
def getData(url, timeout=__cachePeriod__, name='', postData=None,referer=__REFERER__):
        for i in range(1,3):
          print "getData: Attempt " + str(i)
          try:
            return getData_attempt(url, timeout, name, postData,referer)
          except urllib2.URLError, e:
            print e
            if (i == 3):
              raise e


def getImage(imageURL, siteName):
        imageName = getImageName(imageURL)
        cacheDir = xbmc.translatePath(os.path.join(__PLUGIN_PATH__, 'cache', 'images', siteName))
        cachePath = xbmc.translatePath(os.path.join(cacheDir, imageName))
        if not os.path.exists(cachePath):
            ## fetch the image and store it in the cache path
            if not os.path.exists(cacheDir):
                os.makedirs(cacheDir)
            urllib.urlretrieve(imageURL, cachePath)
        return cachePath
        
def getImageName(imageURL):
        idx = int(imageURL.rfind("/")) + 1
        return imageURL[idx:]


  
