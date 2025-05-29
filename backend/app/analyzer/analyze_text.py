from collections import defaultdict
from app.analyzer.tokenizer import simple_tokenizer
from app.analyzer.tagger import tag_tokens, noun_lexicon
from app.analyzer.rule_checker import (
    check_spelling,
    check_adj_noun_gender_agreement,
    check_subject_verb_agreement,
    check_determiners,
    check_conjunction_vs_pronoun
)
from app.analyzer.tokenizer import detokenize
def correct_spelling_errors(tagged):
    corrected = []
    for token in tagged:
        if token["pos"] == "UNK" and token.get("suggestions"):
            # Използвай първото предложение само ако съществува в лексиконите
            suggestion = None
            for word in token["suggestions"]:
                if word in noun_lexicon:
                    suggestion = word
                    break
            corrected.append({"text": suggestion if suggestion else token["text"]})
        else:
            corrected.append({"text": token["text"]})
    return corrected

def analyze_text(text):
    tokens = simple_tokenizer(text)
    tagged = tag_tokens(tokens)

    issues = []
    spelling_issues = check_spelling(tagged)
    issues += spelling_issues

    corrected_tokens = correct_spelling_errors(tagged)
    corrected_words = [t["text"] for t in corrected_tokens]
    corrected_tagged = tag_tokens(corrected_words)

    # Съставни подлози → множествено число
    for i in range(2, len(corrected_tagged)):
        t0, t1, t2 = corrected_tagged[i - 2], corrected_tagged[i - 1], corrected_tagged[i]
        if t1["text"].lower() == "и" and t0["pos"] in ["NOUN", "PRON"] and t2["pos"] in ["NOUN", "PRON"]:
            t0["number"] = t2["number"] = "Plur"

    grammar_issues = (
        check_adj_noun_gender_agreement(corrected_tagged) +
        check_subject_verb_agreement(corrected_tagged) +
        check_determiners(corrected_tagged) +
        check_conjunction_vs_pronoun(corrected_tagged)
    )
    issues += grammar_issues

    # Събиране на предложения за корекции
    replacement_votes = defaultdict(list)
    for issue in issues:
        if "suggestion" in issue and issue["suggestion"]:
            suggestion_words = issue["suggestion"].split()
            if len(suggestion_words) == len(corrected_words):
                for i in range(len(corrected_words)):
                    if corrected_words[i].lower() != suggestion_words[i].lower():
                        replacement_votes[i].append(suggestion_words[i])

    final_words = corrected_words.copy()
    for i, variants in replacement_votes.items():
        if variants:
            most_common = max(set(variants), key=variants.count)
            final_words[i] = most_common

    # Възстановяване на главни букви
    for i in range(len(final_words)):
        if corrected_words[i][0].isupper():
            final_words[i] = final_words[i].capitalize()

    corrected_text = detokenize(final_words)
    return {
        "issues": issues,
        "corrected_text": corrected_text
    }
