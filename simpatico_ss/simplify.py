from analysis import Analysis
from nltk.tokenize import StanfordTokenizer
from util import Parser
import string

class Simplify():

    def __init__(self, doc):
        """
        Perform syntactic simplification rules.
        @param doc: document to be simplified.
        """
        self.sentences = open(doc, "r").read().strip().split("\n")
        #markers are separated by their most used sense
        self.time = ['when', 'after', 'since', 'before']
        self.concession = ['although', 'though', 'but', 'however', 'whereas', 'while']
        self.justify = ['because', 'so']
        self.condition = ['if']
        self.addition = ['and']
        #list of all markers for analysis purposes
        self.cc = self.time + self.concession + self.justify + self.condition + self.addition
        

        
    def transformation(self, sent, ant):
        """
        Transformation step in the simplification process.
        This is a recursive method that receives two parameters:
        @param sent: sentence to be simplified.
        @param ant: previous sentence. If sent = ant, then no simplification should be performed.
        """
        
        def build(root, dep, aux, final):
            """
            Creates a dictionary with the words of a simplified clause, following the sentence order.
            This is a recursive method that navigates through the dependency tree.
            @param root: the root node in the dependency tree
            @param dep: the dependencies of the root node
            @param aux: the auxiliary parser output
            @param final: dictionary with the positions and words
            @return: dictionary with position as keys as words as values.
            """
            final[root]=aux.get_by_address(root)[u'word']
            for k in dep.keys():
                for i in dep[k]:
                    deps = dict(aux.get_by_address(i)[u'deps'])
                    build(i, deps, aux, final)
                    final[i]=aux.get_by_address(i)[u'word']

        def print_sentence(final1, final2, root_tag, mark=None):
            """
            Finalise the simplification process by including markers and punctuation.
            TODO: this should be removed from here and moved to generation phase.
            @param final1: dictionary of first clause 
            @param final2: dictionary of second clause
            @param root_tag: POS tag of the root node
            @mark marker that triggered the simplification
            @return: two sentences, one for each clause.
            """ 
            s_sentence = ''
            s_sentence2 = ''
            if mark in self.addition:
                s_sentence2 += 'And '
            if mark in self.condition:
                s_sentence += 'Suppose '
                if final2[sorted(final2.keys())[0]].lower() != 'then':
                    s_sentence2 += 'Then '
            elif mark in self.concession:
                s_sentence2 += 'But '
            elif mark in self.time:
                if root_tag == 'VBP' or root_tag == 'VBZ':
                    s_sentence2 += 'This is ' + mark + " "
                else:
                    s_sentence2 += 'This was ' + mark + " "
            elif mark in self.justify:
                s_sentence2 += 'So '

            for k in sorted(final1.keys()):
                s_sentence += final1[k] + " "
            s_sentence += ". "

            for k in sorted(final2.keys()):
                s_sentence2 += final2[k] + " "
            s_sentence2 += ". "
            s_sentence = s_sentence[0].capitalize() + s_sentence[1:]
            s_sentence2 = s_sentence2[0].capitalize() + s_sentence2[1:]
            return s_sentence, s_sentence2

        def conjoint_clauses(aux, root, deps_root, ant, _type, rel):
            """
            Simplify conjoint clauses
            @param aux: auxiliary parser output
            @param root: root node in the dependency tree
            @param deps_root: dependencies of the root node
            @param ant: previous sentence (for recursion purposes)
            @param _type: list of markers found in the sentence that can indicate conjoint clauses
            @param rel: parser relation between the main and the dependent clause (can be 'advcl' or 'conj')
            @return: a flag that indicates whether or not the sentence was simplified and the result sentence (if flag = False, ant is returned)
            """
            ## split the clauses
            others = dict(aux.get_by_address(root)[u'deps'])[rel]
            pos = 0
            flag = True
            s1 = s2 = ""
            for o in others:
                deps_other = dict(aux.get_by_address(o)[u'deps'])

                ## check the marker position ('when' is advmod, while others are mark)
                if rel == u'advcl':
                    if u'mark' in deps_other.keys():
                        mark = deps_other[u'mark'][0]
                        mark_name = aux.get_by_address(mark)[u'word'].lower()
                    elif u'advmod' in deps_other.keys():
                        mark = deps_other[u'advmod'][0]
                        mark_name = aux.get_by_address(mark)[u'word'].lower()
                    else: 
                        return False, ant #needed for broken cases
                else:
                    if u'cc' in deps_root.keys():
                        mark = deps_root[u'cc'][0]
                        mark_name = aux.get_by_address(mark)[u'word'].lower()
                    else:
                        return False, ant
                                

                ## check if the marker is in the list of selected markers
                if mark_name in _type:
                                
                    ## delete marker and relation from the graph
                    if rel == u'advcl':
                        if u'mark' in deps_other.keys():
                             del deps_other[u'mark']
                        elif u'advmod' in deps_other.keys():
                            del deps_other[u'advmod']
                    else:
                        del deps_root[u'cc']
                                
                    del deps_root[rel][pos]
                    pos+=1

                    ## built the sentence again
                    final_root = {}
                    build(root, deps_root, aux, final_root)
                    final_deps = {}
                    build(o, deps_other, aux, final_deps)
                    
                    ## TODO: remove this part from here --> move to another module: generation
                    root_tag =  aux.get_by_address(root)[u'tag']
                    if (root > o) or (mark_name == 'because' and mark > 1): 
                        sentence1, sentence2 = print_sentence(final_deps, final_root, root_tag, mark_name)

                    else:
                        sentence1, sentence2 = print_sentence(final_root, final_deps, root_tag, mark_name)

                    s1 = self.transformation(sentence1, ant)
                    s2 = self.transformation(sentence2, ant)
                                    
                    return True, s1 + " " +  s2
                else:
                    return False, ant



        ## control recursion: check whether there is no simplification to be done
        if sent == ant:
            return sent

        ant = sent

        ## tokenizer 
        tokenizer = StanfordTokenizer()
        sent_tok = tokenizer.tokenize(sent)

        ## parser
        parser = Parser(sent)
        parsed = parser.process()


        s = sent_tok
            
        ## analyse whether or not a sentence has simplification clues (in this case, discourse markers)
        a = Analysis(s, self.cc)
        flag,_type = a.analyse_cc()

        ## if sentence has a marker that requires attention
        if flag:


            ## reads parsed sentence
            for aux in parsed:
                    
                ## root
                root = dict(aux.get_by_address(0)[u'deps'])['root'][0]
                    
                ## root dependencies
                deps_root = dict(aux.get_by_address(root)[u'deps'])

                ## search for 'advcl' clause (for cases with 'although', 'though', ...)
                if 'advcl' in deps_root.keys():
                    flag, simpl = conjoint_clauses(aux, root, deps_root, ant, _type, u'advcl')
                    return simpl
                ## search for 'conj' clause (for cases with 'and' and 'but' in the middle of the sentence)
                if 'conj' in deps_root.keys():
                    flag, simpl = conjoint_clauses(aux, root, deps_root, ant, _type, u'conj')
                    return simpl



                else:
                    flag = False #if there is no 'advcl', then do not simplify
    
        if flag== False:
            return " ".join(s)

    def simplify(self):        
        """
        Call the simplification process for all sentences in the document.
        """
        c = 0
        simp_sentences = []
        for s in self.sentences:

            print "Original: " + s
            
            simp_sentences.append(self.transformation(s, ''))

            ## for demonstration purposes only. remove the prints later
            print "Simplified: ",
            print simp_sentences[c]
            c+=1

            print   
        return simp_sentences
