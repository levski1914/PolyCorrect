import stanza

stanza.download('bg')
nlp = stanza.Pipeline('bg')

def get_feat(feats_str: str, key: str) -> str | None:
    if not feats_str:
        return None
    parts = feats_str.split('|')
    for part in parts:
        if part.startswith(key + '='):
            return part.split('=')[1]
    return None

def check_adj_noun_agreement(sentence) -> list[dict]:
    issues = []
    words = sentence.words
    word_by_id = {word.id: word for word in words}

    for word in words:
        if word.pos == "ADJ" and word.head in word_by_id:
            noun = word_by_id[word.head]
            if noun.pos == "NOUN" and noun.feats and word.feats:
                adj_gender = get_feat(word.feats, "Gender")
                noun_gender = get_feat(noun.feats, "Gender")
                adj_number = get_feat(word.feats, "Number")
                noun_number = get_feat(noun.feats, "Number")

                if adj_gender and noun_gender and adj_gender != noun_gender:
                    issues.append({
                        "type": "Gender disagreement",
                        "adj": word.text,
                        "noun": noun.text,
                        "adj_gender": adj_gender,
                        "noun_gender": noun_gender
                    })

                if adj_number and noun_number and adj_number != noun_number:
                    issues.append({
                        "type": "Number disagreement",
                        "adj": word.text,
                        "noun": noun.text,
                        "adj_number": adj_number,
                        "noun_number": noun_number
                    })

    return issues

def analyze_text(text: str) -> list[dict]:
    doc = nlp(text)
    all_issues = []
    for sentence in doc.sentences:
        all_issues.extend(check_adj_noun_agreement(sentence))
    return all_issues
