import re, requests, bs4
from bs4 import BeautifulSoup as parser
ses=requests.Session()

user = input("masukan email : ")
pw = input("masukan sandi : ")
ua = input("masukan user-agent : ")

url = ses.get(f"https://mbasic.facebook.com/login/device-based/password/?uid={user}&flow=login_no_pin")
headers = {
	"Host": "mbasic.facebook.com",
	"cache-control": "max-age=0",
	"upgrade-insecure-requests": "1",
	"origin": "https://mbasic.facebook.com",
	"content-type": "application/x-www-form-urlencoded",
	"user-agent": ua,
	"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
	"x-requested-with": "mark.via.gp",
	"sec-fetch-site": "same-origin",
	"sec-fetch-mode": "cors",
	"sec-fetch-user": "empty",
	"sec-fetch-dest": "document",
	"referer": "https://mbasic.facebook.com/index.php?next=https://developers.facebook.com/tools/debug/accesstoken/",
	"accept-encoding": "gzip, deflate br",
	"accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7"}
data = {
	"lsd":re.search('name="lsd" value="(.*?)"', str(url.text)).group(1),
	"jazoest": re.search('name="jazoest" value="(.*?)"', str(url.text)).group(1),
	"uid":user,
	"flow":"login_no_pin",
	"pass": pw,
	"next": "https://mbasic.facebook.com/login/save-device/"}
post = ses.post("https://mbasic.facebook.com/login/device-based/validate-password/?shbl=0", data=data, headers=headers)
if "c_user" in ses.cookies.get_dict():
	coki = ";".join(i["name"]+"="+i["value"] for i in ses.cookies.get_dict())
	print(f"{user}|{pw}|{coki}")
elif "checkpoint" in ses.cookies.get_dict():
	parsing1 = parser(post.text,"html.parser")
	action1 = parsing1.find("form",{"method":"post"})["action"]
	data2 = {
		"fb_dtsg":re.search('name="fb_dtsg" value="(.*?)"', str(post.text)).group(1),
		"jazoest":re.search('name="jazoest" value="(.*?)"', str(post.text)).group(1),
		"checkpoint_data": "",
		"nh":re.search('name="nh" value="(.*?)"', str(post.text)).group(1)}
	past = ses.post("https://mbasic.facebook.com"+action1,data=data2)
	parsing2 = parser(past.text,"html.parser")
	action2 = parsing2.find("form",{"method":"post"})["action"]
	data3 = {
		"fb_dtsg":re.search('name="fb_dtsg" value="(.*?)"', str(past.text)).group(1),
		"jazoest":re.search('name="jazoest" value="(.*?)"', str(past.text)).group(1),
		"checkpoint_data": "",
		"submit[Continue]": "Lanjutkan",
		"nh":re.search('name="nh" value="(.*?)"', str(past.text)).group(1)}
	pust = ses.post("https://mbasic.facebook.com"+action2,data=data3)
	parsing3 = parser(pust.text,"html.parser")
	option = parsing3.find_all("option")
	if len(option) == 0:
		print("tidak ada opsi terdeteksi")
	else:
		for opsi in option:
			print(opsi.text)
	
	
	
	