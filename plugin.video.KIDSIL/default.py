﻿# -*- coding: utf-8 -*-

import urllib,urllib2,sys,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc,os,random
import json
AddonID = 'plugin.video.KIDSIL' 
ADDON = xbmcaddon.Addon(id=AddonID)
libDir = os.path.join(xbmc.translatePath("special://home/addons/"), AddonID, 'resources', 'lib')
sys.path.insert(0, libDir)
import commonkids
from commonkids import *


def CATEGORIES():
        mes()
        if    not os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.supercartoons'):
              downloader_is('https://github.com/spoyser/spoyser-repo/raw/master/zips/repository.spoyser/repository.spoyser-1.0.5.zip','supercartoons repository')
              downloader_is('https://github.com/spoyser/spoyser-repo/blob/master/zips/plugin.video.supercartoons/plugin.video.supercartoons-1.0.4.zip?raw=true','supercartoons  addon')
              dlg = xbmcgui . Dialog ( )
              dlg.ok( "KIDSIL" , "צא מהתוסף וחזור כדי לראות את התוסף החדש")
        else:
              addDir('Super cartoons','plugin://plugin.video.supercartoons/?mode=400&page=1',8,'https://encrypted-tbn2.gstatic.com/images?q=tbn:ANd9GcQQoKkxPt4MxnzTqM-ChAH7My_OdIZQJ2U6CoXIeDzOkdMBaG8G','')
              

                
        if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.seretil'):
                #addDir('מדובבים seretil','plugin://plugin.video.seretil/?mode=4&name=&url=http%3A%2F%2Fseretil.me%2Fcategory%2F%25d7%25a1%25d7%25a8%25d7%2598%25d7%2599%25d7%259d-%25d7%259e%25d7%2593%25d7%2595%25d7%2591%25d7%2591%25d7%2599%25d7%259d%2Fpage%2F1%2F',8,'https://dl.dropboxusercontent.com/u/5461675/meduvavim1.png','')
                addDir('seretil מדובבים','plugin://plugin.video.seretil/?mode=211&name=%20%d7%90%d7%95%d7%a1%d7%a3%20%d7%a1%d7%a8%d7%98%d7%99%d7%9d%20%d7%9e%d7%93%d7%95%d7%91%d7%91%d7%99%d7%9d&url=http%3a%2f%2fseretil.me%2f%25D7%2590%25D7%2595%25D7%25A1%25D7%25A3-%25D7%25A1%25D7%25A8%25D7%2598%25D7%2599%25D7%259D-%25D7%259E%25D7%2593%25D7%2595%25D7%2591%25D7%2591%25D7%2599%25D7%259D%2f',8,'https://dl.dropboxusercontent.com/u/5461675/seretIL0.png','')
                addDir('seretil 2 מדובבים','plugin://plugin.video.seretil/?mode=211&name=%d7%90%d7%95%d7%a1%d7%a3%20%d7%9e%d7%a1%d7%a4%d7%a8%202%20%d7%a1%d7%a8%d7%98%d7%99%d7%9d%20%d7%9e%d7%93%d7%95%d7%91%d7%91%d7%99%d7%9d&url=http%3a%2f%2fseretil.me%2f%25D7%2590%25D7%2595%25D7%25A1%25D7%25A3-%25D7%2592%25D7%2593%25D7%2595%25D7%259C-%25D7%25A9%25D7%259C-%25D7%25A1%25D7%25A8%25D7%2598%25D7%2599%25D7%259D-%25D7%259E%25D7%25A6%25D7%2595%25D7%2599%25D7%25A8%25D7%2599%25D7%259D%25D7%259E%25D7%2593%25D7%2595%25D7%2591%25D7%2591%25D7%2599%25D7%259D%2f',8,'https://dl.dropboxusercontent.com/u/5461675/seretIL1.png','')
                         
        else:
                addDir('[COLOR red]seretil לא מותקן[/COLOR]','','','','')
        if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.gozlan.me'):        
                addDir('אנימציה גוזלן','plugin://plugin.video.gozlan.me/?mode=1&name=%d7%a1%d7%a8%d7%98%d7%99%20%d7%90%d7%a0%d7%99%d7%9e%d7%a6%d7%99%d7%94&url=http%3a%2f%2fanonymouse.org%2fcgi-bin%2fanon-www.cgi%2fhttp%3a%2f%2fgozlan.co%2f%2fsearch.html%3fg%3d%25D7%2590%25D7%25A0%25D7%2599%25D7%259E%25D7%25A6%25D7%2599%25D7%2594',8,'https://dl.dropboxusercontent.com/u/5461675/GOZLAN1.png','')
                addDir('משפחה גוזלן','plugin://plugin.video.gozlan.me/?mode=1&name=%d7%a1%d7%a8%d7%98%d7%99%20%d7%9e%d7%a9%d7%a4%d7%97%d7%94&url=http%3a%2f%2fanonymouse.org%2fcgi-bin%2fanon-www.cgi%2fhttp%3a%2f%2fgozlan.co%2f%2fsearch.html%3fg%3d%25D7%259E%25D7%25A9%25D7%25A4%25D7%2597%25D7%2594',8,'https://dl.dropboxusercontent.com/u/5461675/GOZLAN2.png','')
        else:
                 addDir('[COLOR red]GOZLAN לא מותקן[/COLOR]','','','','')
                 
        if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.10qtv'):
                addDir('10Q סרטי אנימציה ','plugin://plugin.video.10qtv/?mode=6&name=אנימציה&url=http://www.10q.tv/board/filmy/animciha/5',8,'https://dl.dropboxusercontent.com/u/5461675/10qtv.png','')
                addDir('10Q  ומשפחה סרטי אנימציה ','plugin://plugin.video.10qtv/?mode=6&name=אנימציה&url=http://www.10q.tv/board/filmy/mshfhha/17',8,'https://dl.dropboxusercontent.com/u/5461675/10qtv2.png','')
        else:
                addDir('[COLOR red]10QTV לא מותקן[/COLOR]','','','','')


        if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.wallaNew.video'):
                addDir('קלסיקלטת','plugin://plugin.video.wallaNew.video/?mode=1&module=338&name=קלסיקלטת&url=http://vod.walla.co.il/channel/338/clasicaletet',8,'https://encrypted-tbn2.gstatic.com/images?q=tbn:ANd9GcTYE2VT8CR2O31MsqAhdaydYrqrCD--HCCdGcs7blBn3Zh92Kwq','')
                addDir('ניק','plugin://plugin.video.wallaNew.video/?mode=1&module=nick&name=ניק&url=http://nick.walla.co.il/',8,'http://www.karmieli.co.il/sites/default/files/images/nico.jpg','')
                addDir('גוניור','plugin://plugin.video.wallaNew.video/?mode=1&module=junior&name=גוניור&url=http://junior.walla.co.il/',8,'http://upload.wikimedia.org/wikipedia/he/1/19/%D7%A2%D7%A8%D7%95%D7%A5_%D7%92%27%D7%95%D7%A0%D7%99%D7%95%D7%A8.jpg','')
                addDir('ניק גוניור ','plugin://plugin.video.wallaNew.video/?mode=1&module=nickjr&name=ניקלאודיון גוניור&url=http://nickjr.walla.co.il/',8,'http://www.imanoga.co.il/wp-content/uploads/2012/06/646457567.jpg','')
                addDir('וואלה ילדים','plugin://plugin.video.wallaNew.video/?mode=1&module=wallavod&name=י%d7%99%d7%9c%d7%93%d7%99%d7%9d&url=englishName%3dkids',8,'https://lh6.ggpht.com/V8v_FzkTMqeLRg_oY7G00zf0bcxubsm659cLrbf9nEKMLHQG-5LSZdbbJGQgkV6j1PQ=w300','')
        else:
                addDir('[COLOR red]וואלה לא מותקן[/COLOR]','','','','')
        if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.hotVOD.video'):
                addDir('HOT VOD YOUNG','plugin://plugin.video.hotVOD.video/?mode=5&name=%20HOT%20VOD%20YOUNG&url=http%3a%2f%2fhot.ynet.co.il%2fhome%2f0%2c7340%2cL-7449%2c00.html',8,'http://i28.tinypic.com/20o8lt.jpg','')
        else:
               addDir('[COLOR red]HOT VOD לא מותקן[/COLOR]','','','','')

        
        addDir('מצויירים קלאסיים','https://dl.dropboxusercontent.com/s/cwcptnocx310g00/Merry_Melodies.plx',7,'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSmzwydiY6V_l5sE_ed7Rf66G6B8Ug2p7ajn4uPAhH2NYpDVMNBUQ','')
        addDir('Baby Einstein','TerrapinStation5',9,'http://d202m5krfqbpi5.cloudfront.net/books/1170326163l/46377.jpg','1')
        addDir(' וידאו לילדים','UCnToIWbMbc9VehbtjTBBnRw',9,'http://www.iandroidil.net/icone/5718-icon.png','1')
        addDir('YES שירי','PLF11AD94724D37E02',13,'http://static.wixstatic.com/media/96e157_2b95d7111507dcbbf4d07a346b1a08bf.jpg_srz_261_263_85_22_0.50_1.20_0.00_jpg_srz','1')
        addDir('בייבי אוריינטל','PL4RuBaWCIgHrFNTIP37qBS254y7-2r9e4',13,'http://f0.bcbits.com/img/a2562115784_10.jpg','1')
        
        YOUsubs('UC5RJ8so5jivihrnHB5qrV_Q')
        #addDir('יוטיוב מרשת','reshettv',16,'','')
        addDir('יוטיוב מחינוכית 23','23tv',16,'','')
        setView('movies', 'default')







# reads  user names from my subscriptions 



def ShowFromUser(user):
    murl='https://gdata.youtube.com/feeds/api/users/'+user+'/shows?alt=json&start-index=1&max-results=50&v=2'
    resultJSON = json.loads(OPEN_URL(murl))
    shows=resultJSON['feed']['entry']
    hasNext= True
    while hasNext:
        shows=resultJSON['feed']['entry']
        for  i in range (0, len(shows)) :
            showApiUrl=shows[i]['link'][1]['href']
            showApiUrl=showApiUrl[:-4]+'/content?v=2&alt=json'
            showName=shows[i]['title']['$t'].encode('utf-8')
            image= shows[i]['media$group']['media$thumbnail'][-1]['url']
            addDir(showName,showApiUrl,14,image,'')
        hasNext= resultJSON['feed']['link'][-1]['rel'].lower()=='next'
        if hasNext:
            resultJSON = json.loads(OPEN_URL(resultJSON['feed']['link'][-1]['href']))
        
def SeasonsFromShow(showApiUrl):
    #print showApiUrl
    resultJSON = json.loads(OPEN_URL(showApiUrl))
    seasons=resultJSON['feed']['entry']
    for  i in range (0, len(seasons)) :
        #print seasons[i].keys()
        #print seasons[i]['title']['$t']
        for index,item in  enumerate(seasons[i]['gd$feedLink']) :
            if item['countHint'] !=0:
                resultJSON = json.loads(OPEN_URL( seasons[i]['gd$feedLink'][index]['href']+'&alt=json'))
                for  j in range (0, len(resultJSON['feed']['entry'])) :
                    title= str(resultJSON['feed'][u'entry'][j][ u'media$group'][u'media$title'][u'$t'].encode('utf-8')).decode('utf-8')
                    thumb =str(resultJSON['feed'][u'entry'][j][ u'media$group'][u'media$thumbnail'][-1][u'url'])
                    episode_num=resultJSON['feed']['entry'][j]['yt$episode']['number']
                    url= resultJSON['feed']['entry'][j]['link'][0]['href']
                    match=re.compile('www.youtube.com/watch\?v\=(.*?)\&f').findall(url)
                    finalurl="plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid="+match[0]+"&hd=1"
                    addLink(title+' '+episode_num ,finalurl,thumb,'')
                    
                    
        
def YOUsubs(user):
        murl='http://gdata.youtube.com/feeds/api/users/'+user+'/subscriptions?alt=json&start-index=1&max-results=50'
        resultJSON = json.loads(OPEN_URL(murl))
        feed=resultJSON['feed']['entry']
        for i in range (0, len(feed)) :
            image=str(feed[i]['media$thumbnail']['url'])
            name = feed[i]['title']['$t'].replace('Activity of:','').encode('utf-8')
            url=feed[i]['yt$channelId']['$t'].encode('utf-8')
            addDir(name,url,9,image,'1')
        setView('tvshows', 'default')
#list the links from  usernames based on mash23 + improvment
def YOUList(name,url,description):
        playlists=PlaylistsFromUser(url)
        if url=='TerrapinStation5' :
                addDir('[COLOR yellow]Playlist:[/COLOR]     Baby Einstein' ,'PLlBpB13l5PDCndYQPS4PHw5ElfKZMhgCE',12,'http://d202m5krfqbpi5.cloudfront.net/books/1170326163l/46377.jpg','')
        else:        
                for playlistid,title,thumb in playlists :
                        addDir('[COLOR yellow]Playlist:[/COLOR]                  ' + title,playlistid,12,thumb,'')
#                        print playlistid
        
        murl='http://gdata.youtube.com/feeds/api/users/'+url+'/uploads?&max-results=50&start-index='+description
        link=OPEN_URL(murl)
        addDir('[COLOR red]נגן כל התוצאות בעמוד זה [/COLOR]',murl,11,'',description)
        match=re.compile("http\://www.youtube.com/watch\?v\=([^\&]+)\&.+?<media\:descriptio[^>]+>([^<]+)</media\:description>.+?<media\:thumbnail url='([^']+)'.+?<media:title type='plain'>(.+?)/media:title>").findall(link)
        for nurl,desc,thumb,rname in match:
                rname=rname.replace('<','')
                YOULink(rname,nurl,thumb)
        description=int(description)+50
        addDir('[COLOR blue]            עוד תוצאות [/COLOR]',url,9,'',str(description))
        setView('tvshows', 'default')


def TvMode(user):
    playlists=PlaylistsFromUser(user)
    if playlists==[] :  #no playlists on  youtube channel
        dialog = xbmcgui.Dialog()
        ok = dialog.ok('XBMC', 'No TV mode for this Channel.')
        CATEGORIES()
    #print "str is" +  str(random.choice(playlists)[0])
    else:
        pl = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        pl.clear()
        dp= xbmcgui.DialogProgress()
        dp.create('KIDSIL BY o2Ri','Preapring TV mode')
        for i in range (1,21) :  #20  RANDOM PROGRAMS IN TV MODE 
            dp.update(i*5,"Please wait ","Will take few minutes")
            #print str (playlists)
            ran=str(random.choice(playlists)[0])
            print "kkkkkkkkkkkkkk"+str(ran)
            finalurl,title,thumb= RanFromPlayList(ran)
            liz = xbmcgui.ListItem(title, iconImage="DefaultVideo.png", thumbnailImage=thumb)
            liz.setInfo( type="Video", infoLabels={ "Title": title} )
            liz.setProperty("IsPlayable","true")
            pl.add(finalurl, liz)
        xbmc.Player(xbmc.PLAYER_CORE_MPLAYER).play(pl)
    
def YOULink(mname,url,thumb):
        ok=True
        url = "plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid="+url
        liz=xbmcgui.ListItem(mname, iconImage="DefaultVideo.png", thumbnailImage=thumb)
        liz.setInfo( type="Video", infoLabels={ "Title": mname, "Plot": description } )
        liz.setProperty("IsPlayable","true")
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,isFolder=False)
        return ok
def PlaylistsFromUser(user):
    url='https://gdata.youtube.com/feeds/api/users/'+user+ '/playlists?alt=json&max-results=50'
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    prms=json.loads(link)
    TotalPlaylists=int(prms['feed'][u'openSearch$totalResults'][u'$t'])
    i=0
    lst=[]
    while i<TotalPlaylists:
        thumb=''
        try:
                playlistid=str(prms['feed'][u'entry'][i][u'yt$playlistId'][u'$t'])
                title=str(prms['feed'][u'entry'][i][u'title'][u'$t'].encode('utf-8'))
                thumb=str(prms['feed'][u'entry'][i][u'media$group'][u'media$thumbnail'][2][u'url'])
        except:
                     pass
        i=i+1
        lst.append((playlistid,title,thumb))
    return lst

def ListPlaylist(playlistid): 
        url='https://gdata.youtube.com/feeds/api/playlists/'+playlistid+'?alt=json&max-results=50'
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        prms=json.loads(link)

        pl = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        pl.clear()
        playlist = []
        numOfItems=int(prms['feed'][u'openSearch$totalResults'][u'$t']) #if bigger than 50 needs  to add more result
        
        j=1
        h=1
        pages = (numOfItems //50)+1
        while  j<= pages:
                link=OPEN_URL(url)
                prms=json.loads(link)
                i=0
                while i< 50  and  h<numOfItems :
                        #print "i===" +str(i) +"numOfItems="+ str(numOfItems)
                        try:
                                urlPlaylist= str(prms['feed'][u'entry'][i][ u'media$group'][u'media$player'][0][u'url'])
                                match=re.compile('www.youtube.com/watch\?v\=(.*?)\&f').findall(urlPlaylist)
                                finalurl="plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid="+match[0]+"&hd=1"
                                title= str(prms['feed'][u'entry'][i][ u'media$group'][u'media$title'][u'$t'].encode('utf-8')).decode('utf-8')
                                thumb =str(prms['feed'][u'entry'][i][ u'media$group'][u'media$thumbnail'][2][u'url'])
                                addLink(title,finalurl,thumb,'')
                        except:
                                pass
                        i=i+1
                        h=h+1

                j=j+1
                url='https://gdata.youtube.com/feeds/api/playlists/'+playlistid+'?alt=json&max-results=50&start-index='+str (j*50-49)
	

def YOULinkAll(url):
    dp = xbmcgui.DialogProgress()
    dp.create("KIDSIL",'Creating Your Playlist')
    dp.update(0)
    pl = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
    pl.clear()
    link=OPEN_URL(url)
    match=re.compile("http\://www.youtube.com/watch\?v\=([^\&]+)\&.+?<media\:descriptio[^>]+>([^<]+)</media\:description>.+?<media\:thumbnail url='([^']+)'.+?<media:title type='plain'>(.+?)/media:title>").findall(link)
    playlist = []
    nItem    = len(match)

    for nurl,desc,thumb,rname in match:
         rname=rname.replace('<','')
         finalurl= "plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid="+nurl+"&hd=1"
         liz = xbmcgui.ListItem(rname, iconImage="DefaultVideo.png", thumbnailImage=thumb)
         liz.setInfo( type="Video", infoLabels={ "Title": rname} )
         liz.setProperty("IsPlayable","true")
         playlist.append((finalurl ,liz))
         progress = len(playlist) / float(nItem) * 100  
         dp.update(int(progress), 'Adding to Your Playlist',rname)
         if dp.iscanceled():
                return
    
    dp.close()
    for blob ,liz in playlist:
            try:
                if blob:
                    pl.add(blob,liz)
            except:
                pass
    
    if not xbmc.Player().isPlayingVideo():
	    xbmc.Player(xbmc.PLAYER_CORE_MPLAYER).play(pl)
        

        
def RanFromPlayList(playlistid):
        url='https://gdata.youtube.com/feeds/api/playlists/'+playlistid+'?alt=json&max-results=50'
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        prms=json.loads(link)
        numOfItems=int(prms['feed'][u'openSearch$totalResults'][u'$t']) #if bigger than 50 needs  to add more result
        if numOfItems >1 :
            link=OPEN_URL(url)
            prms=json.loads(link)
            if numOfItems>49:
                numOfItems=49
            i=random.randint(1, numOfItems-1)
            #print str (len(prms['feed'][u'entry']))  +"and i="+ str(i)
            try:
                urlPlaylist= str(prms['feed'][u'entry'][i][ u'media$group'][u'media$player'][0][u'url'])
                match=re.compile('www.youtube.com/watch\?v\=(.*?)\&f').findall(urlPlaylist)
                finalurl="plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid="+match[0]+"&hd=1"
                title= str(prms['feed'][u'entry'][i][ u'media$group'][u'media$title'][u'$t'].encode('utf-8')).decode('utf-8')
                thumb =str(prms['feed'][u'entry'][i][ u'media$group'][u'media$thumbnail'][2][u'url'])
            except :
                 return "","",""  # private video from youtube
            '''liz = xbmcgui.ListItem(title, iconImage="DefaultVideo.png", thumbnailImage=thumb)
            liz.setInfo( type="Video", infoLabels={ "Title": title} )
            liz.setProperty("IsPlayable","true")
            pl = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
            pl.clear()
            pl.add(finalurl, liz)'''
            #xbmc.Player(xbmc.PLAYER_CORE_MPLAYER).play(pl)
            return finalurl,title,thumb
        else:
            return "","",""
        
        
def PlayPlayList(playlistid):

        url='https://gdata.youtube.com/feeds/api/playlists/'+playlistid+'?alt=json&max-results=50'
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        prms=json.loads(link)

        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
        playlist1 = []
        numOfItems=int(prms['feed'][u'openSearch$totalResults'][u'$t']) #if bigger than 50 needs  to add more result
        
        j=1
        h=1
        pages = (numOfItems //50)+1
        while  j<= pages:
                link=OPEN_URL(url)
                prms=json.loads(link)
                i=0
                while i< 50  and  h<numOfItems :
                        try:
                                urlPlaylist= str(prms['feed'][u'entry'][i][ u'media$group'][u'media$player'][0][u'url'])
                                match=re.compile('www.youtube.com/watch\?v\=(.*?)\&f').findall(urlPlaylist)
                                finalurl="plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid="+match[0]+"&hd=1"
                                title= str(prms['feed'][u'entry'][i][ u'media$group'][u'media$title'][u'$t'].encode('utf-8')).decode('utf-8')
                                thumb =str(prms['feed'][u'entry'][i][ u'media$group'][u'media$thumbnail'][2][u'url'])
                                liz = xbmcgui.ListItem(title, iconImage="DefaultVideo.png", thumbnailImage=thumb)
                                liz.setInfo( type="Video", infoLabels={ "Title": title} )
                                liz.setProperty("IsPlayable","true")
                                playlist1.append((finalurl ,liz))
                        except:
                                pass
                        i=i+1
                        h=h+1

                j=j+1
                url='https://gdata.youtube.com/feeds/api/playlists/'+playlistid+'?alt=json&max-results=50&start-index='+str (j*50-49)
        random.shuffle(playlist1)
        for blob ,liz in playlist1:
            try:
                if blob:
                    playlist.add(blob,liz)
            except:
                pass
        playlist.shuffle()

        if not xbmc.Player().isPlayingVideo():
	    xbmc.Player(xbmc.PLAYER_CORE_MPLAYER).play(playlist)
        

 #https://gdata.youtube.com/feeds/api/users/polosoft/playlists (gets playlist fro, user) https://gdata.youtube.com/feeds/api/users/polosoft/playlists?alt=json
 #https://gdata.youtube.com/feeds/api/playlists/PLN0EJVTzRDL_53Jz8bhZl4m3UtkY2btbV?max-results=50?alt=json  (gets items in playlist)
 #https://gdata.youtube.com/feeds/api/playlists/PLN0EJVTzRDL_53Jz8bhZl4m3UtkY2btbV?max-results=50&alt=json
		
		


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
        print ""
        CATEGORIES()
       
elif mode==1:
        print ""+url
        Choose_series(url)
elif mode==2:
        series_land(url)
elif mode==3:
        play_episode(url)
elif mode==8:
           update_view(url)
elif mode==7:
           ListLive(url)
elif mode==9:
        YOUList(name,url,description)
elif mode==10:
        YOUsubs(url)
elif mode==11:
        YOULinkAll(url)
elif mode==12:
        PlayPlayList(url)
elif mode==13:
        ListPlaylist(url)
elif mode==14:       
        SeasonsFromShow(url)
elif mode==15:       
            CleanTheCache()
elif mode==16:       
    ShowFromUser(url)
elif mode==115:
    TvMode(url)
xbmcplugin.endOfDirectory(int(sys.argv[1]))
