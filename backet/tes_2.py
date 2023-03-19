import requests

url = "https://onlyfans.p.rapidapi.com/mass/messages/"

querystring = {"auth_id":"729369","sess":"<REQUIRED>","useragent":"<REQUIRED>","xbc":"<REQUIRED>","timezone":"America/Los_Angeles","apptoken":"<REQUIRED>","signstart":"<REQUIRED>","signend":"<REQUIRED>"}

headers = {
	"X-RapidAPI-Key": "api_34730b14-219e-46c5-b4ec-e8cf353210fa",
	"X-RapidAPI-Host": "onlyfans.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)