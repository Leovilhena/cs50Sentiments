import nltk
import os
import sys

class Analyzer():
    """Implements sentiment analysis."""
    
    def __init__(self, positives, negatives):
        """Initialize Analyzer."""
        
        self.positives = positives
        self.negatives = negatives
        self.positive_words = []
        self.negative_words = []
        
        # try to open files, append to new list without ';' and '\n' and closes
        with open(self.positives, 'r') as p:
            for lines in p:
                if not lines.startswith(';') and not lines.startswith('\n'):
                    self.positive_words.append(lines.strip('\n'))
            
        with open(self.negatives, 'r') as n:
            for lines in n:
                if not lines.startswith(';') and not lines.startswith('\n'):
                    self.negative_words.append(lines.strip('\n'))

  
    def analyze(self, text):
        """Analyze text for sentiment, returning its score."""
        
        # initialize score and sets at 0
        score = 0
        
        # instantiate tokenizer
        tokenizer = nltk.tokenize.TweetTokenizer()
        
        # create a list of words from tweet
        tokens = tokenizer.tokenize(text)
      
        # iterates through tokens and return score of positive vs negative words
        for token in tokens:
            if token.lower() in self.positive_words:
                score += 1
            elif token.lower() in self.negative_words:
                score -= 1
                
        return score
