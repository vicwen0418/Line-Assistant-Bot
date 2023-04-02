from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
from abc import ABC, abstractmethod
import time

ua = UserAgent() 
user_agent = UserAgent()

list_city = ["台北市", "基隆市", "新北市", 
             "台中市", "桃園市", "台南市",
             "高雄市", "宜蘭縣", "新竹縣",
             "苗栗縣", "彰化縣", "南投縣",
             "雲林縣", "嘉義縣", "屏東縣",
             "台東縣", "澎湖縣", "新竹市","嘉義市"]

list_play_dic = ["景點", "好玩", "地方", "地點", "地", "娛樂"]

list_food_dic = ["餐廳", "好吃", "美食", "飲食", "吃飯"]

list_weather_dic = ["天氣", "下雨", "降雨機率"]


class function(ABC):

    @abstractmethod
    def crawler(self):
        pass


class IFoodie(function):

    def crawler(self, area):
        # IFoodie 愛食記網站
        url = "https://ifoodie.tw/explore/" + area + \
            "/list?sortby=popular&opening=true"
        
        response = requests.get(url = url, headers = {"user-agent" : user_agent.random})
                
        soup = BeautifulSoup(response.content, "html.parser")

        cards = soup.find_all('div', {'class': 'jsx-1156793088 restaurant-info'}, limit=10)

        content = ""
        for card in cards:
                    
            title = card.find(  # 餐廳名稱
            "a", {"class": "jsx-1156793088 title-text"}).getText()

            stars = card.find(  # 餐廳評價
            "div", {"class": "jsx-2373119553 text"}).getText()
        
            address = card.find(  # 餐廳地址
            "div", {"class": "jsx-1156793088 address-row"}).getText()
        
        
            #將取得的餐廳名稱、評價及地址連結一起，並且指派給content變數
            content += f"{title} - {stars}顆星 \n{address} \n\n"
                    
        return content




class okgo(function):

    def crawler(self, area):
        # okgo 玩全台灣
        url = "https://okgo.tw/Search.html?Page=1&kw=" + area + "&st=1"
        response = requests.get(url = url, headers = {"user-agent" : user_agent.random})
                
        soup = BeautifulSoup(response.content, "html.parser") 

        cards = soup.find_all('li', {'id': 'Search_Content_li'}, limit=5)

        content = ""
        for card in cards:
            web_address = card.find('a', {'class' : 'STopic'})

            url = "https://okgo.tw/" + web_address["href"]
            
            response = requests.get(url = url, headers = {"user-agent" : user_agent.random})

            soup = BeautifulSoup(response.content, "html.parser") 

            information = soup.find('div', {'class' : 'sec3 word Resize'})

            title = information.find('h2', {'style' : 'color:#40a0bf;'}).getText()

            zone_list = information.find('strong').find_all('a')
            zone = ""
            for zones in zone_list: zone += zones.text

            TransInfo = soup.find('div', {'id' : 'Buty_View_Traffic'}).getText()


            content += f"{title} - {zone}\n\n{TransInfo}\n\n"


        return content


class weather(function):      

    def crawler(self, area):

        city_web = {"台北市" : "https://weather.com/zh-TW/weather/hourbyhour/l/6b221b26e046a442e03dc46fbe91d5874c6461afde61187dd4126bddeea1e2aa",
                    "基隆市" : "https://weather.com/zh-TW/weather/hourbyhour/l/7a1bd787c9a5bfd8b7290f325ea531127a0447198d4c09689f6cf12f4421a110a042adb62e0ce6b4ee0110784300e689",
                    "台南市" : "https://weather.com/zh-TW/weather/hourbyhour/l/cb9a4442e9bf7da0ece89bd21a5161210e79cccc0ec2647b3565977e7a278c31"}

        url = city_web[area]

        user_agent = UserAgent()

        response = requests.get(url=url, headers={"user-agent": user_agent.random})

        soup = BeautifulSoup(response.content, "html.parser")

        cards = soup.find_all(
            "div", {"class": "DetailsSummary--DetailsSummary--1DqhO"}, limit=15)

        content = f"{area}每日天氣\n\n"
        for card in cards:

            times = card.find(
                "h3", {"class": "DetailsSummary--daypartName--kbngc"}).getText()

            if times == "00:00": break # breakpoint

            temprature = card.find("span", {"class": "DetailsSummary--tempValue--jEiXE"}).getText()

            status = card.find("span", {"class": "DetailsSummary--extendedData--307Ax"}).getText()

            rain_prob = card.find("span", {"data-testid": "PercentageValue"}).getText()

            content += f"時間:{times}\n氣溫:{temprature}\n天氣狀況:{status}\n降雨機率:{rain_prob}\n\n"
            

        return content
        

class check:
    def __init__(self) -> None:
        self.area = ""
        self.func = '0'

    def CheckFunc(self, sentence, list_dic, func_no):
        for i in list_dic:
            pos = sentence.find(i)

            if pos != -1:
                for j in list_city:
                    pos = sentence.find(j)

                    if pos != -1:
                        self.func = func_no
                        self.area = sentence[pos:pos+3]
                        break
            
            if self.area != "":
                break


    def main(self, sentence):
        
        if self.func == '0': self.CheckFunc(sentence, list_food_dic, '1')

        if self.func == '0': self.CheckFunc(sentence, list_play_dic, '2')
        
        if self.func == '0': self.CheckFunc(sentence, list_weather_dic, '3')


        if self.func == '0':
            content = "error"
        
        elif self.func == '1':
            content = IFoodie().crawler(self.area)
        
        elif self.func == '2':
            content = okgo().crawler(self.area)
        
        elif self.func == '3':
            content = weather().crawler(self.area)
        
        else:
            content = "error"

        return content


for i in range(0,3):
    sen = ["台南市天氣", "台北市美食", "基隆市景點"]

    reply = check().main(sen[i])
    print(reply)
    time.sleep(2)
