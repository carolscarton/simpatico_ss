from nltk.parse.stanford import StanfordDependencyParser

class Parser():
    def __init__(self, sentences):
        self.sentences = sentences
    
    def process(self):
        #sentences = open(self.doc, "r").read().strip().split("\n")
        #sentences = [l.strip().split(' ') for l in f_read]
        dep_parser = StanfordDependencyParser(model_path="edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")
        return dep_parser.raw_parse(self.sentences)

