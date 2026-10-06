import os
from pathlib import Path

def get_sort_key(name):
    """Ключ сортировки: если название начинается с цифры, сортируем по числу, иначе по алфавиту"""
    num_part = ''
    for char in name:
        if char.isdigit():
            num_part += char
        else:
            break
    
    if num_part:
        return (0, int(num_part), name.lower())
    else:
        return (1, 0, name.lower())

def find_txt_files(root_dir):
    """Находит все .txt файлы в папке скрипта и подпапках"""
    txt_files = []
    root_path = Path(root_dir)
    
    for txt_file in root_path.rglob('*.txt'):
        txt_files.append(txt_file)
    
    return txt_files

def build_display_name(txt_path, root_dir):
    """Строит отображаемое имя: папка/файл или просто файл"""
    root_path = Path(root_dir).resolve()
    file_path = txt_path.resolve()
    
    relative = file_path.relative_to(root_path)
    
    parts = list(relative.parts)
    parts[-1] = Path(parts[-1]).stem
    
    if len(parts) == 1:
        return parts[0]
    else:
        return '/'.join(parts)

def read_txt_content(txt_path):
    """Читает содержимое txt файла, пробуя разные кодировки"""
    for encoding in ('utf-8', 'utf-8-sig', 'cp1251', 'latin-1'):
        try:
            with open(txt_path, 'r', encoding=encoding) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
    # Если ничего не подошло — читаем с игнорированием ошибок
    with open(txt_path, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read()

def main():
    # Папка, где находится сам скрипт
    script_dir = Path(__file__).resolve().parent
    
    txt_files = find_txt_files(script_dir)
    
    if not txt_files:
        print("Не найдено .txt файлов в папке скрипта")
        return
    
    def sort_key(file_path):
        relative = file_path.resolve().relative_to(script_dir)
        parts = relative.parts
        
        key = []
        for part in parts[:-1]:
            key.append(get_sort_key(part))
        key.append(get_sort_key(Path(parts[-1]).stem))
        
        return key
    
    txt_files.sort(key=sort_key)
    
    output_parts = []
    
    for i, txt_file in enumerate(txt_files):
        display_name = build_display_name(txt_file, script_dir)
        content = read_txt_content(txt_file)
        
        # 3 переноса строки перед каждым заголовком, кроме первого
        if i != 0:
            output_parts.append('\n\n\n')
        
        # Заголовок с разделителями
        output_parts.append(f'===\n{display_name}\n===\n')
        
        # Содержимое файла
        output_parts.append(content)
        
        # Гарантируем перевод строки в конце блока (если файл не заканчивается на \n)
        if not content.endswith('\n'):
            output_parts.append('\n')
    
    # index.html создаётся в той же папке, что и скрипт
    output_file = script_dir / 'index.html'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(''.join(output_parts))
    
    print(f"Обработано файлов: {len(txt_files)}")
    print(f"Результат записан в: {output_file}")

if __name__ == '__main__':
    main()