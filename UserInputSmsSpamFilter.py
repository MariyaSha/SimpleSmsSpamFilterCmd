import argparse
import numpy as np
import pandas as pd
import string
import nltk

#Collect User Input for Custom SMS
parser = argparse.ArgumentParser(description='Simple SMS Spam Detection Function, Categorizing a User Input Messege')
parser.add_argument('sms', metavar='', action='store', type=str, nargs='+', help='Type a custom sms to determine if it\'s spam or not')
args = parser.parse_args()

#functions
def categorize_words():
    '''
    Catagorizes each spam/non-spam word into a corresponding list
    Repeating words in each list will help with categorizing
    '''
    spam_words = []
    ham_words = []
    for sms in data['processed'][data['label'] == 'spam']:
        for word in sms:
            spam_words.append(word)
    for sms in data['processed'][data['label'] == 'ham']:
        for word in sms:
            ham_words.append(word)
    return spam_words, ham_words

def predict(sms):
    '''
    Determine whether the sms is spam or not by compairing the number
    of times each of the words appears in each of the categories
    '''
    spam_counter = 0
    ham_counter = 0
    for word in sms:
        spam_counter += spam_words.count(word)
        ham_counter += ham_words.count(word)
    print('---------------------------------------\n                RESULTS\n---------------------------------------')
    if ham_counter > spam_counter:
        accuracy = round((ham_counter / (ham_counter + spam_counter) * 100))
        print('messege is not spam, with {}% certainty'.format(accuracy))
    elif ham_counter == spam_counter:
        print('message could be spam')
    else:
        accuracy = round((spam_counter / (ham_counter + spam_counter) * 100))
        print('message is spam, with {}% certainty'.format(accuracy))

def pre_process(sms):
    '''
    Remove punctuation and stop words from the custom sms
    '''
    remove_punct = "".join([word.lower() for word in sms if word not in string.punctuation])
    tokenize = nltk.tokenize.word_tokenize(remove_punct)
    remove_stop_words = [word for word in tokenize if word not in nltk.corpus.stopwords.words('english')]
    return remove_stop_words

if __name__ == '__main__':

    #Loading SMS Spam Filter Dataset and Processing it to remove punctuation and stopwords
    data = pd.read_csv('SMSSpamCollection.txt', sep = '\t', header=None, names=["label", "sms"])
    data['processed'] = data['sms'].apply(lambda x: pre_process(x))

    #creating lists to store spam/non-spam associated words and their instances
    spam_words, ham_words = categorize_words()

    #storing user input and processing it
    user_sms = pre_process(" ".join(args.sms))

    predict(user_sms)
