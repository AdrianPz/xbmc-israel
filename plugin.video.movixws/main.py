# -*- coding: utf-8 -*-
import urllib,urllib2,sys,re,os,random,json
import xbmcaddon, xbmc, xbmcplugin, xbmcgui
import urlresolver
import repoCheck

__settings__ = xbmcaddon.Addon(id='plugin.video.movixws')
Domain = __settings__.getSetting("domain")
baseUrl = Domain[:-1] if Domain.endswith('/') else Domain
print baseUrl
autoPlay = __settings__.getSetting("autoPlay") == "true"

def searchWs():
	dialog = xbmcgui.Dialog()
	filter = dialog.select("בחר סוג חיפוש", ["הכל", "סרטים", "סדרות"])
	search_entered =''
	keyboard = xbmc.Keyboard(search_entered, 'הכנס מילות חיפוש כאן')
	keyboard.doModal()
	if keyboard.isConfirmed():
		search_entered = keyboard.getText()

	if search_entered !='' :
		if filter == 1:
			search_entered += "&sortby=movie"
		elif filter == 2:
			search_entered += "&sortby=tv-show"
		IndexPage('{0}/search_movies?q={1}'.format(baseUrl, search_entered))
	else:
		return

def IndexPage(url):
	if  'search_movies' in url:
		result=OPEN_URL(url)
		matches=re.compile('<div class=\"mov\".*? <img src="(.*?)".*?<h3><a href="(.*?)">(.*?)<.*?<p class=\"ic_text\">(.*?)<\/p>',re.I+re.M+re.U+re.S).findall(result)
		for match in matches:
			addDir(match[2],'{0}{1}'.format(baseUrl, match[1]), 4, match[0], True, match[3])
	else:
		if not 'page' in url:
			url=url+'/page/0'
		current_page=int(url.split('/')[-1])
		result=OPEN_URL(url)
		block=re.compile('pnation(.*?)<\/div>',re.I+re.M+re.U+re.S).findall(result)[0]
		last_page=int(re.compile('a href=".*?\/page\/(.*?)"',re.I+re.M+re.U+re.S).findall(block)[-1])
		stop=False
		i=current_page
		j=1
		while i<=last_page and not stop:
			result=OPEN_URL(url)
			matches=re.compile('<div class=\"mov\".*? <img src="(.*?)".*?<h3><a href="(.*?)">(.*?)<.*?<p class=\"ic_text\">(.*?)<\/p>',re.I+re.M+re.U+re.S).findall(result)
			for match in matches:
				addDir(match[2],'{0}{1}'.format(baseUrl, match[1]), 4, match[0], True, match[3])
			i+=15
			j+=1
			url=url[:url.rfind('/')+1]
			url+=str(i)
			if (j%10 ==0):
				stop=True
				addDir('[COLOR blue]'+'תוצאות נוספות'+'[/COLOR]',url,2,'',True,'')

def OPEN_URL(url, headers={}, user_data={}, referer=None, Host=None):
	link = ""
	if user_data:
		user_data = urllib.urlencode(user_data)
		req = urllib2.Request(url, user_data)
	else:
		req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	for k, v in headers.items():
		req.add_header(k, v)
	if referer:
		req.add_header('Referer' ,referer)
	if Host:
		req.add_header('Host' ,Host)
	try:
		response = urllib2.urlopen(req,timeout=100)
		link = response.read()
		response.close()
	except:
		return None
	return link

def ResolveUrl(url, type):
	link = None
	if type == "filehoot":
		url = url.replace("/embed-","/")
		url = "{0}.html".format(url[:url.rfind('-')])
		html = OPEN_URL(url)
		id = re.compile("http://filehoot.com/(.*?).html", re.I+re.M+re.U+re.S).findall(url)
		user_data = {'op':'download1','usr_login':'','id':id[0],'fname':'','referer':'','method_free':'Continue+to+watch+your+Video'}
		html = OPEN_URL(url, user_data=user_data)
		matches = re.compile("{file:'(.*?)'", re.I+re.M+re.U+re.S).findall(html)
		if len(matches) > 0:
			link = matches[0]
	elif type == "goodvideohost":
		url = url.replace("/embed-","/")
		html = OPEN_URL(url)

		url = re.compile('method="POST" action=\'(.*?)\'', re.I+re.M+re.U+re.S).findall(html)[0]
		op =  re.compile('name="op" value="(.*?)"', re.I+re.M+re.U+re.S).findall(html)[0]
		usr_login =  re.compile('name="usr_login" value="(.*?)"', re.I+re.M+re.U+re.S).findall(html)[0]
		id = re.compile('name="id" value="(.*?)"', re.I+re.M+re.U+re.S).findall(html)[0]
		fname =  re.compile('name="fname" value="(.*?)"', re.I+re.M+re.U+re.S).findall(html)[0]
		referer =  re.compile('name="referer" value="(.*?)"', re.I+re.M+re.U+re.S).findall(html)[0]
		hash = re.compile('name="hash" value="(.*?)"', re.I+re.M+re.U+re.S).findall(html)[0]
		imhuman =  re.compile('name="imhuman" value="(.*?)"', re.I+re.M+re.U+re.S).findall(html)[0]
		
		#user_data = {'op':'download1','usr_login':'','id':id[0],'fname':'','referer':'','hash':hash[0],'imhuman':'Proceed+to+video'}
		user_data = {'op':urllib.quote_plus(op),'usr_login':urllib.quote_plus(usr_login),'id':urllib.quote_plus(id),'fname':urllib.quote_plus(fname),'referer':urllib.quote_plus(referer),'hash':urllib.quote_plus(hash),'imhuman':urllib.quote_plus(imhuman)}
		html = OPEN_URL(url, user_data=user_data)

		matches = re.compile('{file:"(.*?)"', re.I+re.M+re.U+re.S).findall(html)
		if len(matches) > 0:
			link = matches[0]
	return link

def addDir(name,url,mode,iconimage,isFolder=True,description=''):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name , "Plot": str(description)} )
	if not isFolder:
		liz.setProperty("IsPlayable","true")
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=isFolder)
	return ok

def GetSeasons(series_num):
	result=OPEN_URL('{0}/watchmovies/get_seasons/{1}'.format(baseUrl, series_num))
	matches=re.compile('onclick=\"get_episodes\(\'(.*?)\'\);\">(.*?)<',re.I+re.M+re.U+re.S).findall(result)
	for season in matches:
		addDir('{0}  {1}'.format(name, season[1]), '{0}/watchmovies/get_episodes/{1}?seasonid={2}'.format(baseUrl, series_num, season[0]), 3, '', True)

def GetEpisodes(url):
	result=OPEN_URL(url)
	matches=re.compile('onclick=\"get_episode\(\'(.*?)\',\'(.*?)\'\);\">(.*?)<',re.I+re.M+re.U+re.S).findall(result)
	url=url.replace('get_episodes','get_episode')
	for episode in matches:
		addDir(name +'  '+episode[2],url+'&episodeid='+episode[1],4,url,True)

def LinksPage(url, iconimage):
	result=OPEN_URL(url)
	if  not 'get_seasons' in result:
		matches=re.compile('id="wrapserv"><a href="(.*?)" target=.*?src="\/img\/servers\/(.*?).png',re.I+re.M+re.U+re.S).findall(result)
		if autoPlay:
			playingUrlsList = []
			for match in matches:
				playingUrlsList.append(match[0])
			addDir('צפיה ב-"{0}"'.format(name), json.dumps(playingUrlsList), 7, iconimage, False)
		else:
			addDir('[COLOR red]'+'   בחר מקור לניגון, אם לא עובד נסה אחר '+'[/COLOR]','99',99,'',False)
			for match in matches:
				addDir(name +'  '+match[1],match[0],5,iconimage,False)
	else:
		series_num=url.split('-')[-1]
		GetSeasons(series_num)

def PlayWs(url):
	result=OPEN_URL(url)
	matches=re.compile('<IFRAME SRC="http:(.*?)" FRAMEBORDER',re.I+re.M+re.U+re.S).findall(result)
	url = 'http:{0}'.format(matches[0])
	if "filehoot" in url:
		new_url = ResolveUrl(url, "filehoot")
	elif "goodvideohost" in url:
		#new_url = ResolveUrl(url, "goodvideohost")
		new_url = None
	else:
		if "movreel" in url:
			url = url.replace("/embed-","/")
		item=urlresolver.HostedMediaFile(url)
		new_url = urlresolver.resolve(item.get_url())
	if new_url:
		listitem = xbmcgui.ListItem(path=new_url)
		xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
		return True
	else:
		if not autoPlay:
			dialog = xbmcgui.Dialog()
			ok = dialog.ok('OOOPS', 'Try a differnt Source')	
		return False

def AutoPlayUrl(urls):
	playingUrlsList = json.loads(urls)
	random.seed()
	random.shuffle(playingUrlsList)
	for playingUrl in playingUrlsList:
		if PlayWs(playingUrl):
			return
	dialog = xbmcgui.Dialog()
	ok = dialog.ok('OOOPS', 'לא נמצאו מקורות זמינים לניגון')

def Categories():
	addDir("Search - חפש"," ",6,'https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcQlAUVuxDFwhHYzmwfhcUEBgQXkkWi5XnM4ZyKxGecol952w-Rp')
	addDir("Movies - סרטים","{0}/movies".format(baseUrl),2,'http://www.aldeahostelcostarica.com/wp-content/uploads/2015/03/aldea_movie_day-500x300.jpg')
	addDir("Series - סדרות","{0}/series".format(baseUrl),2,'http://kibenterprise.com/media/catalog/category/TV_Series.png')
	addDir("Kids - ילדים","{0}/genres/Kids".format(baseUrl),2,'http://www.in-hebrew.co.il/images/logo-s.jpg')
	addDir("Animation - אנימציה","{0}/genres/Animation".format(baseUrl),2,'http://icons.iconarchive.com/icons/designbolts/free-movie-folder/256/Animated-icon.png')
	addDir("Fantasy - פנטזיה","{0}/genres/Fantasy".format(baseUrl),2,'http://blog.tapuz.co.il/girlkido/images/3472680_852.jpg')
	addDir("Family - משפחה","{0}/genres/Family".format(baseUrl),2,'http://pschools.haifanet.org.il/dror/DocLib1/%D7%99%D7%95%D7%9D%20%D7%9E%D7%A9%D7%A4%D7%97%D7%94%20%D7%A9%D7%9E%D7%97.jpg')
	addDir("Israeli - ישראלי","{0}/genres/israeli".format(baseUrl),2,'http://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Flag_of_Israel.svg/250px-Flag_of_Israel.svg.png')
	addDir("Comedy - קומדיה","{0}/genres/Comedy".format(baseUrl),2,'http://www.filmsite.org/images/comedy-genre.jpg')
	addDir("Drama - דרמה","{0}/genres/Drama".format(baseUrl),2,'http://comps.canstockphoto.com/can-stock-photo_csp11392197.jpg')
	addDir("Documentary - דוקומנטרי","{0}/genres/Documentary".format(baseUrl),2,'http://icons.iconarchive.com/icons/aaron-sinuhe/tv-movie-folder/512/Documentaries-National-Geographic-icon.png')
	addDir("Action - פעולה","{0}/genres/Action".format(baseUrl),2,'http://pmtips.net/wp-content/uploads/2012/02/action.jpg')
	addDir("Crime - פשע","{0}/genres/Crime".format(baseUrl),2,'http://drthurstone.com/wp-content/uploads/2014/07/Crime-Pix.jpg')
	addDir("Thriller - מתח","{0}/genres/Thriller".format(baseUrl),2,'http://becplmovies.files.wordpress.com/2011/06/thrillers_title12.jpg')
	addDir("War - מלחמה","{0}/genres/War".format(baseUrl),2,'http://cdn2.pitchfork.com/news/53502/0ff1bba7.jpg')
	addDir("Mystery - מיסתורין","{0}/genres/Mystery".format(baseUrl),2,'http://www.barronmind.com/WMHlogoweb.gif')
	addDir("Horror - אימה","{0}/genres/Horror".format(baseUrl),2,'https://cdn4.iconfinder.com/data/icons/desktop-halloween/256/Mask.png')
	addDir("Sci-Fi - מ.בדיוני","{0}/genres/Sci-Fi".format(baseUrl),2,'http://images.clipartpanda.com/sci-fi-clipart-peacealienbw.png')
	xbmc.executebuiltin('Container.SetViewMode(500)')

def get_params():
	param=[]
	paramstring=sys.argv[2]
	if len(paramstring)>=2:
		params=sys.argv[2]
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


params=get_params()
url=None
name=None
mode=None

try:
	url=urllib.unquote_plus(params["url"])
except:
	pass
try:
	name=urllib.unquote_plus(params["name"])
except:
	pass
try:
	mode=int(params["mode"])
except:
	pass
try:
	iconimage=urllib.unquote_plus(params["iconimage"])
except:
	pass
	

print "checkMode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

if mode==None or url==None or len(url)<1:
	repoCheck.UpdateRepo()
	Categories()
elif mode==2:
	IndexPage(url)
elif mode==3:
	GetEpisodes(url)
elif mode==4:
	LinksPage(url, iconimage)
elif mode==5:
	PlayWs(url)
elif mode==6:
	searchWs()
elif mode==7:
	AutoPlayUrl(url)
	
xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
if mode==None or url==None or len(url)<1:
	xbmc.executebuiltin("Container.SetViewMode(500)")
else:
	xbmc.executebuiltin('Container.SetViewMode(504)')
xbmcplugin.endOfDirectory(int(sys.argv[1]))