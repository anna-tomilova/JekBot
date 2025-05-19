
from functools import lru_cache
from typing import List

@lru_cache(maxsize=64)
def get_score_change(dice_value: int) -> int:
    """
    Проверка выигрышной комбинации

    :param dice_value: значение Telegram-слота (1-64)
    :return: изменение счета пользователя
    """
    if dice_value in (1, 22, 43):
        return 7  # Three of a kind
    elif dice_value in (16, 32, 48):
        return 5  # Two 7s
    elif dice_value == 64:
        return 10  # Jackpot (777)
    else:
        return -1  # Проигрыш

def get_combo_parts(dice_value: int) -> List[str]:
    """
    Возвращает список значков (bar, grapes, lemon, seven)

    :param dice_value: значение Telegram-слота (1-64)
    :return: список значков в виде строк
    """
    values = ["bar", "grapes", "lemon", "seven"]
    dice_value -= 1
    result = []
    for _ in range(3):
        result.append(values[dice_value % 4])
        dice_value //= 4
    return result
