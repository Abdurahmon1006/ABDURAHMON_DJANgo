import os
import shutil
from pathlib import Path
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.core.files import File
from django.core.files.storage import default_storage
from apps.models import game


class Command(BaseCommand):
    help = "O'yinlar papkasidan o'yinlarni avtomatik yuklaydi"

    def add_arguments(self, parser):
        parser.add_argument(
            '--update',
            action='store_true',
            help="Mavjud o'yinlarni ham yangilaydi",
        )

    def handle(self, *args, **options):
        # O'yinlar papkasini aniqlash
        games_folder = Path(settings.BASE_DIR) / "o'yinlar"
        
        if not games_folder.exists():
            raise CommandError(f"O'yinlar papkasi topilmadi: {games_folder}")

        self.stdout.write(f"O'yinlar papkasi: {games_folder}")
        
        # Static files papkasini aniqlash (development uchun static folder)
        if settings.STATICFILES_DIRS:
            static_base_folder = Path(settings.STATICFILES_DIRS[0])
        else:
            static_base_folder = Path(settings.BASE_DIR) / "static"
        
        static_games_folder = static_base_folder / "oyinlar"
        static_games_folder.mkdir(parents=True, exist_ok=True)

        loaded_games = 0
        updated_games = 0
        skipped_games = 0

        # O'yinlar papkasidagi barcha papkalarni ko'rib chiqish
        for game_folder in games_folder.iterdir():
            if not game_folder.is_dir():
                continue

            game_name = game_folder.name
            self.stdout.write(f"\nO'yin papkasi topildi: {game_name}")

            # name.txt faylini o'qish
            name_file = game_folder / "name.txt"
            if not name_file.exists():
                self.stdout.write(
                    self.style.WARNING(f"  name.txt fayli topilmadi: {game_folder}")
                )
                continue

            try:
                with open(name_file, 'r', encoding='utf-8') as f:
                    display_name = f.read().strip()
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"  name.txt faylini o'qishda xato: {e}")
                )
                continue

            if not display_name:
                display_name = game_name.replace('_', ' ').replace('-', ' ').title()

            self.stdout.write(f"  O'yin nomi: {display_name}")

            # Asosiy HTML faylini topish
            html_files = list(game_folder.glob("*.html"))
            if not html_files:
                self.stdout.write(
                    self.style.WARNING(f"  HTML fayl topilmadi: {game_folder}")
                )
                continue

            main_html = html_files[0]  # Birinchi HTML faylini olish
            self.stdout.write(f"  HTML fayl: {main_html.name}")

            # O'yin papkasini static ga ko'chirish
            static_game_folder = static_games_folder / game_name
            
            try:
                # Agar mavjud bo'lsa, avval o'chirish
                if static_game_folder.exists():
                    shutil.rmtree(static_game_folder)
                
                # Butun papkani ko'chirish
                shutil.copytree(game_folder, static_game_folder)
                self.stdout.write(
                    self.style.SUCCESS(f"  Fayllar ko'chirildi: {static_game_folder}")
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"  Fayllarni ko'chirishda xato: {e}")
                )
                continue

            # O'yin havolasini tuzish
            game_url = f"/static/oyinlar/{game_name}/{main_html.name}"

            # Kategoriyani aniqlash (fayl nomi asosida)
            category = self.detect_category(game_name, display_name)

            # Tavsifni yaratish
            description = f"{display_name} - interaktiv HTML o'yin"

            # Rasmi uchun o'yin papkasidan rasm topish yoki default yaratish
            screenshot_path = self.find_game_image(game_folder, game_name)

            # Ma'lumotlar bazasida tekshirish
            existing_game = game.objects.filter(nomi=display_name).first()

            if existing_game:
                if options['update']:
                    # Mavjud o'yinni yangilash
                    existing_game.link = game_url
                    existing_game.kategoriya = category
                    existing_game.tavsif = description
                    if screenshot_path:
                        with open(screenshot_path, 'rb') as img_file:
                            existing_game.rasmi.save(
                                f"{game_name}_image.png",
                                File(img_file),
                                save=False
                            )
                    existing_game.save()
                    updated_games += 1
                    self.stdout.write(
                        self.style.SUCCESS(f"  ✅ O'yin yangilandi: {display_name}")
                    )
                else:
                    skipped_games += 1
                    self.stdout.write(
                        self.style.WARNING(f"  ⚠️  O'yin allaqachon mavjud: {display_name}")
                    )
            else:
                # Yangi o'yinni yaratish
                new_game = game(
                    nomi=display_name,
                    tavsif=description,
                    link=game_url,
                    kategoriya=category
                )

                # Rasmni qo'shish
                if screenshot_path:
                    with open(screenshot_path, 'rb') as img_file:
                        new_game.rasmi.save(
                            f"{game_name}_image.png",
                            File(img_file),
                            save=False
                        )

                new_game.save()
                loaded_games += 1
                self.stdout.write(
                    self.style.SUCCESS(f"  ✅ Yangi o'yin qo'shildi: {display_name}")
                )

        # Yakuniy natija
        self.stdout.write("\n" + "="*50)
        self.stdout.write(
            self.style.SUCCESS(f"Yangi yuklangan o'yinlar: {loaded_games}")
        )
        self.stdout.write(
            self.style.SUCCESS(f"Yangilangan o'yinlar: {updated_games}")
        )
        self.stdout.write(
            self.style.WARNING(f"O'tkazib yuborilgan o'yinlar: {skipped_games}")
        )
        self.stdout.write(
            self.style.SUCCESS(f"Jami ishlov berilgan: {loaded_games + updated_games + skipped_games}")
        )

    def detect_category(self, folder_name, display_name):
        """O'yin kategoriyasini fayl nomi yoki nomi asosida aniqlash"""
        folder_lower = folder_name.lower()
        name_lower = display_name.lower()
        
        # Kategoriyalarni aniqlash logikasi
        if any(word in folder_lower or word in name_lower for word in ['tic', 'tac', 'toe', 'x-o', 'chess', 'checkers']):
            return 'strategiya'
        elif any(word in folder_lower or word in name_lower for word in ['puzzle', 'sudoku', 'crossword', 'jigsaw']):
            return 'puzzle'
        elif any(word in folder_lower or word in name_lower for word in ['snake', 'tetris', 'pacman', 'arcade', 'pong']):
            return 'arkada'
        elif any(word in folder_lower or word in name_lower for word in ['football', 'soccer', 'basketball', 'sport']):
            return 'sport'
        elif any(word in folder_lower or word in name_lower for word in ['fight', 'war', 'battle', 'shooter', 'jang']):
            return 'jang'
        elif any(word in folder_lower or word in name_lower for word in ['adventure', 'quest', 'explore', 'sarguzasht']):
            return 'sarguzasht'
        else:
            return 'boshqa'

    def find_game_image(self, game_folder, game_name):
        """O'yin papkasidan rasmni topish yoki default 🎮 yaratish"""
        
        self.stdout.write(f"  Rasm qidirilmoqda: {game_folder}")
        
        # Rasm fayl kengaytmalari
        image_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.webp', '.bmp']
        
        # 1. Avval maxsus nomli rasmlarni qidirish
        priority_names = ['rasm', 'image', 'screenshot', 'preview', 'foto', 'rasmcha', 'picture']
        for name in priority_names:
            for ext in image_extensions:
                img_path = game_folder / f"{name}{ext}"
                if img_path.exists():
                    self.stdout.write(f"  ✅ Maxsus rasm topildi: {img_path.name}")
                    return img_path
        
        # 2. O'yin nomiga o'xshash rasm qidirish
        for ext in image_extensions:
            img_path = game_folder / f"{game_name}{ext}"
            if img_path.exists():
                self.stdout.write(f"  ✅ O'yin nomidagi rasm topildi: {img_path.name}")
                return img_path
        
        # 3. Papkadagi har qanday birinchi rasm faylni olish
        for ext in image_extensions:
            for img_file in game_folder.glob(f"*{ext}"):
                self.stdout.write(f"  ✅ Har qanday rasm topildi: {img_file.name}")
                return img_file
        
        # 4. Agar hech qanday rasm topilmasa, default 🎮 rasm yaratish
        self.stdout.write(f"  ⚠️  Papkada rasm topilmadi. Default rasm yaratilmoqda...")
        return self.create_default_game_image(game_name)
    
    def create_default_game_image(self, game_name):
        """Default 🎮 rasm yaratish"""
        try:
            from PIL import Image, ImageDraw, ImageFont
            
            # Temporary papka yaratish
            temp_folder = Path(settings.BASE_DIR) / "temp_images"
            temp_folder.mkdir(exist_ok=True)
            
            default_image_path = temp_folder / f"{game_name}_default.png"
            
            # Agar allaqachon mavjud bo'lsa, qaytarish
            if default_image_path.exists():
                self.stdout.write(f"  💾 Mavjud default rasm ishlatildi")
                return default_image_path
            
            # 400x300 o'lchamida rasm yaratish
            img = Image.new('RGB', (400, 300), color='#007BFF')
            draw = ImageDraw.Draw(img)
            
            # 🎮 emoji yozish
            try:
                # Windows emoji fontini ishlatish
                font = ImageFont.truetype("seguiemj.ttf", 100)
            except:
                try:
                    font = ImageFont.truetype("arial.ttf", 100)
                except:
                    font = ImageFont.load_default()
            
            # Emoji va matnni yozish
            emoji = "🎮"
            
            try:
                # Emoji'ni markazga joylashtirish
                bbox = draw.textbbox((0, 0), emoji, font=font)
                emoji_width = bbox[2] - bbox[0]
                emoji_height = bbox[3] - bbox[1]
                x = (400 - emoji_width) // 2
                y = (300 - emoji_height) // 2 - 20
                
                draw.text((x, y), emoji, font=font, fill='white')
                
                # "O'yin" matni qo'shish
                try:
                    text_font = ImageFont.truetype("arial.ttf", 24)
                except:
                    text_font = ImageFont.load_default()
                
                text = "O'yin"
                text_bbox = draw.textbbox((0, 0), text, font=text_font)
                text_width = text_bbox[2] - text_bbox[0]
                text_x = (400 - text_width) // 2
                text_y = y + emoji_height + 10
                
                draw.text((text_x, text_y), text, font=text_font, fill='white')
                
            except Exception as e:
                # Agar bbox ishlamasa, oddiy pozitsiyada yozish
                draw.text((150, 120), emoji, font=font, fill='white')
                draw.text((170, 200), "O'yin", font=font, fill='white')
            
            # Rasmni saqlash
            img.save(default_image_path)
            self.stdout.write(f"  ✅ Default rasm yaratildi: 🎮")
            return default_image_path
            
        except ImportError:
            self.stdout.write(
                self.style.WARNING(f"  ⚠️  PIL kutubxonasi o'rnatilmagan. Default rasm yaratilmadi.")
            )
            return None
        except Exception as e:
            self.stdout.write(
                self.style.WARNING(f"  ⚠️  Default rasm yaratishda xato: {e}")
            )
            return None
