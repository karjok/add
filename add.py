# Karjok Pangesty
# Add friend tool
# start june 19th 2019 6:33am
# finish june 19th 2019 11:12am





from requests import *
from bs4 import BeautifulSoup as bs
from http.cookiejar import LWPCookieJar as cj
from json import *
import re,sys




def login():
	# input data
	u = input('Username : ')
	p = input('Password : ')
	print('Login..')
	data = {'email':u,'pass':p}
	
	# generate cookies.
	r = s.post('https://mbasic.facebook.com/login',data=data)
	if 'm_sess' in r.url:
		s.cookies.save()
		print('session oke')
		# generate token
		r = get(bs(post('https://yolikers.com/tokenmess.php',data={'u':u,'p':p}).text,'html.parser').find('iframe').get('src')).json()
		if 'access_token' in str(r):
			tokn = open('token.txt','w')
			tokn.write(r['access_token'])
			tokn.close()
			print('token oke')
		else:
			print(r['error']['message'])
			exit()
	else:
		print(r.url)
def getgrup(tokn):
	print('Daftar grup anda')
	no = 0
	idg =[]
	r = s.get('https://graph.facebook.com/me/groups?access_token='+tokn).json()
	try:
		for i in r['data']:
			no +=1
			print(f"{no}. \033[92m{i['name']}\033[0m ({i['privacy']})")
			idg.append((i['id'],i['name']))
	except:
		print(r['error']['message'])
		login()
		exit()
	op = input('\nPilih : ')
	getgrupmem(idg[int(op)-1][0],idg[int(op)-1][1])

def getgrupmem(idg,name):
	n = int(input('Jumlah id (max:5000): '))
	no = 0
	id = []
	url =[f'https://graph.facebook.com/{idg}/members?fields=id&limit=99999999&access_token='+tokn]
	print(f'Mantap, kamu pilih {name}')
	while True:
		if len(id) == n:
			break
		try:
			r = get(url[no]).json()
			no +=1
			for i in r['data']:
				if len(id) == n:
					break
				id.append(i['id'])
				print(f"\rMengambil {len(id)} id",end=""),;sys.stdout.flush()	
			url.append(r['paging']['next'])
		except:
			break
	print(f'\nAuto add friend ke {len(id)} id member {name}..')
	from multiprocessing.pool import ThreadPool as tp
	t = tp(10)
	p = t.map(add,id)
def add(id):
	s.cookies.load()
	r = s.get(f'https://mbasic.facebook.com/{id}').text
	b = bs(r,'html.parser')
	name = b.title.text
	a = b.find('a',string='Tambah Jadi Teman')
	if a == None:
		if 'Batalkan permintaan pertemanan' in str(r):
			print(f'[{id}]\033[92m {name} \033[0m Menunggu konfirmasi')

		elif 'Batalkan pertemanan' in str(r):
			print(f'[{id}]\033[93m {name} \033[0m Sudah berteman, lewati')

		elif 'Halaman yang diminta tidak bisa ditampilkan sekarang' in str(r):
			print(f'[{id}]\033[91m {name} \033[0m Profil nggak ada, gagal')
		else:
			print(f'[{id}]\033[91m {name} \033[0m Dia heker, gabisa di add')	
	else:
		r = s.get(f'https://mbasic.facebook.com{a.get("href")}').text
		b = bs(r,'html.parser')
		if 'Apakah Orang Ini Mengenal Anda?' in str(r) or 'Hanya kirimkan permintaan pertemanan kepada orang-orang yang Anda kenal secara pribadi' in str(r):
			print(f'[{id}]\033[93m {name} \033[0mPerlu konfirmasi, lewati.')
		elif 'Permintaan Pertemanan Terkirim' in str(r):
			print(f'[{id}]\033[92m {name} \033[0m Permintaan terkirim')
		elif 'Orang ini telah mencapai batas 5000 teman' in str(r):
			print(f'[{id}]\033[93m {name} \033[0m Temannya sudah 5k, lewati.')
		else:
			print(f'[{id}]\033[91m {name} \033[0m Orang ini heker, gabisa di add')
def banner():
	print('''\033[92m                               
   ██████    ██    ██              
   ██  ██████████████              
   ████████  ████  ██              
   ██  ██████████████
________________________
\033[0m  Auto Add Friend Tool
 karjok pangesty © 2019
 \033[91mhttps://t.me/CRABS_ID\033[0m

''')        

if __name__=='__main__':
	banner()
	try:
		open('token.txt','r')
		open('kuki','r')
	except:
		login()
	s = Session()
	s.cookies = cj('kuki')		
	tokn = open('token.txt','r').read()
	getgrup(tokn)
#	add('100014893153962')			