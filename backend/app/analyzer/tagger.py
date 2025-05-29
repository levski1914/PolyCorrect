import os
import json
import re
from app.analyzer.spellcheck import suggest_similar_words

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
adj_path = os.path.join(BASE_DIR, "../lexicons/adj_lexicon.json")
noun_path = os.path.join(BASE_DIR, "../lexicons/noun_lexicon.json")

with open(adj_path, "r", encoding="utf-8") as f:
    adj_lexicon = json.load(f)

with open(noun_path, "r", encoding="utf-8") as f:
    noun_lexicon = json.load(f)
pron_path = os.path.join(BASE_DIR, "../lexicons/pron_lexicon.json")
verb_path = os.path.join(BASE_DIR, "../lexicons/verb_lexicon.json")

with open(pron_path, "r", encoding="utf-8") as f:
    pron_lexicon = json.load(f)

with open(verb_path, "r", encoding="utf-8") as f:
    verb_lexicon = json.load(f)



def tag_tokens(tokens):
    tagged = []
    for token in tokens:
        word = token.lower()

        if word in adj_lexicon:
            entry = adj_lexicon[word]
            tagged.append({
                "text": token,
                "pos": entry["pos"],
                "gender": entry["gender"],
                "number": entry["number"],
                "forms": entry.get("forms", {}),
                "base": word
            })
        elif word in pron_lexicon:
            entry = pron_lexicon[word]
            tagged.append({
                "text": token,
                "pos": entry["pos"],
                "person": entry["person"],
                "number": entry["number"]
            })
        elif word in verb_lexicon:
            entry = verb_lexicon[word]
            tagged.append({
                "text": token,
                "pos": entry["pos"],
                "person": entry["person"],
                "number": entry["number"],
                "base": entry["base"]
            })
        elif word in noun_lexicon:
            entry = noun_lexicon[word]
            tagged.append({
                "text": token,
                "pos": entry["pos"],
                "gender": entry["gender"],
                "number": entry["number"],
                "base": word
            })
        else:
            # Форми на прилагателни
            found = False
            for base, entry in adj_lexicon.items():
                forms = entry.get("forms", {})
                for form_gender, form in forms.items():
                    if word == form:
                        tagged.append({
                            "text": token,
                            "pos": entry["pos"],
                            "gender": form_gender,
                            "number": entry["number"],
                            "forms": forms,
                            "base": base
                        })
                        found = True
                        break
                if found:
                    break

            # Членувани съществителни
            if not found:
                noun_suffixes = ["ът", "ят", "та", "то", "те"]
                for suffix in noun_suffixes:
                    if word.endswith(suffix):
                        base_candidate = word[:-len(suffix)]
                        if base_candidate in noun_lexicon:
                            entry = noun_lexicon[base_candidate]
                            tagged.append({
                                "text": token,
                                "pos": entry["pos"],
                                "gender": entry["gender"],
                                "number": entry["number"],
                                "base": base_candidate
                            })
                            found = True
                            break

            # Спелчек
            if not found:
                # Опитай първо със съществителни (ако дума завършва на -ът, -та и т.н.)
                if re.search(r'(ът|та|то|те|ят)$', word):
                    suggestions = suggest_similar_words(word, list(noun_lexicon.keys()))
                else:
                    combined_vocab = (
                        list(noun_lexicon.keys()) +
                        list(adj_lexicon.keys()) +
                        list(verb_lexicon.keys())
                    )
                    
                suggestions = suggest_similar_words(word, combined_vocab)

         

                tagged.append({
                    "text": token,
                    "pos": "UNK", 
                    "suggestions": suggestions
                })

    return tagged
