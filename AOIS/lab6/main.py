RU_ALPHABET = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
H = 20  
B = 0 


def char_value(ch: str) -> int:
    ch = ch.upper()
    if ch in RU_ALPHABET:
        return RU_ALPHABET.index(ch)
    return 0


def key_to_V(key: str) -> int:

    key = key.strip()
    b1 = char_value(key[0]) if len(key) >= 1 else 0
    b2 = char_value(key[1]) if len(key) >= 2 else 1
    return b1 * 33 + b2


def hash_addr(V: int) -> int:
    return V % H + B

def make_empty_row() -> dict:
    return dict(id_key="", C=0, U=0, T=1, L=0, D=0, P0=-1, Pi="")


class HashTable:
    def __init__(self, size: int = H, base: int = B):
        self.size = size
        self.base = base
        self.table = [make_empty_row() for _ in range(size)]

    def _find_free(self, start: int) -> int:
        for i in range(self.size):
            idx = (start + i) % self.size
            if self.table[idx]["U"] == 0:
                return idx
        return -1 

    def insert(self, key: str, data: str) -> str:
        V = key_to_V(key)
        h = hash_addr(V)
        row = self.table[h]
        found = self._search_row(key)
        if found is not None:
            return f"[!] Ключ «{key}» уже есть в таблице (строка {found})."

        if row["U"] == 0:
            self.table[h] = dict(id_key=key, C=0, U=1, T=1, L=0, D=0, P0=-1, Pi=data)
            return f"[+] «{key}» -> строка {h} (V={V}, h={h})"
        else:
            free = self._find_free((h + 1) % self.size)
            if free == -1:
                return "[!] Таблица полна!"
            cur = h
            while self.table[cur]["T"] == 0 and self.table[cur]["P0"] != -1:
                cur = self.table[cur]["P0"]
            self.table[cur]["T"] = 0
            self.table[cur]["P0"] = free
            self.table[cur]["C"] = 1
            self.table[free] = dict(id_key=key, C=0, U=1, T=1, L=0, D=0, P0=-1, Pi=data)
            return (f"[+] «{key}» -> строка {free} (V={V}, h={h}, коллизия->пробинг->{free})")

    def _search_row(self, key: str):
        V = key_to_V(key)
        h = hash_addr(V)
        cur = h
        while True:
            row = self.table[cur]
            if row["U"] == 0:
                return None
            if row["id_key"] == key and row["D"] == 0:
                return cur
            if row["T"] == 1 or row["P0"] == -1:
                return None
            cur = row["P0"]

    def search(self, key: str) -> str:
        idx = self._search_row(key)
        if idx is None:
            return f"[-] Ключ «{key}» не найден."
        row = self.table[idx]
        return (f"[OK] Найдено в строке {idx}: ID={row['id_key']}, "
                f"Данные={row['Pi']}, "
                f"C={row['C']} U={row['U']} T={row['T']} D={row['D']} P0={row['P0']}")

    def delete(self, key: str) -> str:
        V = key_to_V(key)
        h = hash_addr(V)

        idx = self._search_row(key)
        if idx is None:
            return f"[-] Ключ «{key}» не найден — удаление невозможно."

        row = self.table[idx]

        if row["T"] == 1 and row["P0"] == -1:
            self.table[idx] = make_empty_row()
            self._fix_prev_chain(idx)
            return f"[x] «{key}» (строка {idx}) удалена (одиночная)."
        if row["T"] == 1:
            prev = self._find_prev(h, idx)
            self.table[idx] = make_empty_row()
            if prev is not None:
                self.table[prev]["T"] = 1
                self.table[prev]["P0"] = -1
                prev_h = hash_addr(key_to_V(self.table[prev]["id_key"]))
                if self.table[prev]["T"] == 1 and self.table[prev]["P0"] == -1:
                    if prev_h == prev:
                        self.table[prev]["C"] = 0
            return f"[x] «{key}» (строка {idx}) удалена (конец цепочки)."
        next_idx = row["P0"]
        next_row = self.table[next_idx]
        self.table[idx] = dict(
            id_key=next_row["id_key"], C=next_row["C"], U=next_row["U"],
            T=next_row["T"], L=next_row["L"], D=next_row["D"],
            P0=next_row["P0"], Pi=next_row["Pi"]
        )
        self.table[idx]["C"] = 1
        self.table[next_idx] = make_empty_row()
        return (f"[x] «{key}» (строка {idx}) удалена; "
                f"содержимое строки {next_idx} перемещено на место {idx}.")

    def _find_prev(self, start: int, target: int):
        cur = start
        while True:
            if self.table[cur]["P0"] == target:
                return cur
            if self.table[cur]["T"] == 1 or self.table[cur]["P0"] == -1:
                return None
            cur = self.table[cur]["P0"]

    def _fix_prev_chain(self, freed_idx: int):
        for i in range(self.size):
            if self.table[i]["U"] == 1 and self.table[i]["P0"] == freed_idx:
                self.table[i]["P0"] = -1
                self.table[i]["T"] = 1
                break

    def fill_factor(self) -> float:
        occupied = sum(1 for r in self.table if r["U"] == 1)
        return occupied / self.size

    def display(self):
        print("\n" + "=" * 90)
        print(f"{'№':>3} | {'ID':<20} | C U T L D | {'P0':>4} | Данные (Pi)")
        print("-" * 90)
        for i, row in enumerate(self.table):
            if row["U"] == 0:
                print(f"{i:>3} | {'(свободно)':<20} |           |      |")
            else:
                flags = f"{row['C']} {row['U']} {row['T']} {row['L']} {row['D']}"
                p0 = str(row["P0"]) if row["P0"] != -1 else "—"
                d_mark = " [удалена]" if row["D"] == 1 else ""
                print(f"{i:>3} | {row['id_key']:<20} | {flags} | {p0:>4} | {row['Pi']}{d_mark}")
        print("=" * 90)
        occ = sum(1 for r in self.table if r["U"] == 1)
        print(f"Заполнено: {occ}/{self.size} строк  |  Коэффициент заполнения: {self.fill_factor():.2f}\n")

    def show_vh(self, keys):
        print("\n{:<22} {:>6} {:>6}".format("Ключевое слово", "V", "h(V)"))
        print("-" * 36)
        for k in keys:
            V = key_to_V(k)
            h = hash_addr(V)
            print(f"{k:<22} {V:>6} {h:>6}")
        print()


INITIAL_DATA = [
    ("Автомат",    "Стрелковое оружие, пистолет-пулемёт под промежуточный патрон"),
    ("Артиллерия", "Род войск; огнестрельное оружие крупного калибра"),
    ("Бронетанк",  "Бронетанковые войска; техника с бронезащитой и гусеничным ходом"),
    ("Батальон",   "Воинское подразделение, обычно 3–4 роты"),
    ("Вертолёт",   "Летательный аппарат вертикального взлёта; военная авиация"),
    ("Граната",    "Ручное взрывное устройство; вид метательного оружия"),
    ("Дивизия",    "Основное тактическое соединение сухопутных войск"),
    ("Дрон",       "Беспилотный летательный аппарат; разведка и ударные задачи"),
    ("Зенитка",    "Зенитное орудие для поражения воздушных целей"),
    ("Карабин",    "Укороченная винтовка; оружие кавалерии и спецподразделений"),
    ("Миномёт",    "Гладкоствольное орудие навесного огня"),
    ("Ракета",     "Реактивный снаряд; стратегическое и тактическое оружие"),
]


def menu():
    ht = HashTable(H, B)
    print("\n=== Хеш-таблица: Армия и вооружение (Вариант 10) ===")
    print("Инициализация таблицы начальными данными...\n")
    keys_init = [k for k, _ in INITIAL_DATA]
    ht.show_vh(keys_init)
    for key, data in INITIAL_DATA:
        print(ht.insert(key, data))

    while True:
        print("\n--- МЕНЮ ---")
        print("1. Показать таблицу")
        print("2. Поиск по ключевому слову")
        print("3. Добавить запись")
        print("4. Удалить запись")
        print("5. Показать V и h для ключевых слов")
        print("6. Коэффициент заполнения")
        print("0. Выход")
        choice = input("Выберите действие: ").strip()

        if choice == "1":
            ht.display()

        elif choice == "2":
            key = input("Введите ключевое слово: ").strip()
            print(ht.search(key))

        elif choice == "3":
            key = input("Ключевое слово: ").strip()
            data = input("Данные: ").strip()
            V = key_to_V(key)
            h = hash_addr(V)
            print(f"  V={V}, h(V)={h}")
            print(ht.insert(key, data))

        elif choice == "4":
            key = input("Ключевое слово для удаления: ").strip()
            print(ht.delete(key))

        elif choice == "5":
            raw = input("Введите ключевые слова через запятую: ")
            keys = [k.strip() for k in raw.split(",") if k.strip()]
            ht.show_vh(keys)

        elif choice == "6":
            occ = sum(1 for r in ht.table if r["U"] == 1)
            print(f"Занято: {occ}/{ht.size}  |  Коэффициент заполнения: {ht.fill_factor():.2f}")

        elif choice == "0":
            print("До свидания!")
            break
        else:
            print("Неверный ввод.")


if __name__ == "__main__":
    menu()