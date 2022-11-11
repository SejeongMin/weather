import requests
import re
import json
import time
from bs4 import BeautifulSoup
import datetime

KAKAO_TOKEN = "K9RB5iOM9_Fh4RuUryKyDMF7NoWqaBq_eoHhyqVWCilwFAAAAYRmblMx"

def sendToMeMessage(text):
	header = {"Authorization":'Bearer ' + KAKAO_TOKEN}
	url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
	post = {
		"object_type": "text",
		"text": text,
		"link": {
			"web_url": "https://developers.kakao.com",
			"mobile_web_url": "https://developers.kakao.com"
		},
		"button_title": "바로 확인"
	}
	data = { "template_object": json.dumps(post)}
	return requests.post(url, headers=header, data=data)

def getWeather():
	url = "http://www.kma.go.kr/wid/queryDFSRSS.jsp?zone=4139054000"
	response = requests.get(url)

	time = re.findall(r'<hour>(.+?)</hour>', response.text)
	temp = re.findall(r'<temp>(.+)</temp>', response.text)
	humi = re.findall(r'<reh>(.+?)</reh>', response.text)
	wfKor = re.findall(r'<wfKor>(.+?)</wfKor>', response.text)
	text=  ""
	for i in range(8):
		text = text + "(" + str(time[i]) + "시 "
		text = text + str(temp[i]) + "C "
		text = text + str(humi[i]) + "% "
		text = text + str(wfKor[i]) + ")"
	
	return text

try:
	while True:
		now = datetime.datetime.now()
		hms = now.strftime('%H:%M:%S')
		print(hms)
		if re.search(':00:00$', hms):
			text = getWeather()
			print(sendToMeMessage(text).text)
		
		time.sleep(1.0)

except KeyboardInterrupt:
	pass
