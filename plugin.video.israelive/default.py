# -*- coding: utf-8 -*-
import xbmc, xbmcaddon, xbmcplugin, xbmcgui
import sys, os, time, datetime, re
import urllib

AddonID = "plugin.video.israelive"
Addon = xbmcaddon.Addon(AddonID)
if Addon.getSetting("unverifySSL") == "true":
	try:
		import ssl
		ssl._create_default_https_context = ssl._create_unverified_context
	except:
		pass
addonPath = xbmc.translatePath(Addon.getAddonInfo("path")).decode("utf-8")
libDir = os.path.join(addonPath, 'resources', 'lib')
sys.path.insert(0, libDir)
import common, myIPTV, checkUpdates, updateM3U, resolver

localizedString = Addon.getLocalizedString
AddonName = Addon.getAddonInfo("name")
icon = Addon.getAddonInfo('icon')
artDir = os.path.join(addonPath, 'resources', 'art')
__icon__ = os.path.join(artDir, "check2.png")
__icon2__= os.path.join(artDir, "signQuestionMark.png")

user_dataDir = xbmc.translatePath(Addon.getAddonInfo("profile")).decode("utf-8")
if not os.path.exists(user_dataDir):
	os.makedirs(user_dataDir)
FAV = os.path.join(user_dataDir, 'favorites.txt')
if not (os.path.isfile(FAV)):
	common.WriteList(FAV, [])
remoteSettings = common.GetRemoteSettings()
remoteSettingsFile = os.path.join(user_dataDir, "remoteSettings.txt")
if not os.path.isfile(remoteSettingsFile):
	common.UpdateFile(remoteSettingsFile, "remoteSettingsZip", remoteSettings, zip=True, forceUpdate=True)
	remoteSettings = common.ReadList(remoteSettingsFile)
if remoteSettings == []:
	xbmc.executebuiltin('Notification({0}, Cannot load settings, {1}, {2})'.format(AddonName, 5000, icon))
	sys.exit()
listsFile = os.path.join(user_dataDir, "israelive.list")
if not os.path.isfile(listsFile):
	common.UpdateChList(remoteSettings)
fullGuideFile = os.path.join(user_dataDir, 'fullGuide.txt')
iptvChannelsFile = os.path.join(user_dataDir, "iptv.m3u")
iptvGuideFile = os.path.join(user_dataDir, "guide.xml")
iptvLogosDir = os.path.join(user_dataDir, "logos")
categoriesFile =  os.path.join(user_dataDir, 'lists', 'categories.list')
selectedCategoriesFile =  os.path.join(user_dataDir, 'lists', 'selectedCategories.list')
useCategories = Addon.getSetting("useCategories") == "true"
useEPG = Addon.getSetting("useEPG") == "true"
if useEPG and not os.path.isfile(fullGuideFile):
	useEPG = False
epg = None

def CATEGORIES():
	common.CheckNewVersion(remoteSettings)

	addDir("[COLOR yellow][B][{0}][/B][/COLOR]".format(localizedString(30239).encode('utf-8')), 50, 'https://www.ostraining.com/cdn/images/coding/setting.png', background="http://3.bp.blogspot.com/-vVfHI8TbKA4/UBAbrrZay0I/AAAAAAAABRM/dPFgXAnF8Sg/s1600/retro-tv-icon.jpg")
	addDir("[COLOR {0}][B][{1}][/B][/COLOR]".format(Addon.getSetting("favColor"), localizedString(30000).encode('utf-8')), 16, 'http://cdn3.tnwcdn.com/files/2010/07/bright_yellow_star.png', background="http://3.bp.blogspot.com/-vVfHI8TbKA4/UBAbrrZay0I/AAAAAAAABRM/dPFgXAnF8Sg/s1600/retro-tv-icon.jpg")
	
	if useCategories:
		categories = common.ReadList(selectedCategoriesFile)
		ind = -1
		for category in categories:
			ind += 1
			try:
				if category.has_key("type") and category["type"] == "ignore":
					continue
				addDir("[COLOR {0}][B][{1}][/B][/COLOR]".format(Addon.getSetting("catColor"), category["name"].encode("utf-8")), 2, category["image"], background="http://3.bp.blogspot.com/-vVfHI8TbKA4/UBAbrrZay0I/AAAAAAAABRM/dPFgXAnF8Sg/s1600/retro-tv-icon.jpg", channelID=ind)
			except Exception as ex:
				xbmc.log("{0}".format(ex), 3)
	else:
		ListLive(categoryID="9999", iconimage="http://3.bp.blogspot.com/-vVfHI8TbKA4/UBAbrrZay0I/AAAAAAAABRM/dPFgXAnF8Sg/s1600/retro-tv-icon.jpg")
		
	SetViewMode()

def SetViewMode():
	if useEPG:
		xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
		viewMode = 504 if int(xbmc.getInfoLabel("System.BuildVersion")[:2]) < 17 else 55
		xbmc.executebuiltin("Container.SetViewMode({0})".format(viewMode))

def ListLive(categoryID=None, iconimage=None, chID=None, catChannels=None):
	if catChannels is None:
		catChannels = common.GetChannels(categoryID)

	groupChannels = []
	for channel in catChannels:
		if channel["type"] == 'ignore':
			continue
		matches = [groupChannels.index(x) for x in groupChannels if len(x) > 0 and x[0]["name"] == channel["name"]]
		if len(matches) == 1:
			groupChannels[matches[0]].append(channel)
		else:
			if chID is None or chID == channel['id']:
				groupChannels.append([channel])

	for channels in groupChannels:
		isGroupChannel = len(channels) > 1 and chID is None
		chs = [channels[0]] if isGroupChannel else channels
		for channel in chs:
			image = channel['image']
			description = ""
			channelName = channel['name'].encode("utf-8")
			background = None
			isTvGuide = False
			isFolder=True
			
			displayName, description, background, isTvGuide = GetProgrammeDetails(channelName, categoryID)

			if isGroupChannel:
				mode = 3
				displayName = displayName.replace('[COLOR {0}][B]'.format(Addon.getSetting("chColor")), '[COLOR {0}][B]['.format(Addon.getSetting("catColor")), 1).replace('[/B]', '][/B]', 1)
			elif channel["type"] == 'video' or channel["type"] == 'audio':
				mode = 10
				isFolder=False
			elif not useCategories and channel["type"] == 'playlist':
				mode = 2
				displayName = displayName.replace('[COLOR {0}][B]'.format(Addon.getSetting("chColor")), '[COLOR {0}][B]['.format(Addon.getSetting("catColor")), 1).replace('[/B]', '][/B]', 1)
				background = image
			else:
				continue
						
			if background is None or background == "":
				background = iconimage
				
			addDir(displayName, mode, image, description, isFolder=isFolder, background=background, isTvGuide=isTvGuide, channelID=channel["id"], categoryID=categoryID)

	SetViewMode()

def PlayChannelByID(chID=None, fromFav=False, channel=None):
	try:
		if channel is None:
			channel = common.ReadList(FAV)[int(chID)] if fromFav else common.GetChannelByID(chID)
		categoryID = 'Favourites' if fromFav else channel["group"]
		PlayChannel(channel["url"], channel["name"].encode("utf-8"), channel["image"].encode("utf-8"), categoryID)
	except Exception as ex:
		xbmc.log(str(ex), 3)
		
def PlayChannel(url, name, iconimage, categoryID):
	url = resolver.resolveUrl(url)
	if url is None:
		xbmc.log("Cannot resolve stream URL for channel '{0}'".format(urllib.unquote_plus(name)), 3)
		xbmc.executebuiltin("Notification({0}, Cannot resolve stream URL for channel '[COLOR {1}][B]{2}[/B][/COLOR]', {3}, {4})".format(AddonName, Addon.getSetting("chColor"), urllib.unquote_plus(name), 5000, __icon2__))
		return False
	
	channelName, programmeName, description = GetPlayingDetails(urllib.unquote_plus(name), categoryID)

	listItem = xbmcgui.ListItem(path=url)
	listItem.setInfo(type="Video", infoLabels={"mediatype": "movie", "studio": channelName, "title": programmeName, "plot": description, "tvshowtitle": channelName, "episode": "0", "season": "0"})
	if iconimage is not None:
		try:
			listItem.setArt({'thumb' : iconimage})
		except:
			listItem.setThumbnailImage(iconimage)
	
	xbmcplugin.setResolvedUrl(handle=int(sys.argv[1]), succeeded=True, listitem=listItem)
	return True

def GetPlayingDetails(channelName, categoryID):
	programmeName = "[COLOR {0}][B]{1}[/B][/COLOR]".format(Addon.getSetting("chColor"), channelName)
	if not useEPG:
		return programmeName, programmeName
	global epg
	if epg is None:
		epg = common.GetGuide(categoryID)
	programmes = GetProgrammes(epg, channelName)
	channelName = programmeName
	description = ''
	if len(programmes) > 0:
		programme = programmes[0]
		programmeName = '[COLOR {0}][B]{1}[/B][/COLOR] [COLOR {2}][{3}-{4}][/COLOR]'.format(Addon.getSetting("prColor"), programme["name"].encode('utf-8'), Addon.getSetting("timesColor"), datetime.datetime.fromtimestamp(programme["start"]).strftime('%H:%M'), datetime.datetime.fromtimestamp(programme["end"]).strftime('%H:%M'))
		if programmes[0]["description"] is not None:
			description = '{0}[CR]{1}'.format(programmeName, programmes[0]["description"].encode('utf-8'))
		if len(programmes) > 1:
			nextProgramme = programmes[1]
			channelName = "{0} - [COLOR {1}]Next: [B]{2}[/B][/COLOR] [COLOR {3}][{4}-{5}][/COLOR]".format(channelName, Addon.getSetting("nprColor"), nextProgramme["name"].encode("utf-8"), Addon.getSetting("timesColor"), datetime.datetime.fromtimestamp(nextProgramme["start"]).strftime('%H:%M'), datetime.datetime.fromtimestamp(nextProgramme["end"]).strftime('%H:%M'))
			description = '{0}[CR][CR]Next: [COLOR {1}][B]{2}[/B][/COLOR] [COLOR {3}][{4}-{5}][/COLOR]'.format(description, Addon.getSetting("prColor"), programmes[1]["name"].encode('utf-8'), Addon.getSetting("timesColor"), datetime.datetime.fromtimestamp(programmes[1]["start"]).strftime('%H:%M'), datetime.datetime.fromtimestamp(programmes[1]["end"]).strftime('%H:%M'))

	return channelName, programmeName, description

def ChannelGuide(chID, categoryID):
	epg = common.GetGuide(categoryID)
	if categoryID == 'Favourites':
		channel = common.ReadList(FAV)[int(chID)]
	else:
		channel = common.GetChannelByID(chID)
	channelName = channel["name"].encode("utf-8")
	programmes = GetProgrammes(epg, channelName, full=True)
	ShowGuide(programmes, channelName, channel["image"].encode("utf-8"))

def ShowGuide(programmes, channelName, iconimage):
	if programmes is None or len(programmes) == 0:
		addDir('[COLOR red][B]{0}[/B] "{1}".[/COLOR]'.format(localizedString(30204).encode('utf-8'), channelName), 99, iconimage, isFolder=False)
	else:
		addDir('------- [B][COLOR {0}]{1}[/COLOR] - [COLOR {2}]{3}[/COLOR][/B] -------'.format(Addon.getSetting("chColor"), channelName, Addon.getSetting("prColor"), localizedString(30205).encode('utf-8')), 99, iconimage, isFolder=False)
		day = ""
		for programme in programmes:
			startdate = datetime.datetime.fromtimestamp(programme["start"]).strftime('%d/%m/%y')
			if startdate != day:
				day = startdate
				addDir('[COLOR {0}][B]{1}:[/B][/COLOR]'.format(Addon.getSetting("nprColor"), day), 99, iconimage, isFolder=False)
			startdatetime = datetime.datetime.fromtimestamp(programme["start"]).strftime('%H:%M')
			enddatetime = datetime.datetime.fromtimestamp(programme["end"]).strftime('%H:%M')
			programmeName = "[COLOR {0}][{1}-{2}][/COLOR] [COLOR {3}][B]{4}[/B][/COLOR]".format(Addon.getSetting("timesColor"), startdatetime, enddatetime, Addon.getSetting("prColor"), programme["name"].encode('utf-8'))
			description = "" if programme["description"] is None else programme["description"].encode('utf-8')
			image = programme["image"] if programme["image"] else iconimage
			addDir(programmeName, 99, image, description, isFolder=False)
		
	SetViewMode()

def GetProgrammeDetails(channelName, categoryID):
	global epg
	displayName = "[COLOR {0}][B]{1}[/B][/COLOR]".format(Addon.getSetting("chColor"), channelName)
	description = ""
	background = None
	isTvGuide = False
	if useEPG:
		if epg is None:
			epg = common.GetGuide(categoryID)
		programmes = GetProgrammes(epg, channelName)

		if programmes is not None and len(programmes) > 0:
			isTvGuide = True
			programmeName = "[COLOR {0}][B]{1}[/B][/COLOR] [COLOR {2}][{3}-{4}][/COLOR]".format(Addon.getSetting("prColor"), programmes[0]["name"].encode('utf-8'), Addon.getSetting("timesColor"), datetime.datetime.fromtimestamp(programmes[0]["start"]).strftime('%H:%M'), datetime.datetime.fromtimestamp(programmes[0]["end"]).strftime('%H:%M'))
			displayName = "{0} - {1}".format(displayName, programmeName)
			if programmes[0]["description"] is not None:
				description = '{0}[CR]{1}'.format(programmeName, programmes[0]["description"].encode('utf-8'))
			if programmes[0]["image"] is not None:
				background = programmes[0]["image"]
			if len(programmes) > 1:
				displayName = "{0} - [COLOR {1}]Next: [B]{2}[/B][/COLOR] [COLOR {3}][{4}-{5}][/COLOR]".format(displayName, Addon.getSetting("nprColor"), programmes[1]["name"].encode('utf-8'), Addon.getSetting("timesColor"), datetime.datetime.fromtimestamp(programmes[1]["start"]).strftime('%H:%M'), datetime.datetime.fromtimestamp(programmes[1]["end"]).strftime('%H:%M'))
				description = '{0}[CR][CR]Next: [COLOR {1}][B]{2}[/B][/COLOR] [COLOR {3}][{4}-{5}][/COLOR]'.format(description, Addon.getSetting("prColor"), programmes[1]["name"].encode('utf-8'), Addon.getSetting("timesColor"), datetime.datetime.fromtimestamp(programmes[1]["start"]).strftime('%H:%M'), datetime.datetime.fromtimestamp(programmes[1]["end"]).strftime('%H:%M'))
				
	return displayName, description, background, isTvGuide
		
def GetProgrammes(epg, channelName ,full=False):
	programmes = []
	try:
		matches = [x["tvGuide"] for x in epg if x["channel"].encode('utf-8').strip() == common.GetUnColor(channelName)]
		programmes = matches[0]
	except Exception, e:
		pass

	now = int(time.time())
	programmesCount = len(programmes)

	for i in range(programmesCount):
		start = programmes[i]["start"]
		stop = programmes[i]["end"]
		if now >= stop:
			continue
		if now < start:
			newStart = now if i == 0 else programmes[i-1]["end"]
			programme = {"start": newStart, "end": programmes[i]["start"], "name": "No Details", "description": None, "image": None}
			programmes.insert(i, programme)
			
		if (full):
			return programmes[i:]
		elif i+1 < programmesCount: 
			return programmes[i:i+2]
		else:
			return programmes[i:i+1]
	return []

def listFavorites():
	favsList = common.ReadList(FAV)
	if favsList == []:
		addDir('[COLOR red]{0}[/COLOR]'.format(localizedString(30202).encode('utf-8')), 99, isFolder=False)
		addDir('[COLOR red]{0}[/COLOR]'.format(localizedString(30203).encode('utf-8')), 99, isFolder=False)
	ind = -1
	for favourite in favsList:
		ind += 1
		if favourite["type"] == "ignore":
			continue
		channelName = common.GetUnColor(favourite["name"].encode("utf-8"))
		image = favourite["image"].encode("utf-8")
		description = None
		background = None
		isTvGuide = False
		displayName, description, background, isTvGuide = GetProgrammeDetails(channelName, "Favourites")
		addDir(displayName, 11, image, description, isFolder=False, background=background, isTvGuide=isTvGuide, channelID=ind, categoryID="Favourites")
	SetViewMode()

def addFavorites(channels, showNotification=True):
	favsList = common.ReadList(FAV)
	
	for channel in channels:
		if any(f.get('id', '') == channel["id"] for f in favsList):
			if showNotification:
				xbmc.executebuiltin('Notification({0}, [COLOR {1}][B]{2}[/B][/COLOR]  Already in favourites, {3}, {4})'.format(AddonName, Addon.getSetting("chColor"), channel["name"].encode("utf-8"), 5000, __icon2__))
			continue
		favsList.append(channel)
		if showNotification:
			xbmc.executebuiltin('Notification({0}, [COLOR {1}][B]{2}[/B][/COLOR]  added to favourites, {3}, {4})'.format(AddonName, Addon.getSetting("chColor"), channel["name"].encode("utf-8"), 5000, __icon__))
	common.WriteList(FAV, favsList)
	common.MakeFavouritesGuide(fullGuideFile)

def removeFavorties(indexes):
	favsList = common.ReadList(FAV)
	for ind in range(len(indexes)-1, -1, -1):
		favsList.remove(favsList[indexes[ind]])
	common.WriteList(FAV, favsList)
	common.MakeFavouritesGuide(fullGuideFile)

def SaveGuide():
	try:
		xbmc.executebuiltin("XBMC.Notification({0}, Saving Guide..., {1}, {2})".format(AddonName, 300000 ,icon))
		if common.UpdateFile(fullGuideFile, "fullGuide", remoteSettings, zip=True, forceUpdate=True):
			xbmc.executebuiltin("XBMC.Notification({0}, Guide saved., {1}, {2})".format(AddonName, 5000 ,icon))
			epg = common.ReadList(fullGuideFile)
			fullCategoriesList =  common.ReadList(categoriesFile)
			fullCategoriesList.append({"id": "Favourites"})
			common.MakeCatGuides(fullCategoriesList, epg)
		else:			
			xbmc.executebuiltin("XBMC.Notification({0}, Guide is up to date., {1}, {2})".format(AddonName, 5000 ,icon))
		return True
	except Exception as ex:
		xbmc.log("{0}".format(ex), 3)
		xbmc.executebuiltin("XBMC.Notification({0}, Guide NOT saved!, {1}, {2})".format(AddonName, 5000 ,icon))
		return False

def addDir(name, mode, iconimage=None, description=None, background=None, isFolder=True, isTvGuide=False, channelID=None, categoryID=None):
	try:
		liz=xbmcgui.ListItem(name)
		liz.setArt({'thumb' : iconimage, 'icon': 'DefaultFolder.png'})
	except:
		liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
		
	liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description} )
	
	if mode==10 or mode==11:
		liz.setProperty("IsPlayable","true")
		items = []

		if mode == 10:
			if isTvGuide:
				items.append((localizedString(30205).encode('utf-8'), 'XBMC.Container.Update({0}?mode=5&channelid={1}&categoryid={2})'.format(sys.argv[0], channelID, categoryID)))
			items.append((localizedString(30206).encode('utf-8'), 'XBMC.RunPlugin({0}?mode=17&channelid={1}&categoryid={2})'.format(sys.argv[0], channelID, categoryID)))
		elif mode == 11:
			if isTvGuide:
				items.append((localizedString(30205).encode('utf-8'), 'XBMC.Container.Update({0}?mode=5&channelid={1}&categoryid={2})'.format(sys.argv[0], channelID, categoryID)))
			items.append((localizedString(30207).encode('utf-8'), 'XBMC.RunPlugin({0}?mode=18&channelid={1})'.format(sys.argv[0], channelID)))
			items.append((localizedString(30021).encode('utf-8'), 'XBMC.RunPlugin({0}?mode=41&channelid={1}&iconimage=-1)'.format(sys.argv[0], channelID)))
			items.append((localizedString(30022).encode('utf-8'), 'XBMC.RunPlugin({0}?mode=41&channelid={1}&iconimage=1)'.format(sys.argv[0], channelID)))
			items.append((localizedString(30023).encode('utf-8'), 'XBMC.RunPlugin({0}?mode=41&channelid={1}&iconimage=0)'.format(sys.argv[0], channelID)))

		liz.addContextMenuItems(items = items)
		
	elif mode == 2:
		items = []
		items.append((localizedString(30210).encode('utf-8'), 'XBMC.Container.Update({0}?mode=37&categoryid={1})'.format(sys.argv[0], channelID)))
		items.append((localizedString(30212).encode('utf-8'), 'XBMC.Container.Update({0}?mode=38&categoryid={1})'.format(sys.argv[0], channelID)))
		if useCategories:
			items.append((localizedString(30021).encode('utf-8'), 'XBMC.RunPlugin({0}?mode=42&channelid={1}&iconimage=-1)'.format(sys.argv[0], channelID)))
			items.append((localizedString(30022).encode('utf-8'), 'XBMC.RunPlugin({0}?mode=42&channelid={1}&iconimage=1)'.format(sys.argv[0], channelID)))
			items.append((localizedString(30023).encode('utf-8'), 'XBMC.RunPlugin({0}?mode=42&channelid={1}&iconimage=0)'.format(sys.argv[0], channelID)))
		liz.addContextMenuItems(items = items)
	
	elif mode == 3:
		iconimage = background
	
	elif mode == 16:
		liz.addContextMenuItems(items = 
			[(localizedString(30211).encode('utf-8'), 'XBMC.Container.Update({0}?mode=39)'.format(sys.argv[0])),
			(localizedString(30213).encode('utf-8'), 'XBMC.Container.Update({0}?mode=40)'.format(sys.argv[0])),
			(localizedString(30224).encode('utf-8'), 'XBMC.Container.Update({0}?mode=45)'.format(sys.argv[0]))])
	
	if background is not None:
		liz.setProperty("Fanart_Image", background)

	if iconimage is None: iconimage = 'DefaultFolder.png'
	fullUrl = "{0}?mode={1}&iconimage={2}&channelid={3}".format(sys.argv[0], mode, urllib.quote_plus(iconimage),channelID)
	if categoryID is not None:
		fullUrl = "{0}&categoryid={1}".format(fullUrl, urllib.quote_plus(categoryID))
	xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=fullUrl, listitem=liz, isFolder=isFolder)

def UpdateChannelsLists():
	xbmc.executebuiltin("XBMC.Notification({0}, Updating Channels Lists..., {1}, {2})".format(AddonName, 300000 ,icon))
	common.UpdateFile(remoteSettingsFile, "remoteSettingsZip", zip=True, forceUpdate=True)
	remoteSettings = common.ReadList(remoteSettingsFile)
	if remoteSettings == []:
		xbmc.executebuiltin('Notification({0}, Cannot load settings, {1}, {2})'.format(AddonName, 5000, icon))
		sys.exit()

	common.UpdateChList(remoteSettings)
	xbmc.executebuiltin("XBMC.Notification({0}, Channels Lists updated., {1}, {2})".format(AddonName, 5000 ,icon))

def MakeIPTVlists():
	xbmc.executebuiltin("XBMC.Notification({0}, Making IPTV channels list..., {1}, {2})".format(AddonName, 300000 ,icon))
	if not os.path.isfile(listsFile):
		common.UpdateChList()
	myIPTV.makeIPTVlist(iptvChannelsFile)
	xbmc.executebuiltin("XBMC.Notification({0}, Making IPTV TV-guide..., {1}, {2})".format(AddonName, 300000 ,icon))
	myIPTV.MakeChannelsGuide(fullGuideFile, iptvGuideFile)
	myIPTV.RefreshPVR(iptvChannelsFile, iptvGuideFile, iptvLogosDir)
	xbmc.executebuiltin("XBMC.Notification({0}, IPTV channels list and TV-guide created., {1}, {2})".format(AddonName, 5000 ,icon))

def DownloadLogos():
	if myIPTV.GetIptvType() > 1:
		return
	xbmc.executebuiltin("XBMC.Notification({0}, Downloading channels logos..., {1}, {2})".format(AddonName, 300000 ,icon))
	if not os.path.isfile(listsFile):
		common.UpdateChList()
	myIPTV.SaveChannelsLogos(iptvLogosDir)
	xbmc.executebuiltin("XBMC.Notification({0}, Channels logos saved., {1}, {2})".format(AddonName, 5000 ,icon))

def UpdateIPTVSimple():
	xbmc.executebuiltin("XBMC.Notification({0}, Updating IPTVSimple settings..., {1}, {2})".format(AddonName, 300000 ,icon))
	myIPTV.RefreshPVR(iptvChannelsFile, iptvGuideFile, iptvLogosDir, forceUpdate=True)
	xbmc.executebuiltin("XBMC.Notification({0}, IPTVSimple settings updated., {1}, {2})".format(AddonName, 5000 ,icon))

def CleanLogosFolder():
	if not os.path.exists(iptvLogosDir):
		return
	xbmc.executebuiltin("XBMC.Notification({0}, Cleaning channels logos folder..., {1}, {2})".format(AddonName, 300000 ,icon))
	for the_file in os.listdir(iptvLogosDir):
		file_path = os.path.join(iptvLogosDir, the_file)
		try:
			if os.path.isfile(file_path):
				os.unlink(file_path)
		except Exception as ex:
			xbmc.log("{0}".format(ex), 3)
	xbmc.executebuiltin("XBMC.Notification({0}, Channels logos folder cleaned., {1}, {2})".format(AddonName, 5000 ,icon))

def RefreshLiveTV():
	UpdateChannelsLists()
	SaveGuide()
	MakeIPTVlists()
	DownloadLogos()

def AddCategories():
	if not os.path.isfile(categoriesFile):
		common.UpdateChList()
	allCatList = common.ReadList(categoriesFile)
	selectedCatList = common.ReadList(selectedCategoriesFile)
	categories = common.GetUnSelectedList(allCatList, selectedCatList)
	categoriesNames = [u"[COLOR {0}][B][{1}][/B][/COLOR]".format(Addon.getSetting("catColor"), item["name"]) for item in categories]
	selected = common.GetMultiChoiceSelected(localizedString(30503).encode('utf-8'), categoriesNames)
	if len(selected) < 1:
		return
	selectedList = [categories[item] for item in selected]
	common.WriteList(selectedCategoriesFile, selectedCatList + selectedList)

def RemoveCategories():
	if not os.path.isfile(categoriesFile):
		common.UpdateChList()
	
	selectedCatList = common.ReadList(selectedCategoriesFile)
	categories = [u"[COLOR {0}][B][{1}][/B][/COLOR]".format(Addon.getSetting("catColor"), item["name"]) for item in selectedCatList]
	selected = common.GetMultiChoiceSelected(localizedString(30503).encode('utf-8'), categories)
	if len(selected) < 1:
		return
	for ind in range(len(selected)-1, -1, -1):
		selectedCatList.remove(selectedCatList[selected[ind]])
		
	common.WriteList(selectedCategoriesFile, selectedCatList)

def AddFavoritesFromCategory(categoryID):
	channels = common.GetChannels(categoryID)
	channels = [channel for channel in channels if channel["type"] == "video" or channel["type"] == "audio"]
	channelsNames = [u"[COLOR {0}][B]{1}[/B][/COLOR]".format(Addon.getSetting("chColor"), channel["name"]) for channel in channels]
	selected = common.GetMultiChoiceSelected(localizedString(30208).encode('utf-8'), channelsNames)
	if len(selected) < 1:
		return
	selectedList = [channels[index] for index in selected]
	xbmc.executebuiltin('Notification({0}, Start adding channels to favourites, {1}, {2})'.format(AddonName, 5000, icon))
	addFavorites(selectedList, showNotification=False)
	common.MakeFavouritesGuide(fullGuideFile)
	xbmc.executebuiltin('Notification({0}, Channels added to favourites, {1}, {2})'.format(AddonName, 5000, __icon__))

def AddCategoryToFavorites(categoryID):
	allCatList = common.ReadList(categoriesFile)
	category = [u"[COLOR {0}][B][{1}][/B][/COLOR]".format(Addon.getSetting("catColor"), item["name"]) for item in allCatList if item['id'] == categoryID]
	channels = common.GetChannels(categoryID)
	if not common.YesNoDialog(localizedString(30210).encode('utf-8'), localizedString(30221).encode('utf-8'), localizedString(30222).encode('utf-8').format(category[0].encode('utf-8'), len(channels)), localizedString(30223).encode('utf-8'), nolabel=localizedString(30002).encode('utf-8'), yeslabel=localizedString(30001).encode('utf-8')):
		return
	xbmc.executebuiltin('Notification({0}, Start adding channels to favourites, {1}, {2})'.format(AddonName, 5000, icon))
	addFavorites(channels, showNotification=False)
	common.MakeFavouritesGuide(fullGuideFile)
	xbmc.executebuiltin('Notification({0}, Channels added to favourites, {1}, {2})'.format(AddonName, 5000, __icon__))

def AddUserChannelToFavorites():
	chName = common.GetKeyboardText(localizedString(30225).encode('utf-8')).strip()
	if len(chName) < 1:
		return
	chUrl = common.GetKeyboardText(localizedString(30226).encode('utf-8')).strip()
	if len(chUrl) < 1:
		return
	
	if not os.path.isfile(categoriesFile):
		common.UpdateChList()
	categories = common.ReadList(categoriesFile)
	categoriesNames = [u"[COLOR {0}][B][{1}][/B][/COLOR]".format(Addon.getSetting("catColor"), item["name"]) for item in categories]
	categoryInd = common.GetMenuSelected(localizedString(30227).encode('utf-8'), categoriesNames)
	if categoryInd == -1:
		return
	group = categories[categoryInd]["id"]
	chTypeInd = common.GetMenuSelected(localizedString(30232).encode('utf-8'), [localizedString(30233).encode('utf-8'), localizedString(30234).encode('utf-8')])
	if chTypeInd == 0:
		chType = "video"
	elif chTypeInd == 1: 
		chType = "audio"
	else:
		return
	logoInd = common.GetMenuSelected(localizedString(30228).encode('utf-8'), [localizedString(30229).encode('utf-8'), localizedString(30230).encode('utf-8'), localizedString(30231).encode('utf-8')])
	if logoInd == 0:
		logoFile = common.GetKeyboardText(localizedString(30229).encode('utf-8')).strip()
		if len(logoFile) < 1:
			return
	elif logoInd == 1:
		logoFile = xbmcgui.Dialog().browse(2, localizedString(30230).encode('utf-8'), 'myprograms')
		if logoFile is None or len(logoFile) < 1:
			return
	elif logoInd == 2:
		logoFile = ""
	else:
		return
		
	favsList = common.ReadList(FAV)
	for channel in favsList:
		if channel["url"].lower() == chUrl.lower():
			xbmc.executebuiltin('Notification({0}, [COLOR {1}][B]{2}[/B][/COLOR]  Already in favourites, {3}, {4})'.format(AddonName, Addon.getSetting("chColor"), chName, 5000, __icon2__))
			return
		
	data = {"url": chUrl.decode("utf-8"), "group": group, "image": logoFile.decode("utf-8"), "type": chType, "name": chName.decode("utf-8")}
	
	favsList.append(data)
	if common.WriteList(FAV, favsList):
		xbmc.executebuiltin('Notification({0}, [COLOR {1}][B]{2}[/B][/COLOR]  added to favourites, {3}, {4})'.format(AddonName, Addon.getSetting("chColor"), chName, 5000, __icon__))

def RemoveSelectedFavorties():
	allCategories = common.ReadList(categoriesFile)
	channels = common.ReadList(FAV)
	channelsNames = []
	for channel in channels:
		gp = [x["name"] for x in allCategories if x["id"] == channel.get("group", "")]
		groupName = gp[0] if len(gp) > 0 else 'Favourites'
		channelsNames.append(u"[COLOR {0}][B]{1}[/B][/COLOR] [COLOR {2}][B][{3}][/B][/COLOR]".format(Addon.getSetting("chColor"), channel["name"], Addon.getSetting("catColor"), groupName))
	selected = common.GetMultiChoiceSelected(localizedString(30209).encode('utf-8'), channelsNames)
	if len(selected) < 1:
		return
	xbmc.executebuiltin('Notification({0}, Start removing channels from favourites, {1}, {2})'.format(AddonName, 5000, icon))
	removeFavorties(selected)
	common.MakeFavouritesGuide(fullGuideFile)
	xbmc.executebuiltin('Notification({0}, Channels removed trom favourites, {1}, {2})'.format(AddonName, 5000, __icon__))

def EmptyFavorties():
	if not common.YesNoDialog(localizedString(30213).encode('utf-8'), localizedString(30220).encode('utf-8'), "", "", nolabel=localizedString(30002).encode('utf-8'), yeslabel=localizedString(30001).encode('utf-8')):
		return
	xbmc.executebuiltin('Notification({0}, Start removing channels from favourites, {1}, {2})'.format(AddonName, 5000, icon))
	common.WriteList(FAV, [])
	common.MakeFavouritesGuide(fullGuideFile)
	xbmc.executebuiltin('Notification({0}, Channels removed trom favourites, {1}, {2})'.format(AddonName, 5000, __icon__))

def MoveInList(index, step, listFile):
	theList = common.ReadList(listFile)
	if index + step >= len(theList) or index + step < 0:
		return
	
	if step == 0:
		step = GetIndexFromUser(len(theList), index)
		
	
	if step < 0:
		tempList = theList[0:index + step] + [theList[index]] + theList[index + step:index] + theList[index + 1:]
	elif step > 0:
		tempList = theList[0:index] + theList[index +  1:index + 1 + step] + [theList[index]] + theList[index + 1 + step:]
	else:
		return

	common.WriteList(listFile, tempList)
	xbmc.executebuiltin("XBMC.Container.Refresh()")

def GetIndexFromUser(listLen, index):
	dialog = xbmcgui.Dialog()
	location = dialog.input('{0} (1-{1})'.format(localizedString(30024).encode('utf-8'), listLen), type=xbmcgui.INPUT_NUMERIC)
	if location is None or location == "":
		return 0
	try:
		location = int(location) - 1
	except:
		return 0
		
	if location >= listLen or location < 0:
		return 0
		
	return location - index

def ExportFavourites():
	selectedDir = Addon.getSetting("imExFolder")
	if selectedDir is None or selectedDir == "":
		return
	filename = common.GetKeyboardText(localizedString(30026).encode('utf-8'), "favorites").strip()
	if filename == "":
		return
	fullPath = os.path.join(selectedDir.decode("utf-8"), '{0}.txt'.format(filename))
	favsList = common.ReadList(FAV)
	common.WriteList(fullPath, favsList)
	xbmc.executebuiltin('Notification({0}, Favourites list is saved at {1}, {2}, {3})'.format(AddonName, fullPath, 10000, __icon__))

def ImportFavourites():
	selectedDir = Addon.getSetting("imExFolder")
	if selectedDir is None or selectedDir == "":
		return
	files = [f for f in os.listdir(selectedDir) if f.endswith(".txt")]
	fileInd = common.GetMenuSelected(localizedString(30025).encode('utf-8'), files)
	if fileInd == -1:
		return
	fullPath = os.path.join(selectedDir.decode("utf-8"), files[fileInd])
	favsList = common.ReadList(fullPath)
	if not common.YesNoDialog(localizedString(30215).encode('utf-8'), localizedString(30216).encode('utf-8'), line2=localizedString(30217).encode('utf-8').format(len(favsList)), line3=localizedString(30218).encode('utf-8'), nolabel=localizedString(30002).encode('utf-8'), yeslabel=localizedString(30001).encode('utf-8')):
		return
	common.WriteList(FAV, favsList)
	common.MakeFavouritesGuide(fullGuideFile)
	xbmc.executebuiltin('Notification({0}, Favourites list is saved., {2}, {3})'.format(AddonName, fullPath, 5000, __icon__))
	if common.getUseIPTV() and int(Addon.getSetting("iptvList")) == 0:
		MakeIPTVlists()
		DownloadLogos()

def Settings():
	addDir(localizedString(30240).encode('utf-8'), 51, 'https://www.ostraining.com/cdn/images/coding/setting.png', localizedString(30240).encode('utf-8'), isFolder=False)
	addDir(localizedString(30241).encode('utf-8'), 52, 'https://www.ostraining.com/cdn/images/coding/setting.png', localizedString(30241).encode('utf-8'), isFolder=False)
	addDir(localizedString(30242).encode('utf-8'), 53, 'https://www.ostraining.com/cdn/images/coding/setting.png', localizedString(30242).encode('utf-8'), isFolder=False)
	addDir(localizedString(30243).encode('utf-8'), 54, 'https://www.ostraining.com/cdn/images/coding/setting.png', localizedString(30243).encode('utf-8'), isFolder=False)
	SetViewMode()

def UpdateChannelsAndGuides():
	UpdateChannelsLists()
	SaveGuide()
	if Addon.getSetting("useIPTV") == "true":
		MakeIPTVlists()
		DownloadLogos()
		
def RefreshUserdataFolder():
	xbmc.executebuiltin("XBMC.Notification({0}, Cleaning addon profile folder..., {1}, {2})".format(AddonName, 300000 ,icon))
	settingsFile = os.path.join(user_dataDir, 'settings.xml')
	for the_file in os.listdir(user_dataDir):
		file_path = os.path.join(user_dataDir, the_file)
		try:
			if os.path.isfile(file_path) and file_path != FAV and file_path != settingsFile:
				os.unlink(file_path)
		except Exception as ex:
			xbmc.log("{0}".format(ex), 3)
	listsDir =  os.path.join(user_dataDir, 'lists')
	for the_file in os.listdir(listsDir):
		file_path = os.path.join(listsDir, the_file)
		try:
			if os.path.isfile(file_path) and file_path != selectedCategoriesFile:
				os.unlink(file_path)
		except Exception as ex:
			xbmc.log("{0}".format(ex), 3)
	xbmc.executebuiltin("XBMC.Notification({0}, Addon profile folder cleaned., {1}, {2})".format(AddonName, 5000 ,icon))
	CleanLogosFolder()
	remoteSettings = common.GetRemoteSettings()
	if not os.path.isfile(remoteSettingsFile):
		common.UpdateFile(remoteSettingsFile, "remoteSettingsZip", remoteSettings, zip=True, forceUpdate=True)
		remoteSettings = common.ReadList(remoteSettingsFile)
	if remoteSettings == []:
		xbmc.executebuiltin('Notification({0}, Cannot load settings, {1}, {2})'.format(AddonName, 5000, icon))
		return
	UpdateChannelsAndGuides()
	
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

params = get_params()

try:		
	mode = int(params["mode"])
except:
	mode = None
try:
	iconimage = urllib.unquote_plus(params["iconimage"])
except:
	iconimage = None
try:		
	channelID = str(params["channelid"])
except:
	channelID  = None
try:
	categoryID = str(params["categoryid"])
except:
	categoryID  = None


#xbmc.log("----> {0}".format(sys.argv), 2) 
#xbmc.log("----> Mode: {0}".format(mode), 2) 
#xbmc.log("----> IconImage: {0}".format(iconimage), 2)
#xbmc.log("----> categoryID: {0}".format(categoryID), 2)
#xbmc.log("----> channelID: {0}".format(channelID), 5)

updateList = True

if mode is None:
	if channelID is None:
		CATEGORIES()
	else:
		item = common.GetChannelByID(channelID)
		type = item.get('type', '')
		if type == 'video' or type == 'audio':
			PlayChannelByID(channel=item)
		elif type == 'playlist':
			ListLive(catChannels=item["list"])
elif mode == 1 or mode == 10:
	updateList = PlayChannelByID(chID=channelID)
elif mode == 2:
	ListLive(categoryID=channelID, iconimage=iconimage)
elif mode == 3:
	ListLive(categoryID=categoryID, iconimage=iconimage, chID=channelID)
elif mode == 5:
	ChannelGuide(channelID, categoryID)
elif mode == 11:
	updateList = PlayChannelByID(chID=channelID, fromFav=True)
elif mode == 16:
	listFavorites()
elif mode == 17: 
	channels = common.GetChannels(categoryID)
	channel = [x for x in channels if x["id"] == channelID]
	if len(channel) < 1:
		xbmc.executebuiltin('Notification({0},  Cannot add this channel to favourites, {2}, {3})'.format(AddonName, Addon.getSetting("chColor"), 5000, __icon2__))
	else:
		addFavorites(channel) 
elif mode == 18:
	removeFavorties([int(channelID)])
	xbmc.executebuiltin("XBMC.Container.Refresh()")
elif mode == 20: # Download Guide now - from server
	SaveGuide()
	updateList = False
elif mode == 22: # Update Channels Lists now
	UpdateChannelsLists()
	updateList = False
elif mode == 23: # Clean addon profile folder and refresh lists
	RefreshUserdataFolder()
	updateList = False
elif mode == 30: # Make IPTV channels list and TV-guide
	MakeIPTVlists()
	updateList = False
elif mode == 31: # Download channels logos
	DownloadLogos()
	updateList = False
elif mode == 32: # Update IPTVSimple settings
	UpdateIPTVSimple()
	updateList = False
elif mode == 33: # Empty channels logos folder
	CleanLogosFolder()
	updateList = False
elif mode == 34: # Refresh ALL Live TV required resources
	RefreshLiveTV()
	updateList = False
elif mode == 35: # Add categories to display in addon
	AddCategories()
	updateList = False
elif mode == 36: # Remove categories from display in addon
	RemoveCategories()
	updateList = False
elif mode == 37: # Add selected channels from category to favourites
	AddFavoritesFromCategory(categoryID)
	updateList = False
elif mode == 38: # Add the whole group channels from category to favourites
	AddCategoryToFavorites(categoryID)
	updateList = False
elif mode == 39: # Remove selected channels from favorites
	RemoveSelectedFavorties()
	updateList = False
elif mode == 40: # Remove all channels from favorites
	EmptyFavorties()
	updateList = False
elif mode == 41: # Move channels location in favourites
	MoveInList(int(channelID), int(iconimage), FAV)
elif mode == 42: # Move categoties location
	MoveInList(int(channelID), int(iconimage), selectedCategoriesFile)
elif mode == 43: # Export IsraeLIVE favourites
	ExportFavourites()
	updateList = False
elif mode == 44: # Import IsraeLIVE favourites
	ImportFavourites()
	updateList = False
elif mode == 45: # Add an external channel to IsraeLIVE favourites
	AddUserChannelToFavorites()
	updateList = False
elif mode == 50:
	Settings()
elif mode == 51:
	Addon.openSettings()
elif mode == 52:
	xbmc.executebuiltin('Addon.OpenSettings("script.module.israeliveresolver")')
elif mode == 53:
	UpdateChannelsAndGuides()
elif mode == 54: # Clean addon profile folder and refresh lists
	RefreshUserdataFolder()
elif mode == 100: # CheckUpdates
	checkUpdates.Update()
	updateList = False
elif mode == 101: # Update IPTV lists
	updateM3U.Update()
	updateList = False
else:
	updateList = False

if updateList:
	xbmcplugin.endOfDirectory(int(sys.argv[1]))
