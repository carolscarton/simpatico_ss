class Analysis():

    def __init__(self, sentence, cc):
        """
        Perform the analyses check for syntactic simplification.
        @param sentence: sentence to be checked.
        @param cc: conjoint clauses makers.
        """
        self.sentence = sentence
        self.cc = cc

    def analyse_cc(self):
        """
        Analyse sentences searching for markers that could indicate conjoing clauses.
        @return: a flag indicating whether or not a maker was identified and a list of markers found (None if flag = False).
        """
        if any([s.lower() in self.cc for s in self.sentence]):
            mark = []
            for s in self.sentence:
                if s.lower() in self.cc and "this was " + s.lower() not in " ".join(self.sentence).lower() and "this is " + s.lower() not in " ".join(self.sentence).lower():
                    mark.append(s.lower())
            return True, mark
        else: 
            return False, None

