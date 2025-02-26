

async def result_anx_dep(total_anx, total_dep, lang):
    answer = ''
    if lang == 'ru-RU':
        answer += f"Финальный результат по шкале тревожности: {total_anx}\n Статус тревожности: {await anx_result(total_anx, 'ru-RU')}\nФинальный результат по шкале депрессии: {total_dep}\n Статус депрессии: {await dep_result(total_dep, 'ru-RU')}\n"
    else:
        answer += f"Final result on the anxiety scale: {total_anx}\n Anxiety status: {await anx_result(total_anx, 'en-Us')}\nFinal result on the depression scale: {total_dep}\n Depression status: {await dep_result(total_dep, 'en-Us')}\n"
    return answer

async def anx_result(total_anx, lang):
    if lang == 'ru-RU':
        if total_anx > 15: return "Сильное беспокойство"
        if total_anx >= 10: return "Умеренное беспокойство"
        if total_anx >= 5: return "Легкое беспокойство"
        return "Минимальная тревожность"
    else:
        if total_anx > 15: return "Severe Anxiety"
        if total_anx >= 10: return "Moderate Anxiety"
        if total_anx >= 5: return "Mild Anxiety"
        return "Minimal Anxiety"

async def dep_result(total_dep, lang):
    if lang == 'ru-RU':
        if total_dep >= 20: return "Тяжелая депрессии"
        if total_dep >= 15: return "Умеренно тяжелая депрессии"
        if total_dep >= 10: return "Умеренная депрессии"
        if total_dep >= 5: return "Легкая депрессии"
        return "Минимальная депрессии"
    else:
        if total_dep >= 20: return "Severe depression"
        if total_dep >= 15: return "Moderately severe depression"
        if total_dep >= 10: return "Moderate depression"
        if total_dep >= 5: return "Mild depression"
        return "Minimal depression"