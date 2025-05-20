from functools import lru_cache

@lru_cache(maxsize=64)
def get_score_change(dice_value: int) -> int:
    if dice_value in (1, 22, 43):
        return 7
    elif dice_value in (16, 32, 48):
        return 5
    elif dice_value == 64:
        return 300
    else:
        return -30

def get_combo_parts(dice_value: int):
    values = ["BAR", "🍇", "🍋", "7️⃣"]
    dice_value -= 1
    return [values[dice_value % 4], values[(dice_value // 4) % 4], values[(dice_value // 16) % 4]]
