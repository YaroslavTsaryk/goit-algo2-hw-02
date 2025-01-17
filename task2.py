from typing import List, Dict


def rod_cutting_memo(length: int, prices: List[int]) -> Dict:
    """
    Знаходить оптимальний спосіб розрізання через мемоізацію

    Args:
        length: довжина стрижня
        prices: список цін, де prices[i] — ціна стрижня довжини i+1

    Returns:
        Dict з максимальним прибутком та списком розрізів
    """

    # Тут повинен бути ваш код

    # Створення кешу
    dp = [-1] * (length + 1)
    cuts = [None] * (length + 1)  # Зберігання списків різів

    def solve(length):
        if length == 0:  # Базовий випадок
            return 0, []
        if dp[length] != -1:  # Якщо вже обчислено
            return dp[length], cuts[length]

        max_profit = 0
        best_cut = []
        for i in range(1, length + 1):
            if i <= len(prices):
                current_profit, current_cuts = solve(length - i)
                current_profit += prices[i - 1]
                if current_profit > max_profit:
                    max_profit = current_profit
                    best_cut = current_cuts + [i]

        dp[length] = max_profit
        cuts[length] = best_cut
        return dp[length], cuts[length]

    max_profit, cut_list = solve(length)
    # return max_profit, len(cut_list), cut_list

    return {
        "max_profit": max_profit,
        "cuts": cut_list,
        "number_of_cuts": len(cut_list) - 1,
    }


def rod_cutting_table(length: int, prices: List[int]) -> Dict:
    """
    Знаходить оптимальний спосіб розрізання через табуляцію

    Args:
        length: довжина стрижня
        prices: список цін, де prices[i] — ціна стрижня довжини i+1

    Returns:
        Dict з максимальним прибутком та списком розрізів
    """

    # Тут повинен бути ваш код
    dp = [0] * (length + 1)
    cuts = [[] for _ in range(length + 1)]  # Зберігання списків різів

    # Побудова рішення
    for length in range(1, length + 1):
        max_profit = 0
        best_cut = []
        for cut in range(1, length + 1):
            if cut <= len(prices):
                current_profit = prices[cut - 1] + dp[length - cut]
                if current_profit > max_profit:
                    max_profit = current_profit
                    best_cut = cuts[length - cut] + [cut]
        dp[length] = max_profit
        cuts[length] = best_cut

    return {
        "max_profit": max_profit,
        "cuts": best_cut,
        "number_of_cuts": len(cuts[length]) - 1,
    }


def run_tests():
    """Функція для запуску всіх тестів"""
    test_cases = [
        # Тест 1: Базовий випадок
        {"length": 5, "prices": [2, 5, 7, 8, 10], "name": "Базовий випадок"},
        # Тест 2: Оптимально не різати
        {"length": 3, "prices": [1, 3, 8], "name": "Оптимально не різати"},
        # Тест 3: Всі розрізи по 1
        {"length": 4, "prices": [3, 5, 6, 7], "name": "Рівномірні розрізи"},
    ]

    for test in test_cases:
        print(f"\nТест: {test['name']}")
        print(f"Довжина стрижня: {test['length']}")
        print(f"Ціни: {test['prices']}")

        # Тестуємо мемоізацію
        memo_result = rod_cutting_memo(test["length"], test["prices"])
        print("\nРезультат мемоізації:")
        print(f"Максимальний прибуток: {memo_result['max_profit']}")
        print(f"Розрізи: {memo_result['cuts']}")
        print(f"Кількість розрізів: {memo_result['number_of_cuts']}")

        # Тестуємо табуляцію
        table_result = rod_cutting_table(test["length"], test["prices"])
        print("\nРезультат табуляції:")
        print(f"Максимальний прибуток: {table_result['max_profit']}")
        print(f"Розрізи: {table_result['cuts']}")
        print(f"Кількість розрізів: {table_result['number_of_cuts']}")

        print("\nПеревірка пройшла успішно!")


if __name__ == "__main__":
    run_tests()
