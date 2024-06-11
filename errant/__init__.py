from importlib import import_module
import json
import stanza
from errant.annotator import Annotator

# ERRANT version
__version__ = '3.0.0'

# Load an ERRANT Annotator object for a given language
def load(lang, nlp=None, legacy=False):
    # Make sure the language is supported
    if legacy:
        supported = {"en"}
        if lang not in supported:
            raise ValueError(f"{lang} is an unsupported or unknown language")

        # Load Stanza pipeline
        nlp = nlp or stanza.Pipeline(lang, tokenize_pretokenized=True)
        
        # Load language edit merger
        merger = import_module(f"errant.{lang}.merger")

        # Load language edit classifier
        classifier = import_module(f"errant.{lang}.classifier")
        classifier.nlp = nlp
    else:
        with open("errant/stanza_resources_1.7.0.json", mode='r', encoding='utf-8') as f:
            stanza_supported = json.load(f).keys()
        
        if lang not in stanza_supported:
            raise ValueError(f"{lang} is an unsupported or unknown language")
        
        nlp = nlp or stanza.Pipeline(lang)
        merger = import_module(f"errant.multi.merger")
        classifier = import_module(f"errant.multi.classifier")
        classifier.nlp = nlp

    # Return a configured ERRANT annotator
    return Annotator(lang, nlp, merger, classifier)