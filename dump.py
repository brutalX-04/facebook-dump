# --> Author  : brutalX-04
# --> Created : 7-Desember-2023


# --> Module
import os
import re
import sys
import time
import json
import requests


# --> Color
p  = '\33[m' 		# DEFAULT
m  = '\x1b[0;91m' 	# RED 
k  = '\033[0;93m' 	# KUNING 
h  = '\x1b[0;92m' 	# HIJAU 
u  = "\033[0;35m"   # UNGU
a  = "\033[1;30m"   # ABU


# -- > Banner
def banner():
	os.system('clear')
	print(f'{u}    .___                    \n  __| _/_ __  _____ ______  \n / __ |  |  \/     \\____ \ \n/ /_/ |  |  /  Y Y  \  |_> >\n\____ |____/|__|_|  /   __/ \n     \/           \/|__|    {p}')
	print('─' * 30)


# --> Menu
def menu():
	banner()
	acc = infoAcc()
	infoIp = infoIP()

	print('Name     : %s%s%s'%(h,acc[0],p))
	print('Ids      : %s%s%s'%(h,acc[1],p))
	print('Ip       : %s%s%s'%(a,infoIp[0],p))
	print('Country  : %s%s%s'%(a,infoIp[1],p))
	print('Provider : %s%s%s'%(a,infoIp[2],p))
	print('─' * 30)
	print('1. Dump Id')
	print('0. Log Out\n')
	pilih = input('Input :')

	if pilih in ['01','1']:
		dump()

	elif pilih in ['0','00']:
		os.system('rm DATA/account/.token.txt')
		os.system('rm DATA/account/.cookie.txt')


# --> Info Provider
def infoIP():
	try:
		get = requests.get('https://ipapi.co/json/').json()
		ip = get['ip']
		country = get['country_name']
		provider = get['org']
		return ip,country,provider

	except Exception as e:
		raise e


# --> Info Account
def infoAcc():
	try:
		cookie = open('DATA/account/.cookie.txt','r').read()
		token = open('DATA/account/.token.txt','r').read()
		get = requests.get('https://graph.facebook.com/v18.0/me?fields=id,name&access_token='+token, cookies={'cookie': cookie}).json()
		name = get['name']
		ids = get['id']
		return name, ids
	except Exception as e:
		print(f'{m}Failled Get Info Account{p}, Wait To Login ...');time.sleep(2)
		login()


# --> Login
def login():
	try:
		banner()
		cookie = input('Input Cookie : ')
		with requests.Session() as rsn:
			rsn.headers.update({
				'Accept-Language': 'id,en;q=0.9',
				'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
				'Referer': 'https://www.instagram.com/',
				'Host': 'www.facebook.com',
				'Sec-Fetch-Mode': 'cors',
				'Accept': '*/*',
				'Connection': 'keep-alive',
				'Sec-Fetch-Site': 'cross-site',
				'Sec-Fetch-Dest': 'empty',
				'Origin': 'https://www.instagram.com',
				'Accept-Encoding': 'gzip, deflate'
			})
			response = rsn.get('https://www.facebook.com/x/oauth/status?client_id=124024574287414&wants_cookie_data=true&origin=1&input_token=&sdk=joey&redirect_uri=https://www.instagram.com/brutalid_/', cookies={'cookie': cookie})
			if '"access_token":' in str(response.headers):
				token = re.search('"access_token":"(.*?)"', str(response.headers)).group(1)
				open('DATA/account/.token.txt', 'w').write(token)
				open('DATA/account/.cookie.txt', 'w').write(cookie)
				print('%sLogin Succes%s'%(h, p))
				exit()

			else:
				print('%sFailled Get Token%s'%(m, p))
				exit()

	except Exception as e:
		exit()


# --> Dump Id
def dump():
	try:
		banner()
		target = [];idd = 1
		print('Note :\n * Input Id Friendlist Publick')
		print(f' * Use [{h} , {p}] For Dump Multiple Ids\n')
		ids = input('Input Ids : ')
		if ',' in ids:
			[target.append(x) for x in ids.split(',')]
			name = ids.split(',')[0]
		else:
			target.append(ids)
			name = ids

		cookie = open('DATA/account/.cookie.txt','r').read()
		token = open('DATA/account/.token.txt','r').read()
		for x in target:
			get = requests.get('https://graph.facebook.com/%s?fields=friends&access_token=%s'%(x, token), cookies={'cookie': cookie}).json()
			for x in get['friends']['data']:
				try:
					user_id, user_name = x['id'], x['name']
					open('DATA/dump/%s.txt'%(name),'a').write(user_id+'|'+user_name+'\n')
					print('\rSucces Dump %s%s%s User '%(h, idd, p),end='')
					idd+=1
				except:
					pass

		print('\n\nFile Save In %sDATA/dump/%s.txt%s'%(h,name,p))

	except Exception as e:
		print('%sFailled Dump%s'%(m, p))
		print(e)


# --> Running Script
if __name__ == '__main__':
	try:
		os.listdir('DATA')
	except:
		os.system('mkdir DATA')
		os.system('mkdir DATA/account')
		os.system('mkdir DATA/dump')

	menu()