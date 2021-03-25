from tensorflow import keras
from keras import models
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
import numpy as np
import random

class PoemGenerator:
    def __init__(self, seed_text, data, model):
        self.seed_text        = seed_text
        self.data             = data
        self.model            = models.load_model(model, compile=False)
        self.tokenizer        = Tokenizer()
        self.max_sequence_len = []

        corpus = data.lower().split("\n")
        self.tokenizer.fit_on_texts(corpus)
        # total_words = len(PoemGenerator.tokenizer.word_index) + 1

        input_sequences = []
        for line in corpus:
	        token_list = self.tokenizer.texts_to_sequences([line])[0]
	        for i in range(1, len(token_list)):
		        n_gram_sequence = token_list[:i+1]
		        input_sequences.append(n_gram_sequence)

        # pad sequences 
        self.max_sequence_len = max([len(x) for x in input_sequences])

    def generate_poem(self):
        next_words = 100
        for _ in range(next_words):
            token_list  = self.tokenizer.texts_to_sequences([self.seed_text])[0]
            token_list  = pad_sequences([token_list], maxlen=self.max_sequence_len-1, padding='pre')
            predicted   = self.model.predict_classes(token_list, verbose=0)
            output_word = ""
            for word, index in self.tokenizer.word_index.items():
                if index == predicted:
                    output_word = word
                    break
            self.seed_text += " " + output_word
        
        return self.strToPoem(self.seed_text)

    def remove_useless_stuff(self, str):
        return str.replace(' -','').replace(' \'', '')

    def remove_adjacent_dups(self, str):
        strArr1 = []
        strArr2 = str.split()

        strArr1.append(strArr2[0])
        for word in strArr2:
            if word == strArr1[-1]:
                continue
            else:
                strArr1.append(word)
        return strArr1

    def clean(self, str):
        str = self.remove_useless_stuff(str)
        return self.remove_adjacent_dups(str)

    def strToPoem(self, str):
        poemArr      = self.clean(str)
        poemArrFinal = []
        max_index    = len(poemArr)

        start_index = end_index = 0
        while end_index <= max_index:
            end_index   = start_index + random.randint(5, 8)
            arr = poemArr[start_index:end_index]
            poemArrFinal.append(' '.join(arr))
            start_index = end_index
        
        while len(poemArrFinal[-1].split()) < 5:
            del poemArrFinal[-1]

        # remove small words as the last word
        str = poemArrFinal[-1]
        strArr = str.split()
        while len(strArr[-1]) < 4:
            del strArr[-1]
        poemArrFinal[-1] = ' '.join(strArr)

        return poemArrFinal