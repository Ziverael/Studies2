import wn
import morfeusz2
from stopwordsiso import stopwords
from collections import Counter
import re
import nltk
from nltk.probability import FreqDist
import os
from tqdm import tqdm
import spacy
from utils import with_pickle, PATHS
import math

nlp = spacy.load("pl_core_news_md", disable=["ner", "parser"])
STOPWORDS_PL = stopwords("pl")
STOPWORDS_EN = stopwords("en")

polish_chars = re.compile(r"[a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ+]+")
polish_small_chars = re.compile(r"[^a-ząćęłńóśźż\s]")

@with_pickle(default_pickle_path= PATHS.pickles / "pl_wiki_freqs.pkl")
def build_freqdist():
    print("Tokenizaiton...")
    words = get_pl_wiki_tokens()
    print("Lemization...")
    lemmas = []
    batch_size = 10_000
    words_len = len(words)
    batches_no = math.ceil(words_len / batch_size)
    print(batches_no)
    for i in range(batches_no):
        words_doc = nlp(" ".join(words[batch_size*i:batch_size*(i+1)]))
        lemmas_batch = [
        token.lemma_
        for token in words_doc 
        if token.is_alpha and len(token.lemma_) > 2 and token.lemma_ not in STOPWORDS_PL
        ]
        lemmas.extend(lemmas_batch)
        print(len(lemmas_batch))
    return FreqDist(lemmas)

@with_pickle(default_pickle_path=PATHS.pickles / "pl_wiki_tokens.pkl")
def get_pl_wiki_tokens():
    words: list[str] = []
    for doc in read_pl_wiki_corpus():
        tokens = tokenize(doc)
        words.extend(tokens)
    return words

def read_pl_wiki_corpus():
    for root, _, files in tqdm(os.walk("plwiki3")):
        for fn in files:
            if fn.endswith(".txt"):
                path = os.path.join(root, fn)
                with open(path, "r", encoding="utf-8") as f:
                    yield f.read()

def tokenize(text: str):
    """Simple regex-based tokenizer for Polish text."""
    polish_small_text = polish_small_chars.sub(" ", text.lower())
    return re.findall(r"\b\w+\b", polish_small_text, flags=re.UNICODE)
