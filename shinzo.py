# coding=utf-8
import requests, json, time, random, datetime, threading, pickle

sitekey = "6LczOjoUAAAAABEfbqdtD11pFD5cZ0n5nhz89nxI"


def log(event):
	d = datetime.datetime.now().strftime("%H:%M:%S")
	print("Raffle by Azerpas :: " + str(d) + " :: " + event)
		
class Raffle(object):
	def __init__(self):
		self.s = requests.session()
		# "https://colette.sneakers-raffle.fr/","https://starcow.sneakers-raffle.fr/"
		self.shoes = [
		#{"url":"product/nike-air-jordan-1/","shoe_id":"2","shoe_name":"Nike Air Jordan 1","imgURL":"AirJordan.jpg"},
		#{"url":"product/nike-blazer/","shoe_id":"3","shoe_name":"Nike Blazer","imgURL":"Blazer.jpg"},
		{"url":"https://raffle.shinzo.paris/","shoe_id":"14","shoe_name":"The Ten: Air Jordan 1","imgURL":"AirJordan@100cropped.jpg"}]
		self.sites = [
			#{"url":"https://shinzo.sneakers-raffle.fr/","siteid":"2","nomtemplate":"nike-raffle-confirm-shinzo"},
			#{"url":"https://thebrokenarm.sneakers-raffle.fr/","siteid":"3","nomtemplate":"nike-raffle-confirm-the-broken-arm"},
			#{"url":"https://colette.sneakers-raffle.fr/","siteid":"4","nomtemplate":"nike-raffle-confirm-colette"},
			{"url":"https://raffle.shinzo.paris/","siteid":"8","nomtemplate":"nike-raffle-confirm-off-white-popup"}
			]
		# interval etc
		self.api = "https://raffle.shinzo.paris/wp-json/contact-form-7/v1/contact-forms/445/feedback"

	def register(self,identity):
		# For each site...
		for sts in self.sites:
			# register to each shoes.
			for dshoes in self.shoes:

				# getting captcha from threading harvester
				d = datetime.datetime.now().strftime('%H:%M')
				log("Getting Captcha")
				flag = False
				while flag != True:
					d = datetime.datetime.now().strftime('%H:%M')
					try:
						file = open(str(d)+'.txt','r') #r as reading only
						flag = True
					except IOError:
						time.sleep(2)
						log("No captcha available(1)")
						flag = False
				try:
					FileList = pickle.load(file) #FileList the list where i want to pick out the captcharep
				except:
					log("Can't open file")
				while len(FileList) == 0: #if len(FileList) it will wait for captcha scraper 
						d = datetime.datetime.now().strftime('%H:%M')
						try:
							file = open(str(d)+'.txt','r')
							FileList = pickle.load(file)
							if FileList == []:
								log("No captcha available(2)")
								time.sleep(3)
						except IOError as e:
							log("No file, waiting...")
							print(e)
							time.sleep(3)
				captchaREP = random.choice(FileList) 
				FileList.remove(captchaREP)
				file  = open(str(d)+'.txt','w')
				pickle.dump(FileList,file)
				log("Captcha retrieved")

				headers = {
	"Accept":"application/json, text/javascript, */*; q=0.01",
"Accept-Encoding":"gzip, deflate, br",
"Accept-Language":"fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
"Connection":"keep-alive",
"Host":"raffle.shinzo.paris",
"Origin":"https://raffle.shinzo.paris",
"Referer":"https://raffle.shinzo.paris/nike-air-max-1-97-vf-sw/",
"Upgrade-Insecure-Requests":"1",
"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
"X-Requested-With": "XMLHttpRequest",
				}
				payload = {
	"_wpcf7":"445",
	"_wpcf7_version":"4.9.2",
	"_wpcf7_locale":"fr-FR",
	"_wpcf7_unit_tag":"wpcf7-f445-p426-o1",
	"_wpcf7_container_post":"426",
	"_wpcf7cf_hidden_group_fields":"[]",
	"_wpcf7cf_hidden_groups":"[]",
	"_wpcf7cf_visible_groups":"[]",
	"_wpcf7cf_options":"""{"form_id":445,"conditions":[],"settings":false}""",
	"lang":"fr",
	"your-firstname":identity['fname'],
	"your-name":identity['lname'],
	"your-email":identity['mail'],
	"your-tel":identity['phone'],
	"size":"8.5US - 42",
	"accept":"1",
	"g-recaptcha-response":captchaREP,
	"raffle66websiteshinzo67142423":"",
	"bb2_screener_":"1521557187 178.208.16.140 178.208.16.140"
				}

				req = self.s.post(self.api,headers=headers,data=payload)
				print(req)
				print(req.text)
				#{"into":"#wpcf7-f445-p426-o1","status":"validation_failed","message":"Un ou plusieurs champs contiennent une erreur. Veuillez v\u00e9rifier et essayer \u00e0 nouveau.","invalidFields":[{"into":"span.wpcf7-form-control-wrap.your-email","message":"L'adresse e-mail n'est pas valide.","idref":null}]}
				jsonn = json.loads(req.text)
				if(jsonn['status'] == "validation_failed" or jsonn['status'] == "mail_failed"):
					print("ERROR, CHECK BELOW")
					print(json['status'])
					raise Exception('Infos are incorrect or already registered')
				

if __name__ == "__main__":
	ra = Raffle()
	accounts = [
		# 11 5US , 18 9US , 14 7US
		{"fname":"pet","lname":"james","mail":"petjames@gmail.com","phone":"+33612334455","birthdate":"01/01/1998","shoesize":"42",},
		]
	# catpcha
	proxies = []
	errors = []
	index = 0
	regis = 0
	for i in accounts:
		p = random.choice(proxies)
		proxies.remove(p)
		print("\n\n-------------------------")
		print('NEW TASK')
		print("-------------------------\n")
		print(i['mail'])
		if '@' in p:
			proxy = { 'https' : 'https://{}'.format(p) }
			log('Using proxy:')
			print(colored(proxy,'red', attrs=['bold']))
		else:
			proxy = {'http':p,
					'https':p}
			log('Using proxy:')
			print(colored(proxy['https'],'red', attrs=['bold']))
		try:
			ra.register(i,proxy)
			regis += 1
		except:
			print("Error while registering")
			errors.append(i)
		index += 1
	print(errors)
