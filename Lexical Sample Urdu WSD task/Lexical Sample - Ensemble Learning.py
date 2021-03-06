# -*- coding: utf-8 -*-
"""LS_Ensemble.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1aXKYKDShwpYk8DEzvj4R0GB7LCe-eDPj
"""

from numpy import array
from numpy import asarray
from sklearn.metrics import classification_report
from sklearn.metrics import precision_recall_fscore_support
from keras.models import Sequential
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from keras.models import Model
from keras.layers import LSTM, Activation, Dense, Dropout, Input, Embedding,GRU
from keras.optimizers import RMSprop
from keras.preprocessing.text import Tokenizer
from keras.preprocessing import sequence
from keras.utils import to_categorical
from keras.callbacks import EarlyStopping
from keras.layers import Bidirectional
from keras.layers import SimpleRNN
from sklearn.metrics import classification_report
from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import classification_report
from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import accuracy_score

from google.colab import drive
drive.mount('/content/drive')

result_file_path = "/content/drive/My Drive/RNN/Result_LS_LSTM.txt"
vector_model_path = "/content/drive/My Drive/RNN/samar_urduvec_140M_100K_300d.txt"

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


def average_list(lst):
    return round(sum(lst)/len(lst),2)
##### 1.  Simple RNN  ##########

counter = 1
Accu_list = []
Pre_list = []
Recall_list = []
F1_measure_list = []
while counter <=50:
    print("Working on Word no: "+str(counter))
    df = pd.read_csv('/content/drive/My Drive/RNN/LS_Data/CSV_Auto_Train/'+str(counter)+'.csv',delimiter=',',encoding='latin-1')
                        
    df1 = pd.read_csv('/content/drive/My Drive/RNN/LS_Data/CSV_Auto_Test/'+str(counter)+'.csv',delimiter=',',encoding='latin-1')

    sns.countplot(df.v1)
    sns.countplot(df1.v1)

    X = df.v2
    Y = df.v1
    X_train,X_test,Y_train,Y_test = train_test_split(X,Y,test_size=0.01)

    X1 = df1.v2
    Y1 = df1.v1
    X1_train,X1_test,Y1_train,Y1_test = train_test_split(X1,Y1,test_size=0.95)
    max_words = 2000
    max_len = 200

    tok = Tokenizer(num_words=max_words)
    tok.fit_on_texts(X_train)
    vocab_size = len(tok.word_index) +1
    sequences = tok.texts_to_sequences(X_train)
    sequences_matrix = sequence.pad_sequences(sequences,maxlen=max_len, padding='post')

    # create a weight matrix for words in training docs

    embedding_matrix = np.zeros((vocab_size, 300))
    for word, i in tok.word_index.items():
        embedding_vector = embeddings_index.get(word)
        if embedding_vector is not None:
            embedding_matrix[i] = embedding_vector
    
    ######################### Model 1 ##########################
    model = Sequential()
    model.add(Embedding(vocab_size, 300, weights=[embedding_matrix], input_length=300, trainable=False))
    model.add(LSTM(100, return_sequences=True))
    model.add(LSTM(100, return_sequences=True))
    model.add(LSTM(100, return_sequences=False))
    model.add(Dropout(0.2))
    no_of_classes=max(Y_train)+1
    model.add(Dense(int(no_of_classes), activation='softmax'))
    model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    model.fit(sequences_matrix, Y_train, validation_split=0.2, epochs=20, batch_size=32)
    test_sequences = tok.texts_to_sequences(X1_test)
    test_sequences_matrix = sequence.pad_sequences(test_sequences,maxlen=max_len)
    score = model.evaluate(test_sequences_matrix, Y1_test, batch_size=32)
    Y_Pred_Model1 = model.predict(test_sequences_matrix)
    Y_Pred_Model1=np.argmax(Y_Pred_Model1,axis=1)
    
    ######################### Model 2 #########################

   # create a weight matrix for words in training docs

    embedding_matrix = np.zeros((vocab_size, 500))
    for word, i in tok.word_index.items():
        embedding_vector = embeddings_index.get(word)
        if embedding_vector is not None:
            embedding_matrix[i] = embedding_vector
    

    model = Sequential()
    model.add(Embedding(vocab_size, 500, weights=[embedding_matrix], input_length=500, trainable=False))
    model.add(LSTM(100, return_sequences=True))
    model.add(LSTM(100, return_sequences=True))
    model.add(LSTM(100, return_sequences=False))
    model.add(Dropout(0.2))
    no_of_classes=max(Y_train)+1

    model.add(Dense(int(no_of_classes), activation='softmax'))
    model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    model.fit(sequences_matrix, Y_train, validation_split=0.2, epochs=20, batch_size=32)

    test_sequences = tok.texts_to_sequences(X1_test)
    test_sequences_matrix = sequence.pad_sequences(test_sequences,maxlen=max_len)
    score = model.evaluate(test_sequences_matrix, Y1_test, batch_size=32)
    Y_Pred_Model2 = model.predict(test_sequences_matrix)
    Y_Pred_Model2=np.argmax(Y_Pred_Model2,axis=1)
    
    ######################### Model 3 #########################
    embedding_matrix = np.zeros((vocab_size, 5000))
    for word, i in tok.word_index.items():
        embedding_vector = embeddings_index.get(word)
        if embedding_vector is not None:
            embedding_matrix[i] = embedding_vector

    model = Sequential()
    model.add(Embedding(vocab_size, 5000, weights=[embedding_matrix], input_length=5000, trainable=False))
    model.add(SimpleRNN(100, return_sequences=True))
    model.add(SimpleRNN(100, return_sequences=True))
    model.add(SimpleRNN(100, return_sequences=True))
    model.add(SimpleRNN(100, return_sequences=True))
    model.add(SimpleRNN(100, return_sequences=True))
    model.add(SimpleRNN(100, return_sequences=True))
    model.add(SimpleRNN(100, return_sequences=True))
    model.add(SimpleRNN(100, return_sequences=True))
    model.add(SimpleRNN(100, return_sequences=True))
    model.add(SimpleRNN(100, return_sequences=False))
    model.add(Dropout(0.2))
    no_of_classes=max(Y_train)+1

    model.add(Dense(int(no_of_classes), activation='softmax'))
    model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    model.fit(sequences_matrix, Y_train, validation_split=0.2, epochs=20, batch_size=32)

    test_sequences = tok.texts_to_sequences(X1_test)
    test_sequences_matrix = sequence.pad_sequences(test_sequences,maxlen=max_len)
    score = model.evaluate(test_sequences_matrix, Y1_test, batch_size=32)

    Y_Pred_Model3 = model.predict(test_sequences_matrix)
    Y_Pred_Model3=np.argmax(Y_Pred_Model3,axis=1)
    
    ######################### End Model3 #########################
    length=len(Y_Pred_Model1)
    i = 0
    while i < length:
      List=[Y_Pred_Model1[i], Y_Pred_Model2[i], Y_Pred_Model3[i]]
      most_frequent_sense= max(set(List), key = List.count)
      Y_Pred_Model1[i]= most_frequent_sense
      i += 1
      
    R=str((precision_recall_fscore_support(Y1_test.values, Y_Pred_Model1, average='weighted')))

    file.write(str(accuracy_score(Y1_test.values,Y_Pred_Model1)))
    data = R.split(",")
    
    #file.write(R[1:]) 
    #file.write(data[0][1:])# Write Precision on file
    #file.write("+")
    #file.write(data[1]) # Write Recall on file
    #file.write("+")
    file.write(data[2]) # Write F_Measure on file
    counter=counter+1
    file.write("\n")