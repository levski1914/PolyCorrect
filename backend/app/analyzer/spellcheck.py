import difflib

def suggest_similar_words(word, vocabulary, cutoff=0.7, max_suggestions=5):
    suggestions = difflib.get_close_matches(word, vocabulary, n=max_suggestions, cutoff=cutoff)
    if not suggestions and len(word) > 5:
        # опитваме с по-нисък праг
        suggestions = difflib.get_close_matches(word, vocabulary, n=max_suggestions, cutoff=0.5)
    return suggestions

