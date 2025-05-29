import re
from app.analyzer.tagger import adj_lexicon, verb_lexicon, noun_lexicon

def check_conjunction_vs_pronoun(tagged_tokens):
    issues = []
    for i in range(len(tagged_tokens) - 1):
        current = tagged_tokens[i]
        next_token = tagged_tokens[i + 1]
        if current["text"].lower() == "ѝ":
            if next_token["pos"] in ["VERB", "ADJ", "ADV"]:
                suggestion = [t["text"] for t in tagged_tokens]
                suggestion[i] = "и"
                issues.append({
                    "type": "Conjunction vs Pronoun",
                    "word": "ѝ",
                    "issue": "Misused 'ѝ' instead of 'и'",
                    "suggestion": " ".join(suggestion)
                })
    return issues


def check_determiners(tagged_tokens):
    issues = []
    definite_suffixes = ["ът", "ят", "та", "то", "те"]

    for token in tagged_tokens:
        word = token["text"].lower()
        for s1 in definite_suffixes:
            for s2 in definite_suffixes:
                if word.endswith(s1 + s2):
                    suggestion = word[:-len(s2)]
                    issues.append({
                        "type": "Definite article error",
                        "word": token["text"],
                        "issue": "Double definite article",
                        "suggestion": suggestion
                    })
                    break
            else:
                continue
            break
    return issues


def check_spelling(tagged_tokens):
    issues = []
    for token in tagged_tokens:
        if token["pos"] == "UNK":
            suggestions = token.get("suggestions", [])
            if suggestions:
                issues.append({
                    "type": "Spelling error",
                    "word": token["text"],
                    "suggestions": suggestions
                })
    return issues


def check_adj_noun_gender_agreement(tagged_tokens):
    issues = []
    for i in range(len(tagged_tokens) - 1):
        t1 = tagged_tokens[i]
        t2 = tagged_tokens[i + 1]
        if t1["pos"] == "ADJ" and t2["pos"] == "NOUN":
            if t1["gender"] != t2["gender"]:
                base = t1.get("base", t1["text"].lower())
                forms = adj_lexicon.get(base, {}).get("forms", {})
                correct_adj = forms.get(t2["gender"])
                if correct_adj:
                    suggestion_tokens = [t["text"] for t in tagged_tokens]
                    suggestion_tokens[i] = correct_adj
                    issues.append({
                        "type": "Gender disagreement",
                        "adj": t1["text"],
                        "noun": t2["text"],
                        "adj_gender": t1["gender"],
                        "noun_gender": t2["gender"],
                        "suggestion": " ".join(suggestion_tokens)
                    })
    return issues


def check_subject_verb_agreement(tagged_tokens):
    issues = []

    for i in range(len(tagged_tokens) - 1):
        subj = tagged_tokens[i]
        verb = tagged_tokens[i + 1]

        if verb["pos"] != "VERB":
            continue
        if subj["pos"] not in ["PRON", "NOUN"]:
            continue
        if "person" not in verb or "number" not in verb:
            continue

        subj_person = subj.get("person", 3)
        subj_number = subj.get("number")

        # Координиран подлог (X и Y → Plur)
        if i >= 2:
            prev1 = tagged_tokens[i - 1]
            prev2 = tagged_tokens[i - 2]
            if prev1["text"].lower() == "и" and prev2["pos"] in ["PRON", "NOUN"]:
                subj_number = "Plur"
                subj_person = 3

        if subj_number is None:
            continue

        if subj_person != verb["person"] or subj_number != verb["number"]:
            base = verb.get("base", verb["text"].lower())
            correct_verb = None

            for form, entry in verb_lexicon.items():
                if entry["base"] == base and entry["person"] == subj_person and entry["number"] == subj_number:
                    correct_verb = form
                    break

            if correct_verb:
                suggestion_tokens = [t["text"] for t in tagged_tokens]
                suggestion_tokens[i + 1] = correct_verb
                issues.append({
                    "type": "Subject-Verb disagreement",
                    "subject": subj["text"],
                    "verb": verb["text"],
                    "subject_person": subj_person,
                    "subject_number": subj_number,
                    "verb_person": verb["person"],
                    "verb_number": verb["number"],
                    "suggestion": " ".join(suggestion_tokens)
                })

    return issues
