import json
import os

DATA_FILE = "music.json"

#загрузка данных из файла
def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r', encoding="utf-8") as f:
        return json.load(f)
    
#сохранение данных в файл
def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

#добавление трека
def add_music(data, music):
    for b in data:
        if b["id"] == music["id"]:
            print("ошибка: такой id уже используется")
            return False
    data.append(music)
    save_data(data)
    print("трек добавлен")
    return True
    
#получаем трек по id
def get_music(data, music_id):
    for music in data:
        if music['id'] == music_id:
            return music
    return None
    
#изменение данных по id
def update_music(data, music_id, new_fields):
    for music in data:
        if music["id"] == music_id:
            music.update(new_fields)
            save_data(data)
            print("данные обновлены")
            return True
    
    print("ошибка: трек не найден")
    return False

#удаление трека по id
def delete_music(data, music_id):
    for i, music in enumerate(data):
        if music["id"] == music_id:
            del data[i]
            save_data(data)
            print("трек удален")
            return True
    
    print("ошибка: трек не найден")
    return False

def parse_put_command(cmd):
    parts = cmd.split(',', 4)
    
    return {
        "id": int(parts[0].strip()),
        "title": parts[1].strip(),
        "author": parts[2].strip(),
        "duration": parts[3].strip(),
        "rating": int(parts[4].strip())
    }

def main(): 
    data = load_data()
    print("плейлист")
    while True:
        print("\nменю:")
        print("1. добавить трек")
        print("2. найти трек по id")
        print("3. обновить трек")
        print("4. удалить трек")
        print("5. плейлист")
        print("0. выйти")

        choice = input("выберите действие (0-5): ").strip()

        if choice == '1':
            try:
                inp = input("введите: id, название, автора, длительность трека и оценку треку через запятую:\n")
                music_data = parse_put_command(inp)
                add_music(data, music_data)
            except Exception as e:
                print("ошибка, при добавлении трека. Проверьте формат", e)

        elif choice == '2':
            try:
                music_id = int(input("введите id трека:"))
                music = get_music(data, music_id)
                if music:
                    print(music)
                else:
                    print("трек не найден")
            
            except Exception:
                print("ошибка при вводе id")

        elif choice == '3':
            try:
                music_id = int(input("введите id трека для обновления: "))
                print("введите новое название, автора, длительность трека и оценку. Например(title: новое название, rating: новый рейтинг) ")
                raw = input()
                new_data = {}
                for pair in raw.split(","):
                    key, val = pair.split(":", 1)
                    val = val.strip()
                    new_data[key.strip()] = int(val) if key.strip() in ["rating", "id"] else val
                    update_music(data, music_id, new_data)
            
            except Exception:
                print("ошибка в формате данных для обновления")
        
        elif choice == '4':
            try:
                music_id = int(input("введите id для удаления:"))
                delete_music(data, music_id)
            
            except Exception: 
                print("ошибка при в воде id")

        elif choice == '5':
            print("список всех треков:")
            for music in data:
                print(music)
        
        elif choice == "0":
            print("выход")
            break
        else:
            print("неизвестный пункт в меню")

if __name__ == "__main__":
    main()