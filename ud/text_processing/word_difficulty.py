"""Word diffilcuty class basis on
https://github.com/dusking/medium_src/blob/main/src/a01_word_difficulty.py
"""


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
from utils import with_pickle

nlp = spacy.load("pl_core_news_md", disable=["ner", "parser"])
STOPWORDS_PL = stopwords("pl")
STOPWORDS_EN = stopwords("en")

polish_chars = re.compile(r"[a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ+]+")
polish_small_chars = re.compile(r"[^a-ząćęłńóśźż\s]")

def extract_tokens_from_doc(doc):
    return [
        token.lemma_.lower()
        for token in doc
        if token.is_alpha and len(token.lemma_) > 2 and token.lemma_.lower() not in STOPWORDS_PL
    ]

# def extract_tokens(text: str):
#     doc = nlp(clean)
#     return [
#         token.lemma_.lower() 
#         for token in doc 
#         if token.is_alpha and len(token.lemma_) > 2 and token.lemma_.lower() not in STOPWORDS_PL
#     ]

def build_freqdist_batch(documents, batch_size=50, n_process=4):
    """
    Build a NLTK FreqDist from a list (or generator) of raw texts using batch processing.
    
    Parameters:
        documents: iterable of strings
        batch_size: number of documents per batch
        n_process: number of processes (CPU cores) to use
        
    Returns:
        FreqDist object
    """
    fdist = FreqDist()
    cleaned_docs = (polish_chars.sub(" ", doc) for doc in documents)
    for doc in nlp.pipe(cleaned_docs, batch_size=batch_size, n_process=n_process):
        tokens = extract_tokens_from_doc(doc)
        fdist.update(tokens)
    return fdist

@with_pickle(default_pickle_path="data/pl_wiki_tokens.pkl")
def get_pl_wiki_tokens():
    words: list[str] = []
    for doc in read_pl_wiki_corpus():
        tokens = tokenize(doc)
        words.extend(tokens)
    return words

import math

@with_pickle(default_pickle_path="data/pl_wiki_freqs.pkl")
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


# def build_freqdist(morph=False):
#     return build_freqdist_batch(read_pl_wiki_corpus(), batch_size=100, n_process=4)

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

class PolishWordDifficulty:
    def __init__(self, corpus_texts=None):
        self.stopwords = stopwords("pl")
        wn.download("plwordnet")
        self.wordnet = wn.Wordnet("plwordnet")
        self.wordnet_words = set()
        for synset in self.wordnet.synsets():
            for lemma in synset.lemmas():
                self.wordnet_words.add(lemma.lower())

        self.morf = morfeusz2.Morfeusz()

        if corpus_texts:
            tokens = []
            for txt in corpus_texts:
                tokens.extend(self._tokenize(txt))
            self.freq = Counter(tokens)
        else:
            self.freq = Counter()

    def _tokenize(self, text):
        return re.findall(r"\b\w+\b", text.lower(), flags=re.UNICODE)

    def lemmatize(self, word):
        anal = self.morf.analyse(word)
        if not anal:
            return word.lower()
        # Morfeusz zwraca (orth, lemma, tag)
        return anal[0][2][1].lower()

    def word_frequency(self, word):
        lemma = self.lemmatize(word)
        return self.freq.get(lemma, 0)

    def difficulty_score(self, word: str):
        lemma = self.lemmatize(word)
        freq = self.word_frequency(lemma)

        score = 0
        if lemma not in self.wordnet_words:
            score += 1
        if lemma not in self.stopwords:
            score += 1
        if freq == 0:
            score += 1
        elif freq < 5:
            score += 0.5

        return score


# class PolishWordDifficulty:
#     def __init__(self, freqdist):
#         self.freq = freqdist
#         self.stopwords = set(nltk.corpus.stopwords.words('polish'))
#         # Load WordNet for PL if available via `wn` and lemmatizer (Morfeusz2 or spaCy)

#     def word_frequency(self, word):
#         lemma = self.lemmatize(word)
#         return self.freq[lemma]  # FreqDist supports dictionary-style access

#     def difficulty_score(self, word):
#         lemma = self.lemmatize(word)
#         score = 0
#         if lemma not in self.stopwords:
#             score += 1
#         freq = self.freq[lemma]
#         if freq == 0:
#             score += 1
#         elif freq < 5:
#             score += 0.5
#         return score

#     def lemmatize(self, word):
#         # Implement Morfeusz2 lemmatization or spaCy PL
#         return word.lower()

