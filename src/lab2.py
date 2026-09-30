"""
Лабораторна робота № 2: Створення та використання функцій, реалізація рекурсії
Варіант: 12
Тема: Аналіз статистики матчів та героїв (На основі Доти) (Dota 2 Esports)
Студент: Шульга Дмитро Ігорович
"""

from functools import reduce
from typing import Callable, List, Dict, Tuple, Any


# --- 1. Звичайні функції ---

def calculate_kda(kills: int, deaths: int, assists: int) -> float:
    """
    Обчислює показник KDA гравця.
    Якщо смертей 0, показник розраховується відносно 1 умовної смерті.
    """
    effective_deaths = max(1, deaths)
    return round((kills + assists) / effective_deaths, 2)


def estimate_winrate_delta(current_mmr: int, target_mmr: int) -> int:
    """
    Розраховує кількість чистих перемог (+25 MMR за гру),
    необхідних для досягнення цільового рейтингу.
    """
    if target_mmr <= current_mmr:
        return 0
    return (target_mmr - current_mmr + 24) // 25


# --- 2. Функція з параметрами за замовчуванням ---

def calculate_gpm(total_gold: int, duration_seconds: int, is_turbo: bool = False) -> float:
    """
    Розраховує золото за хвилину (GPM).
    За замовчуванням рахує звичайний режим (is_turbo=False).
    """
    if duration_seconds <= 0:
        return 0.0
    minutes = duration_seconds / 60.0
    gpm = total_gold / minutes
    return round(gpm * 0.75 if is_turbo else gpm, 2)


# --- 3. Функція зі змінною кількістю аргументів (*args) ---

def calculate_average_metric(metric_name: str, *values: float) -> float:
    """
    Обчислює середнє значення для довільної кількості переданих метрик.
    """
    if not values:
        return 0.0
    avg = sum(values) / len(values)
    return round(avg, 2)


# --- 4. Лямбда-функції ---

# Розрахунок чистого нетворсу з вирахуванням вартості байбека (buyback cost)
calculate_net_worth_reserve = lambda networth, buyback_cost: max(0, networth - buyback_cost)

# Форматування рядка героя у стислий вигляд
format_match_tag = lambda hero, kda: f"[{hero.upper()} | KDA: {kda:.2f}]"


# --- 5. Рекурсивна функція ---

def recursive_find_best_match(matches: List[Dict[str, Any]], start: int, end: int) -> Dict[str, Any]:
    """
    Рекурсивно методом 'Розділяй і володарюй' знаходить матч із максимальним KDA.
    Базовий випадок (уникнення нескінченної рекурсії):
    коли підмасив звужується до одного елемента (start == end).
    """
    # Базовий випадок
    if start == end:
        return matches[start]

    # Рекурсивний випадок
    mid = (start + end) // 2
    best_left = recursive_find_best_match(matches, start, mid)
    best_right = recursive_find_best_match(matches, mid + 1, end)

    kda_left = calculate_kda(best_left["kills"], best_left["deaths"], best_left["assists"])
    kda_right = calculate_kda(best_right["kills"], best_right["deaths"], best_right["assists"])

    return best_left if kda_left >= kda_right else best_right


# --- 6. Функціональне програмування та функція вищого порядку ---

def filter_and_transform_matches(
    data: List[Dict[str, Any]],
    predicate: Callable[[Dict[str, Any]], bool],
    transform: Callable[[Dict[str, Any]], Any]
) -> List[Any]:
    """
    Власна функція вищого порядку:
    приймає предикат для фільтрації та функцію трансформації результату.
    """
    return [transform(item) for item in data if predicate(item)]


# Набір даних (20 матчів)
MATCHES_DATA: List[Dict[str, Any]] = [
    {"id": 1, "hero": "Morphling", "kills": 14, "deaths": 2, "assists": 8, "gold": 28400, "duration": 2400, "win": True},
    {"id": 2, "hero": "Invoker", "kills": 9, "deaths": 5, "assists": 14, "gold": 21000, "duration": 2300, "win": True},
    {"id": 3, "hero": "Pudge", "kills": 3, "deaths": 11, "assists": 9, "gold": 11500, "duration": 1900, "win": False},
    {"id": 4, "hero": "Storm Spirit", "kills": 18, "deaths": 4, "assists": 12, "gold": 31000, "duration": 2600, "win": True},
    {"id": 5, "hero": "Rubick", "kills": 2, "deaths": 8, "assists": 22, "gold": 13400, "duration": 2550, "win": True},
    {"id": 6, "hero": "Anti-Mage", "kills": 8, "deaths": 3, "assists": 4, "gold": 32000, "duration": 2100, "win": True},
    {"id": 7, "hero": "Crystal Maiden", "kills": 1, "deaths": 12, "assists": 15, "gold": 9800, "duration": 1800, "win": False},
    {"id": 8, "hero": "Shadow Fiend", "kills": 11, "deaths": 7, "assists": 6, "gold": 24500, "duration": 2200, "win": False},
    {"id": 9, "hero": "Ember Spirit", "kills": 13, "deaths": 3, "assists": 17, "gold": 27800, "duration": 2500, "win": True},
    {"id": 10, "hero": "Faceless Void", "kills": 7, "deaths": 6, "assists": 5, "gold": 22000, "duration": 2400, "win": False},
    {"id": 11, "hero": "Lion", "kills": 4, "deaths": 9, "assists": 18, "gold": 12200, "duration": 2350, "win": True},
    {"id": 12, "hero": "Terrorblade", "kills": 10, "deaths": 2, "assists": 7, "gold": 34000, "duration": 2700, "win": True},
    {"id": 13, "hero": "Queen of Pain", "kills": 12, "deaths": 5, "assists": 11, "gold": 23000, "duration": 2150, "win": True},
    {"id": 14, "hero": "Axe", "kills": 6, "deaths": 8, "assists": 10, "gold": 16500, "duration": 2000, "win": False},
    {"id": 15, "hero": "Puck", "kills": 15, "deaths": 1, "assists": 16, "gold": 29000, "duration": 2300, "win": True},
    {"id": 16, "hero": "Slark", "kills": 16, "deaths": 4, "assists": 9, "gold": 28900, "duration": 2450, "win": True},
    {"id": 17, "hero": "Tidehunter", "kills": 2, "deaths": 6, "assists": 19, "gold": 15000, "duration": 2100, "win": True},
    {"id": 18, "hero": "Phantom Assassin", "kills": 5, "deaths": 9, "assists": 4, "gold": 18000, "duration": 1950, "win": False},
    {"id": 19, "hero": "Lina", "kills": 11, "deaths": 4, "assists": 13, "gold": 26500, "duration": 2250, "win": True},
    {"id": 20, "hero": "Juggernaut", "kills": 9, "deaths": 3, "assists": 8, "gold": 25500, "duration": 2300, "win": True},
]


# --- 7. Інтерактивна програма (Текстове меню) ---

def main():
    print("=" * 60)
    print("СИСТЕМА АНАЛІЗУ СТАТИСТИКИ КІБЕРСПОРТИВНИХ МАТЧІВ")
    print("=" * 60)

    while True:
        print("\nОберіть дію:")
        print("1. Розрахувати KDA для власного матчу")
        print("2. Розрахувати GPM (Золото за хвилину)")
        print("3. Обчислити середній KDA за серію матчів (*args)")
        print("4. Рекурсивний пошук найкращого матчу у вибірці")
        print("5. Функціональний аналіз даних (filter, map, reduce)")
        print("6. Власна функція вищого порядку (фільтр перемог)")
        print("7. Розрахувати перемоги до цільового MMR")
        print("8. Вийти")

        choice = input("Введіть номер пункту (1-8): ").strip()

        try:
            if choice == "1":
                k = int(input("Кількість вбивств (Kills): "))
                d = int(input("Кількість смертей (Deaths): "))
                a = int(input("Кількість допомог (Assists): "))
                if k < 0 or d < 0 or a < 0:
                    raise ValueError("Показники не можуть бути від'ємними.")
                kda = calculate_kda(k, d, a)
                print(f"-> Розрахований KDA: {kda}")

            elif choice == "2":
                gold = int(input("Загальне золото: "))
                sec = int(input("Тривалість матчу (в секундах): "))
                mode = input("Це режим Turbo? (y/n, за замовчуванням n): ").strip().lower() == "y"
                if gold < 0 or sec <= 0:
                    raise ValueError("Некоректні дані часу або золота.")
                gpm = calculate_gpm(gold, sec, is_turbo=mode)
                print(f"-> Середній GPM: {gpm}")

            elif choice == "3":
                raw_kdas = input("Введіть значення KDA через пробіл (наприклад: 3.5 4.0 12.2): ")
                values = [float(x) for x in raw_kdas.split()]
                if not values:
                    print("Список порожній.")
                else:
                    avg = calculate_average_metric("KDA", *values)
                    print(f"-> Середній KDA серії: {avg}")

            elif choice == "4":
                best = recursive_find_best_match(MATCHES_DATA, 0, len(MATCHES_DATA) - 1)
                best_kda = calculate_kda(best["kills"], best["deaths"], best["assists"])
                print(f"-> Найкращий матч знайдено рекурсивно:")
                print(f"   Матч ID: {best['id']}, Герой: {best['hero']}")
                print(f"   Рахунок: {best['kills']}/{best['deaths']}/{best['assists']} (KDA: {best_kda})")

            elif choice == "5":
                # filter: відбір тільки переможних матчів
                wins = list(filter(lambda m: m["win"], MATCHES_DATA))
                # map: розрахунок KDA для переможних матчів
                kdas = list(map(lambda m: calculate_kda(m["kills"], m["deaths"], m["assists"]), wins))
                # reduce: загальна сума вбивств у переможних іграх
                total_kills = reduce(lambda acc, m: acc + m["kills"], wins, 0)

                print(f"-> Переможних матчів у базі: {len(wins)} з {len(MATCHES_DATA)}")
                print(f"-> Загальна кількість вбивств у перемогах (reduce): {total_kills}")
                print(f"-> Середній KDA у перемогах: {round(sum(kdas)/len(kdas), 2)}")

            elif choice == "6":
                # Демонстрація власної функції вищого порядку
                top_heroes = filter_and_transform_matches(
                    MATCHES_DATA,
                    predicate=lambda m: m["kills"] >= 12,
                    transform=lambda m: f"{m['hero']} ({m['kills']} kills)"
                )
                print("-> Герої з 12+ вбивствами (через функцію вищого порядку):")
                for hero in top_heroes:
                    print(f"   - {hero}")

            elif choice == "7":
                cur = int(input("Поточний MMR: "))
                target = int(input("Цільовий MMR: "))
                diff = estimate_winrate_delta(cur, target)
                print(f"-> Необхідно чистих перемог (+25 за кожну): {diff}")

            elif choice == "8":
                print("Роботу завершено. Успіхів у кодингу!")
                break
            else:
                print("Невідомий пункт меню. Будь ласка, вкажіть число від 1 до 8.")

        except ValueError as err:
            print(f"Помилка введення: {err}. Спробуйте ще раз.")


if __name__ == "__main__":
    main()
