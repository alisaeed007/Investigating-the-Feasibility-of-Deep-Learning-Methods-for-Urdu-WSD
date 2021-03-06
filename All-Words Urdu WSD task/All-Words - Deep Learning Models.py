# -*- coding: utf-8 -*-
"""Pretrained_Word2Vec_Samar_vectors_keras_Embeddings.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1cdSPByQZ9JKqN5HVCqpyKXTk6Lz8V5rl
"""

from keras.models import Sequential
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from keras.models import Model
from keras.layers import LSTM, Activation, Dense, Dropout, Input, Embedding, SimpleRNN, GRU, Bidirectional
from keras.optimizers import RMSprop
from keras.preprocessing.text import Tokenizer
from keras.preprocessing import sequence
from keras.utils import to_categorical
from keras.callbacks import EarlyStopping

from numpy import array
from numpy import asarray

from sklearn.metrics import classification_report
from sklearn.metrics import precision_recall_fscore_support

from gensim.models import word2vec

from google.colab import drive
drive.mount('/content/drive')

result_file_path = "/content/drive/My Drive/RNN/Result_Pretrained_Samar_Word2vec.txt"
vector_model_path = "/content/drive/My Drive/RNN/samar_urduvec_140M_100K_300d.txt"
df = pd.read_csv('/content/drive/My Drive/RNN/ALL_WORDS.csv',delimiter=',',encoding='latin-1') #MFarhat Path change

"""Follwing code is for Model Development by Ali Saeed"""

max_words = 10000
max_len = 300

sns.countplot(df.v1)
X = df.v2
Y = df.v1
X_train,X_test,Y_train,Y_test = train_test_split(X,Y,test_size=0.33)

max_words = 10000
max_len = 300

tok = Tokenizer(num_words=max_words)
tok.fit_on_texts(X_train)
#MFarhat 
vocab_size = len(tok.word_index) +1
#MFarhat

sequences = tok.texts_to_sequences(X_train)
sequences_matrix = sequence.pad_sequences(sequences,maxlen=max_len, padding='post')
print(sequences_matrix)

# load the whole embedding into memory
embeddings_index = dict()
f = open(vector_model_path,"r")
for line in f:
    values = line.split()
    word = values[0]
    coefs = asarray(values[1:], dtype='float32')
    embeddings_index[word] = coefs
f.close()
print('Loaded %s word vectors.' % len(embeddings_index))
# create a weight matrix for words in training docs

embedding_matrix = np.zeros((vocab_size, 300)) # Embedding Size
for word, i in tok.word_index.items():
	embedding_vector = embeddings_index.get(word)
	if embedding_vector is not None:
		embedding_matrix[i] = embedding_vector

model = Sequential()
model.add(Embedding(vocab_size, 300, weights=[embedding_matrix], input_length=300, trainable=False)) #Embedding Size

model.add(SimpleRNN(100, return_sequences=True))
model.add(SimpleRNN(100, return_sequences=False)) # Use LSTM | SimpleRNN | GRU to chane the method 
#model.add(Bidirectional(LSTM(100, return_sequences=False))) # Uncomment this line to use Bidirectional LSTM
model.add(Dropout(0.2)) # Use this line to increase or decrease the dropout
model.add(Dense(8, activation='softmax'))

model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

model.fit(sequences_matrix, Y_train, validation_split=0.2, epochs=5, batch_size=32)

test_sequences = tok.texts_to_sequences(X_test)
test_sequences_matrix = sequence.pad_sequences(test_sequences,maxlen=max_len)
score = model.evaluate(test_sequences_matrix, Y_test, batch_size=32)

Y_Pred = model.predict(test_sequences_matrix)
Y_Pred=np.argmax(Y_Pred,axis=1)

R=str((precision_recall_fscore_support(Y_test.values, Y_Pred, average='weighted')))
file = open(result_file_path,"w")
print("Accuracy: %.2f%%" % (score[1]*100))
Accu_score = round(score[1]*100,2)
file.writelines("Simple RNN: \nAccuracy Score = "+str(Accu_score))

#########
data = R.split(",")
#print ("Precision " + str(data[0][1:]))
#Preci = round(float(data[0][1:]),2)
#file.writelines("\nPrecision Score = "+str(Preci))

#print ("Recall " + str(data[1]))
#recall = round(float(data[1]),2)
#file.writelines("\nRecall Score = "+str(recall))

print ("F1-measure " + str(data[2]))
#f1_measure = round(float(data[2]),2)
#file.writelines("\nF1_measure Score = "+str(f1_measure))
#file.close()
## https://machinelearningmastery.com/use-word-embedding-layers-deep-learning-keras/

