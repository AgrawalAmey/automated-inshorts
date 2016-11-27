from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Sumy
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
from pymongo import MongoClient
from garbage import *
import re

class Summarizer(object):
	def __init__(self):
		client = MongoClient('mongodb://localhost:27017/')
		db = client['inshort']
		self.stories = db['stories']

		self.language = "english"
		self.sentences_count = 5
		self.stemmer = Stemmer(self.language)
		self.tokenizer = Tokenizer(self.language)
		self.summarizer = Sumy(self.stemmer)
		self.summarizer.stop_words = get_stop_words(self.language)

	def summerize(self):
		for story in self.stories.find({"is_scraped": True, "is_ready": False}):
			story["content"].replace(garbage, '')
			self.parser = PlaintextParser.from_string(story["content"], self.tokenizer)
			sentences = self.summarizer(self.parser.document, self.sentences_count)
			sentences = [x._text for x in sentences]
			if len(sentences) != 0:
				content = ". ".join(sentences)
				self.stories.update({"_id": story["_id"]}, {"$set": {"short": content, "is_ready" : True}})
