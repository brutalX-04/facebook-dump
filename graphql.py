# Author  : brutalX | Rizky Nurahman
# Created : 31 Desember 2023

# --> Module
import os
import re
import json
import requests


# --> Callback
cok    = ''
target = ''


# --> Default Headers
defaultHeaders = {
	'authority': 'www.facebook.com',
	'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
	'accept-language': 'en-US,en;q=0.9,id;q=0.8',
	'cache-control': 'no-cache',
	'dpr': '1',
	'pragma': 'no-cache',
	'sec-ch-prefers-color-scheme': 'dark',
	'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
	'sec-ch-ua-full-version-list': '"Google Chrome";v="119.0.6045.199", "Chromium";v="119.0.6045.199", "Not?A_Brand";v="24.0.0.0"',
	'sec-ch-ua-mobile': '?0',
	'sec-ch-ua-model': '""',
	'sec-ch-ua-platform': '"Linux"',
	'sec-ch-ua-platform-version': '"6.5.0"',
	'sec-fetch-dest': 'document',
	'sec-fetch-mode': 'navigate',
	'sec-fetch-site': 'same-origin',
	'sec-fetch-user': '?1',
	'upgrade-insecure-requests': '1',
	'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
}


# --> Get data for requests
def getData(res):
    av  = re.search('"ACCOUNT_ID":"(.*?)"', res).group(1)
    hs  = re.search('"haste_session":"(.*?)"', res).group(1)
    ccg = re.search('"connectionClass":"(.*?)"', res).group(1)
    rev = re.search('"client_revision"\:(.*?)\,', res).group(1)
    hsi = re.search('"hsi":"(.*?)"', res).group(1)
    dts = re.search('"DTSGInitialData"\,\[\]\,{"token":"(.*?)"', res).group(1)
    jst = re.search('jazoest=(.*?)"', res).group(1)
    lsd = re.search('"LSD"\,\[\]\,{"token":"(.*?)"', res).group(1)
    spr = re.search('"__spin_r"\:(.*?)\,', res).group(1)
    spt = re.search('"__spin_t"\:(.*?)\,', res).group(1)
    data = { 'av': av,'__user': av,'__a': '1','__hs': hs,'dpr': '1','__ccg': ccg,'__rev': rev,'__hsi': hsi,'__comet_req': '15','fb_dtsg': dts,'jazoest': jst,'lsd': lsd,'__aaid': '0','__spin_r': spr,'__spin_b': 'trunk','__spin_t': spt,'fb_api_caller_class': 'RelayModern' }

    return data


# --> All dump with graphql
class dumpGraphql:

	# --> Dump friends
	def Friends(cookie, target):
		try:
			params = {
			    'locale': 'id_ID',
			}

			get           = requests.get('https://www.facebook.com/%s/friends'%(target), params=params, cookies={'cookie': cookie}, headers=defaultHeaders).text
			data          = re.search('"pageItems":(.*?)},"__module_operation_ProfileCometPaginatedAppCollection_timelineAppCollection"', get).group(1)
			node          = json.loads(data)
			count_friends = re.search('"items":{"count":(.*?)}', get).group(1)
			end_cursor    = node['page_info']['end_cursor']
			id_cursor     = re.search('"nav_collections":{"nodes":\[{"id":"(.*?)"', get).group(1)

			print(count_friends)
			for x in node['edges']:
				name = x['node']['title']['text']
				ids  = x['node']['node']['id']
				print(ids,name)
			
			dumpGraphql.nextFriends(cookie, target , end_cursor, id_cursor, get)

		except Exception as e:
			raise e

	# --> Next dump friends with graphql
	def nextFriends(cookie, target , end_cursor, id_cursor, res):
		try:
			headers = defaultHeaders
			data    = getData(res)

			headers.update({
			    'accept': '*/*',
			    'origin': 'https://www.facebook.com',
			    'referer': 'https://www.facebook.com/%s/friends&locale=id_ID'%(target),
			    'sec-fetch-dest': 'empty',
			    'sec-fetch-mode': 'cors',
			    'sec-fetch-site': 'same-origin',
			    'x-asbd-id': '129477',
			    'x-fb-friendly-name': 'ProfileCometAppCollectionListRendererPaginationQuery',
			    'x-fb-lsd': re.search('"LSD"\,\[\]\,{"token":"(.*?)"', res).group(1)
			})

			data.update({
				'fb_api_req_friendly_name': 'ProfileCometAppCollectionListRendererPaginationQuery',
				'variables': '{"count":8,"cursor":"%s","scale":1,"search":null,"id":"%s"}'%(end_cursor, id_cursor),
				'server_timestamps': 'true',
				'doc_id': '6709724792472394'
			})

			post = requests.post('https://www.facebook.com/api/graphql/', cookies={'cookie': cookie}, headers=headers, data=data).json()
			
			for x in post['data']['node']['pageItems']['edges']:
				name = x['node']['title']['text']
				ids  = x['node']['node']['id']
				print(ids,name)

			try:
				end_cursor = post['data']['node']['pageItems']['page_info']['end_cursor']
				dumpGraphql.nextFriends(cookie, target , end_cursor, id_cursor, res)

			except Exception as e:
				print('Succes dump all friends')

		except Exception as e:
			raise e


	# --> Dump followers
	def Followers(cookie, target):
		try:
			params = {
				'locale': 'id_ID',
			}

			get             = requests.get('https://www.facebook.com/%s/followers'%(target), params=params, cookies={'cookie': cookie}, headers=defaultHeaders).text
			data            = re.search('"pageItems":(.*?)},"__module_operation_ProfileCometPaginatedAppCollection_timelineAppCollection"', get).group(1)
			node            = json.loads(data)
			count_followers = re.search('"items":{"count":(.*?)}', get).group(1)
			end_cursor      = node['page_info']['end_cursor']
			id_cursor       = re.search('"tab_key":"followers","id":"(.*?)"', get).group(1)

			print(count_followers)
			for x in node['edges']:
				name = x['node']['title']['text']
				ids  = x['node']['node']['id']
				print(ids,name)
			
			dumpGraphql.nextFollowers(cookie, target , end_cursor, id_cursor, get)

		except Exception as e:
			raise e

	# --> Next dump followers with graphql
	def nextFollowers(cookie, target , end_cursor, id_cursor, res):
		try:
			headers = defaultHeaders
			data    = getData(res)

			headers.update({
			    'accept': '*/*',
			    'origin': 'https://www.facebook.com',
			    'referer': 'https://www.facebook.com/%s/followers?locale=id_ID'%(target),
			    'sec-fetch-dest': 'empty',
			    'sec-fetch-mode': 'cors',
			    'sec-fetch-site': 'same-origin',
			    'x-asbd-id': '129477',
			    'x-fb-friendly-name': 'ProfileCometAppCollectionListRendererPaginationQuery',
			    'x-fb-lsd': re.search('"LSD"\,\[\]\,{"token":"(.*?)"', res).group(1)
			})

			data.update({
				'fb_api_req_friendly_name': 'ProfileCometAppCollectionListRendererPaginationQuery',
				'variables': '{"count":8,"cursor":"%s","scale":1,"search":null,"id":"%s"}'%(end_cursor, id_cursor),
				'server_timestamps': 'true',
				'doc_id': '6709724792472394'
			})

			post = requests.post('https://www.facebook.com/api/graphql/', cookies={'cookie': cookie}, headers=headers, data=data).json()
			
			for x in post['data']['node']['pageItems']['edges']:
				name = x['node']['title']['text']
				ids  = x['node']['node']['id']
				print(ids,name)

			try:
				end_cursor = post['data']['node']['pageItems']['page_info']['end_cursor']
				dumpGraphql.nextFollowers(cookie, target , end_cursor, id_cursor, res)

			except Exception as e:
				print('Succes dump all followers')

		except Exception as e:
			raise e


	# --> Dump Member groups
	def Member(cookie, target):
		try:
			params = {
				'locale': 'id_ID',
			}

			get           = requests.get('https://www.facebook.com/groups/%s/members'%(target), params=params, cookies={'cookie': cookie}, headers=defaultHeaders).text
			data          = re.search('"new_members":(.*?),"group_purposes"', get).group(1)
			node          = json.loads(data)
			end_cursor    = node['page_info']['end_cursor']

			for x in node['edges']:
				name = x['node']['name']
				ids  = x['node']['id']
				print(ids,name)
			
			dumpGraphql.nextMembers(cookie, target , end_cursor, get)

		except Exception as e:
			raise e

	# --> Next dump members with graphql
	def nextMembers(cookie, target , end_cursor, res):
		try:
			headers = defaultHeaders
			data    = getData(res)

			headers.update({
			    'accept': '*/*',
			    'origin': 'https://www.facebook.com',
			    'referer': 'https://www.facebook.com/groups/%s/members?locale=id_ID'%(target),
			    'sec-fetch-dest': 'empty',
			    'sec-fetch-mode': 'cors',
			    'sec-fetch-site': 'same-origin',
			    'x-asbd-id': '129477',
			    'x-fb-friendly-name': 'GroupsCometMembersPageNewMembersSectionRefetchQuery',
			    'x-fb-lsd': re.search('"LSD"\,\[\]\,{"token":"(.*?)"', res).group(1)
			})

			data.update({
				'fb_api_req_friendly_name': 'GroupsCometMembersPageNewMembersSectionRefetchQuery',
				'variables': '{"count":10,"cursor":"%s","groupID":"%s","recruitingGroupFilterNonCompliant":false,"scale":1,"id":"%s"}'%(end_cursor, target, target),
				'server_timestamps': 'true',
				'doc_id': '6621621524622624'
			})

			post = requests.post('https://www.facebook.com/api/graphql/', cookies={'cookie': cookie}, headers=headers, data=data).json()

			for x in post['data']['node']['new_members']['edges']:
				name = x['node']['name']
				ids  = x['node']['id']
				print(ids,name)

			try:
				end_cursor = post['data']['node']['new_members']['page_info']['end_cursor']
				dumpGraphql.nextMembers(cookie, target , end_cursor, res)

			except Exception as e:
				print('Succes dump all members')

		except Exception as e:
			raise e



# dumpGraphql.Friends(cok, target)
# dumpGraphql.Followers(cok, target)
# dumpGraphql.Member(cok, target)
