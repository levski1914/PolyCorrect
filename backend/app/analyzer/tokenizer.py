import re

def simple_tokenizer(text):
    """
    Разделя текста на думи и препинателни знаци.
    Пример: "Той пише, а тя чете." -> ['Той', 'пише', ',', 'а', 'тя', 'чете', '.']
    """
    return re.findall(r'\w+|[^\w\s]', text, re.UNICODE)

def detokenize(tokens):
    """
    Възстановява текст от списък с токени, като поддържа правилна пунктуация и разстояния.
    Пример: ['Той', 'пише', ',', 'а', 'тя', 'чете', '.'] -> "Той пише, а тя чете."
    """
    result = ""
    for i, token in enumerate(tokens):
        if i > 0:
            # Добави интервал преди дума, ако предишният токен не е препинателен знак
            if re.match(r'\w', token) and re.match(r'\w', tokens[i - 1]):
                result += " "
            elif token in ['(', '[', '{']:  # скоби - няма интервал
                result += " "
            elif token not in [",", ".", "!", "?", ":", ";"]:
                result += " "
        result += token
    return result
