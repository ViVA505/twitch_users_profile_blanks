
import requests
from typing import (List, Dict,
                    Tuple)
from PIL import (Image, ImageDraw,
                 ImageFont)
import os
import textwrap



class TwitchCardGenerator:
    def __init__(self, api_handler, font_path: str = "", color: Tuple[int, int, int, int] = (255, 215, 0, 255) ):
        self.api_handler = api_handler
        self.font_path = font_path
        self.color = color
        self.not_found_users = []

    def _download_image(self, url: str, filename: str) -> None:
        response = requests.get(url)
        with open(filename, 'wb') as f:
            f.write(response.content)

    def _create_card(self, user_data: Dict, output_path: str) -> None:
        avatar_url = user_data['profile_image_url']
        avatar_filename = f"temp_avatar_{user_data['login']}.jpg"
        self._download_image(avatar_url, avatar_filename)

        # загружаем аватар как фоновое изображение или иначе хуйня получается
        img = Image.open(avatar_filename).convert("RGBA")
        img = img.resize((800, 800))


        overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)

        # сеттинг текста
        text = user_data['display_name']
        max_width = img.width - 100  # Отступы по бокам
        max_font_size = 150
        min_font_size = 30
        optimal_font_size = max_font_size

        for font_size in range(max_font_size, min_font_size, -2):
            try:
                font = ImageFont.truetype(self.font_path, font_size)
            except:
                font = ImageFont.load_default()

            text_bbox = draw.textbbox((0, 0), text, font=font)
            text_width = text_bbox[2] - text_bbox[0]

            if text_width <= max_width:
                optimal_font_size = font_size
                break

        # мемас сосал
        lines = [text]
        if optimal_font_size == min_font_size:
            max_chars = int(max_width / (min_font_size * 0.6))  # Примерный расчет
            lines = textwrap.wrap(text, width=max_chars)

        try:
            font = ImageFont.truetype(self.font_path, optimal_font_size)
        except:
            font = ImageFont.load_default()

        line_heights = [draw.textbbox((0, 0), line, font=font)[3] for line in lines]
        total_height = sum(line_heights) + 10 * (len(lines) - 1)

        y = img.height - total_height - 50
        if y < 20:
            y = 20


        for line in lines:
            text_bbox = draw.textbbox((0, 0), line, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            x = (img.width - text_width) // 2

            border_size = 10
            border_color = (0, 0, 0, 255)

            # рисуем обводку в 8 направлениях для большей толщины в векторной позиции или иначе блять НИХУЯ НЕ ВИДНО ТАЙЛПЕНИС Я ТВОЙ РОТ ЕБАЛ
            for dx in [-border_size, 0, border_size]:
                for dy in [-border_size, -border_size // 2, 0, border_size // 2, border_size]:
                    if dx == 0 and dy == 0:
                        continue
                    draw.text((x + dx, y + dy), line, font=font, fill=border_color)

            # доп., слои для плотной обводки(ендичан сосал)
            for _ in range(2):
                for dx in [-border_size + 1, 0, border_size - 1]:
                    for dy in [-border_size + 1, 0, border_size - 1]:
                        if dx == 0 and dy == 0:
                            continue
                        draw.text((x + dx, y + dy), line, font=font, fill=border_color)

            draw.text((x, y), line, font=font, fill=self.color)

            y += line_heights[lines.index(line)] + 10

        Image.alpha_composite(img, overlay).convert("RGB").save(output_path)
        os.remove(avatar_filename)

    def generate_all_cards(self, logins: List[str], output_dir: str = "assets/cards"):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        users_data = self.api_handler.get_users_data(logins)

        found_logins = {user['login'].lower() for user in users_data}

        self.not_found_users = [
            login for login in logins
            if login.lower() not in found_logins
        ]

        if self.not_found_users:
            print("\nСледующие юзеры не найдены:")
            for user in self.not_found_users:
                print(f" - {user}")

            with open("not_found_users.txt", "w") as f:
                f.write("\n".join(self.not_found_users))
            print("\nСписок ненайденных пользователей сохранен в not_found_users.txt")

        for user in users_data:
            filename = f"{output_dir}/{user['login']}_card.jpg"
            self._create_card(user, filename)
            print(f"Создана карточка: {filename}")