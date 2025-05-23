from back.TwitchAPI.handler import TwitchAPIHandler
from back.TwitchAPI.cardgenerator import TwitchCardGenerator






if __name__ == "__main__":

    # айдишник и секрет здесь получать -- https://dev.twitch.tv/ (если не похуй станет добавлю чтобы вы могли просто через твич oauth зайди и  все)
    CLIENT_ID = ""
    CLIENT_SECRET = ""

    font_path = "" # путь к вашему шрифту которой вы хотите юзать в качестве текста на профиле чаттера(string)
    color_text = (255, 215, 0, 255) # цвет для текста(RGB , 4(int))  -- пример базового --> (255, 215, 0, 255)

    api_handler = TwitchAPIHandler(CLIENT_ID, CLIENT_SECRET)
    generator = TwitchCardGenerator(api_handler, font_path, color_text)


     # сюда юзеров вписываете(добавлю потом поддержку ткст файла чтобы брать оттуда ники)
    users =  [
    "peacefull02"
]

    generator.generate_all_cards(users)