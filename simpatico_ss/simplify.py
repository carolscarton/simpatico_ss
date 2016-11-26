import en
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
        self.time = ['when', 'after', 'since', 'before', 'once']
        self.concession = ['although', 'though', 'but', 'however', 'whereas']
        self.justify = ['because', 'so', 'while']
        self.condition = ['if']
        self.condition2 = ['or']
        self.addition = ['and']
        
        #list of all markers for analysis purposes
        self.cc = self.time + self.concession + self.justify + self.condition + self.addition + self.condition2

        self.relpron = ['whom', 'whose', 'which', 'who']
        

        
    def transformation(self, sent, ant, justify=False):
        """
        Transformation step in the simplification process.
        This is a recursive method that receives two parameters:
        @param sent: sentence to be simplified.
        @param ant: previous sentence. If sent = ant, then no simplification should be performed.
        @param justify: controls cases where sentence order is inverted and should invert the entire recursion.
        """
        

        def recover_punct(final, s):
            """
            Recover the punctuation of the sentence (needed because the dependency parser does not keep punctuation.
            @param final: the final dictionary with the words in order
            @param s: the tokenised sentence with the punctuation marks
            @return the final dictionary with the punctuation marks
            """

            char_list = "``\'\'"
            ant = 0
            for k in sorted(final.keys()):
                if int(k) - ant == 2 :
                    if s[k-2] in string.punctuation + char_list:
                        final[k-1] = s[k-2]
                    elif s[k-2] == "-RRB-":
                        final[k-1] = ")"
                    elif s[k-2] == "-LRB-":
                        final[k-1] = "("
                if int(k) - ant == 3 :
                    if s[k-2] in string.punctuation + char_list and s[k-3] in string.punctuation + char_list:
                        final[k-1] = s[k-2]
                        final[k-2] = s[k-3]
                ant = k
            return final


        def build(root, dep, aux, final, yes_root=True):
            """
            Creates a dictionary with the words of a simplified clause, following the sentence order.
            This is a recursive method that navigates through the dependency tree.
            @param root: the root node in the dependency tree
            @param dep: the dependencies of the root node
            @param aux: the auxiliary parser output
            @param final: dictionary with the positions and words
            """
            if yes_root:
                final[root]=aux.get_by_address(root)[u'word']
            for k in dep.keys():
                for i in dep[k]:
                    deps = dict(aux.get_by_address(i)[u'deps'])
                    build(i, deps, aux, final)
                    final[i]=aux.get_by_address(i)[u'word']

        def print_sentence_voice(final_subj, final_obj, verb, v_aux,  v_tense, subj_tag, subj_word, final_mod2=None, final_root=None):
            new_verb = ''
            s_sentence1 = s_sentence2 = ''
            if v_tense in ('VBD'):
                new_verb = en.verb.past(verb) + " "
            elif v_tense == 'MD' :
                new_verb = v_aux.lower() + " " + en.verb.infinitive(verb) + " "      
            elif v_tense in ('VBZ', 'VBP'):
                if subj_tag in ("NNS", "NNPS"):
                    new_verb = en.verb.present(verb, person=2) + " "
                elif subj_tag in ("NN", "NNP"):
                    new_verb = en.verb.present(verb, person=3) + " "
                elif subj_tag in ("PRP") and subj_word.lower() in ("i", "me") and len(final_subj) == 1:
                    new_verb = en.verb.present(verb, person = 1) + " "
                elif subj_tag in ("PRP") and subj_word.lower() in ("he", "she", "it", "her", "him") and len(final_subj) == 1:
                    new_verb = en.verb.present(verb, person = 3) + " "
                else:
                    new_verb = en.verb.present(verb, person = 2) + " "
            elif v_tense in ('VBG'):
                if subj_tag in ("NNS", "NNPS"):
                    new_verb = en.verb.present(v_aux.lower(), person = 2, negate = False) + " " + en.verb.present_participle(verb) + " "
                elif subj_tag in ("NN", "NNP"):
                    new_verb = en.verb.present(v_aux.lower(), person = 3, negate = False) + " " + en.verb.present_participle(verb) + " "
                elif subj_tag in ("PRP") and subj_word.lower() in ("i", "me") and len(final_subj) == 1:
                    new_verb = en.verb.present(v_aux.lower(), person = 1, negate = False) + " " + en.verb.present_participle(verb) + " "
                elif subj_tag in ("PRP") and subj_word.lower() in ("he", "she", "it", "her", "him") and len(final_subj) == 1:
                    new_verb = en.verb.present(v_aux.lower(), person = 3, negate = False) + " " + en.verb.present_participle(verb) + " "
                else:
                    new_verb = en.verb.present(v_aux.lower(), person = 2, negate = False) + " " + en.verb.present_participle(verb) + " "

            elif v_tense in ('VBN'):
                if subj_tag in ("NNS", "NNPS"):
                    new_verb = en.verb.present(v_aux.lower(), person = 2, negate = False) + " " + en.verb.past_participle(verb) + " "
                elif subj_tag in ("NN", "NNP"):
                    new_verb = en.verb.present(v_aux.lower(), person = 3, negate = False) + " " + en.verb.past_participle(verb) + " "
                elif subj_tag in ("PRP") and subj_word.lower() in ("i", "me") and len(final_subj) == 1:
                    new_verb = en.verb.present(v_aux.lower(), person = 1, negate = False) + " " + en.verb.past_participle(verb) + " "
                elif subj_tag in ("PRP") and subj_word.lower() in ("he", "she", "it", "her", "him") and len(final_subj) == 1:
                    new_verb = en.verb.present(v_aux.lower(), person = 3, negate = False) + " " + en.verb.past_participle(verb) + " "
                else:
                    new_verb = en.verb.present(v_aux.lower(), person = 2, negate = False) + " " + en.verb.past_participle(verb) + " "
            
            if subj_tag in ("PRP") and subj_word.lower() == "me" and len(final_subj) == 1:
                for k in final_subj.keys():
                    final_subj[k] = "I"
            elif subj_tag in ("PRP") and subj_word.lower() == "her" and len(final_subj) == 1:
                for k in final_subj.keys():
                    final_subj[k] = "she"
            elif subj_tag in ("PRP") and subj_word.lower() == "him" and len(final_subj) == 1:
                for k in final_subj.keys():
                    final_subj[k] = "he"
            elif subj_tag in ("PRP") and subj_word.lower() == "them" and len(final_subj) == 1:
                for k in final_subj.keys():
                    final_subj[k] = "them"
            elif subj_tag in ("PRP") and subj_word.lower() == "us" and len(final_subj) == 1:
                for k in final_subj.keys():
                    final_subj[k] = "we"


            #print v_tense
            #print subj_tag

            for k in sorted(final_subj.keys()):
                s_sentence1 += final_subj[k] + " "

            for k in sorted(final_obj.keys()):
                s_sentence2 += final_obj[k] + " "

            if final_mod2 != None:
                for k in sorted(final_mod2.keys()):
                    s_sentence2 += final_mod2[k] + " "
            if final_root != None:
                for k in sorted(final_root.keys()):
                    s_sentence2 += final_root[k] + " "

            return s_sentence1 + new_verb + s_sentence2 + ". "

        def print_sentence_appos(final_root, final_appos, final_subj, v_tense, n_num, subj_word):
            """
            Finalise the simplification process for appostive cluases.
            TODO: this should be removed from here and moved to generation phase
            TODO: punctuation recovery
            
            """
            s_sentence = ''
            s_sentence2 = ''
            for k in sorted(final_root.keys()):
                s_sentence += final_root[k] + " "
            s_sentence += "."

            for k in sorted(final_subj.keys()):
                s_sentence2 += final_subj[k] + " "


            if n_num in ("NN", "NNP"):
                if v_tense in ("VBP", "VBZ", "VB"):
                    s_sentence2 += "is "
                elif v_tense in ("VBD", "VBG", "VBN"):
                    s_sentence2 += "was "

            elif n_num in ("NNS", "NNPS"):
                if v_tense in ("VBP", "VBZ", "VB"):
                    s_sentence2 += "are "
                elif v_tense in ("VBD", "VBG", "VBN"):
                    s_sentence2 += "were "

            elif n_num in ("PRP") and subj_word.lower() == "they":

                if v_tense in ("VBP", "VBZ", "VB"):
                    s_sentence2 += "are "
                elif v_tense in ("VBD", "VBG", "VBN"):
                    s_sentence2 += "were "

            elif n_num in ("PRP"):
                if v_tense in ("VBP", "VBZ", "VB"):
                    s_sentence2 += "is "
                elif v_tense in ("VBD", "VBG", "VBN"):
                    s_sentence2 += "was "

            for k in sorted(final_appos.keys()):
                s_sentence2 += final_appos[k] + " "
            s_sentence2 += "."
            return s_sentence, s_sentence2
            


        def print_sentence(final1, final2, root_tag=None, mark=None, mark_pos=None, modal=None):
            """
            Finalise the simplification process by including markers and punctuation.
            TODO: this should be removed from here and moved to generation phase.
            TODO: punctuation recovery.
            @param final1: dictionary of first clause 
            @param final2: dictionary of second clause
            @param root_tag: POS tag of the root node
            @mark marker that triggered the simplification
            @return: two sentences, one for each clause.
            """ 
            s_sentence = ''
            s_sentence2 = ''
            
            ## control the markers that should be added into the simplified sentences
            if mark in self.addition:
                s_sentence2 += 'And '
            if mark in self.condition:
                s_sentence += 'Suppose '
                if final2[sorted(final2.keys())[0]].lower() != 'then':
                    s_sentence2 += 'Then '
            elif mark in self.concession:
                s_sentence2 += 'But '
            elif mark in self.time:
                if mark_pos > 1:
                    if root_tag == 'VBP' or root_tag == 'VBZ' or root_tag == 'VB':
                        s_sentence2 += 'This is ' + mark + " "
                    else:
                        s_sentence2 += 'This was ' + mark + " "
                else:

                    if root_tag == 'VBP' or root_tag == 'VBZ':
                        s_sentence2 += 'This happens ' + mark + " "
                    elif root_tag == 'VB' and modal != None: 
                        s_sentence2 += 'This ' + modal + ' happen ' + mark + " "
                    else:
                        s_sentence2 += 'This happened ' + mark + " "

            elif mark in self.justify:
                s_sentence2 += 'So '
            elif mark in self.condition2:
                s_sentence2 += 'Alternatively '

            ## build first sentence
            for k in sorted(final1.keys()):
                s_sentence += final1[k] + " "
            s_sentence += ". "


            ## build second sentence
            for k in sorted(final2.keys()):
                s_sentence2 += final2[k] + " "
            s_sentence2 += ". "
            
            s_sentence = s_sentence.replace("either ", "")
            s_sentence2 = s_sentence2.replace("either ", "")
            s_sentence = s_sentence.replace("Either ", "")
            s_sentence2 = s_sentence2.replace("Either ", "")


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
            v_tense = ""
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
                    if u'cc' in deps_root.keys() and u'conj' in deps_root.keys():
                        conj = deps_root[u'conj'][0]
                        if 'VB' in aux.get_by_address(conj)[u'tag'] and 'VB'in aux.get_by_address(root)[u'tag']: #needed for broken cases like 'Care and support you won't have to pay towards'
                            mark = deps_root[u'cc'][0]
                            mark_name = aux.get_by_address(mark)[u'word'].lower()
                        else:
                            return False, ant
                    else:
                        return False, ant
                
                ## dealing with cases without subject 
                if u'nsubj' not in deps_other and u'nsubj' in deps_root:
                    deps_other[u'nsubj'] = deps_root[u'nsubj']
                elif u'nsubj' not in deps_other and u'nsubjpass' in deps_root:
                    deps_other[u'nsubj'] = deps_root[u'nsubjpass']
                elif u'nsubj' not in deps_other and u'nsubj' not in deps_root:
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

                    tag_list = (u'acomp', u'amod', u'appos', u'cc', u'ccomp', u'dep', u'dobj', u'iobj', u'nwe', u'pcomp', u'pobj', u'prepc', u'rcmod', u'ucomp', u'nmod', u'auxpass')

                    if not any([t in tag_list  for t in deps_root.keys()]):
                        return False, ant
                    elif not any([t in tag_list  for t in deps_other.keys()]):
                        return False, ant

                    #if (len(deps_root) < 2 or len(deps_other) < 2):
                    #   return False, ant
                    
                    ## for cases with time markers -- This + modal + happen
                    modal = None
                    if u'aux' in deps_root and mark_name in self.time:
                        modal = aux.get_by_address(deps_root[u'aux'][0])[u'word']

                    ## for cases either..or with the modal verb attached to the main clause
                    if u'aux' in deps_root and mark_name in self.condition2:
                        deps_other[u'aux'] = deps_root[u'aux']
                   
                    
                    ## built the sentence again
                    final_root = {}
                    build(root, deps_root, aux, final_root)
                    final_deps = {}
                    build(o, deps_other, aux, final_deps)

                    ## recover punctuation
                    final_root = recover_punct(final_root, s)
                    final_deps = recover_punct(final_deps, s)

                    ## check if verbs have objects
                    #if len(final_root.keys()) < 2 or len(final_deps.keys()) < 2 and mark_name.lower() == 'and':
                    #    return False, ant
                    
                    ## TODO: remove this part from here --> move to another module: generation
                    root_tag =  aux.get_by_address(root)[u'tag']
                    justify = True
                    #if ((root > o) and (mark_name in self.time and mark>1)) or (mark_name == 'because' and mark > 1):
                    if (root > o) or (mark_name == 'because' and mark > 1):
                        if (mark_name in self.time and mark == 1):
                            sentence1, sentence2 = print_sentence(final_root, final_deps, root_tag, mark_name, mark, modal)
                        else:
                            sentence1, sentence2 = print_sentence(final_deps, final_root, root_tag, mark_name, mark, modal)
                    else:
                        sentence1, sentence2 = print_sentence(final_root, final_deps, root_tag, mark_name, mark, modal)
                        

                    
                    s1 = self.transformation(sentence1, ant, justify)
                    s2 = self.transformation(sentence2, ant)

                    return True, s1 + " " +  s2
                else:
                    return False, ant


        def relative_clauses(aux, root, deps_root, ant, rel):
            """
            Simplify relative clauses
            @param aux: auxiliary parser output
            @param root: root node in the dependency tree
            @param deps_root: dependencies of the root node
            @param ant: previous sentence (for recursion purposes)
            @param rel: parser relation between the main and the dependent clause (can be 'nsubj' or 'dobj')
            @return: a flag that indicates whether or not the sentence was simplified and the result sentence (if flag = False, ant is returned)
            """
            subj = deps_root[rel][0]
            deps_subj = dict(aux.get_by_address(subj)[u'deps'])
            if 'acl:relcl' in deps_subj.keys():
                relc = deps_subj['acl:relcl'][0]
                deps_relc = dict(aux.get_by_address(relc)[u'deps'])

                if u'nsubj' in deps_relc.keys():
                    subj_rel = u'nsubj'
                elif u'nsubjpass' in deps_relc.keys():
                    subj_rel = u'nsubjpass'

                if aux.get_by_address(deps_relc[subj_rel][0])[u'word'].lower() in self.relpron:
                    deps_relc[subj_rel][0] = subj
                elif u'dobj' in deps_relc: ## needed for cases where the subject of the relative clause is the object
                    obj = deps_relc[u'dobj'][0]
                    mod = aux.get_by_address(obj)[u'deps'][u'nmod:poss'][0]
                    aux.get_by_address(mod)[u'word'] = aux.get_by_address(subj)[u'word'] + '\'s'
                    aux.get_by_address(mod)[u'deps'] = aux.get_by_address(subj)[u'deps']
                else:
                    return False, ant #for borken cases - " There are some situations where it is particularly important that you get financial information and advice that is independent of us."

                del aux.get_by_address(subj)[u'deps'][u'acl:relcl']

                
                final_root= {}
                build(root, deps_root, aux, final_root)
                final_relc = {}
                build(relc, deps_relc, aux, final_relc)

                final_root = recover_punct(final_root, s)
                final_relc = recover_punct(final_relc, s)

                if justify:
                    sentence2, sentence1 = print_sentence(final_root, final_relc)
                else:
                    sentence1, sentence2 = print_sentence(final_root, final_relc)

                s1 = self.transformation(sentence1, ant, justify)
                s2 = self.transformation(sentence2, ant)
                return True, s1 + " " +  s2
            else:
                return False, ant


        def appositive_phrases(sent, ant):
            """
            Simplify appositive phrases
            @param aux: auxiliary parser output
            @param root: root node in the dependency tree
            @param deps_root: dependencies of the root node
            @param ant: previous sentence (for recursion purposes)
            @return: a flag that indicates whether or not the sentence was simplified and the result sentence (if flag = False, ant is returned)
            """

            ## parser
            try:
                parser = Parser(sent)
                parsed = parser.process()

            except AssertionError:
                return False, ant

            for aux in parsed:
                
                ## root
                root = dict(aux.get_by_address(0)[u'deps'])['root'][0]

                ## root dependencies
                deps_root = dict(aux.get_by_address(root)[u'deps'])


                ## apposition needs to have a subject -- same subject of the mais sentence.
                if u'nsubj' in deps_root:

                    subj = deps_root[u'nsubj'][0]
                    subj_word = aux.get_by_address(subj)[u'word']
                    deps_subj = dict(aux.get_by_address(subj)[u'deps'])
                    v_tense = aux.get_by_address(root)[u'tag']
                    n_num = aux.get_by_address(subj)[u'tag']
                    if u'amod' in deps_subj: ## bug -- this generates several mistakes... 
                        mod = deps_subj[u'amod'][0]
                        deps_mod = dict(aux.get_by_address(mod)[u'deps'])
                        del aux.get_by_address(subj)[u'deps'][u'amod']
                        deps_subj = dict(aux.get_by_address(subj)[u'deps'])
                        
                        ## Treat simple cases such as 'general rule'
                        if 'JJ' in aux.get_by_address(mod)[u'tag'] and len(deps_mod.keys()) == 0: 
                            return False, ant

                    elif u'appos' in deps_subj:
                        mod = deps_subj[u'appos'][0]
                        deps_mod = dict(aux.get_by_address(mod)[u'deps'])
                        del aux.get_by_address(subj)[u'deps'][u'appos']
                        deps_subj = dict(aux.get_by_address(subj)[u'deps'])
                    else:
                        return False, ant

                    final_root = {}
                    build(root, deps_root, aux, final_root)
                    final_appos = {}
                    build(mod, deps_mod, aux, final_appos)
                    final_subj = {}
                    build(subj, deps_subj, aux, final_subj)

                    if len(final_appos.keys()) < 2:
                        return False, ant

                    final_root = recover_punct(final_root, s)
                    final_appos = recover_punct(final_appos, s)
                    final_subj = recover_punct(final_subj, s)
                    
                    sentence1, sentence2 = print_sentence_appos(final_root, final_appos, final_subj, v_tense, n_num, subj_word)
                    s1 = self.transformation(sentence1, ant)
                    s2 = self.transformation(sentence2, ant)
                    return True, s1 + " " + s2
                else:
                    return False, ant

        def passive_voice(sent, ant):
            try: 
                parser = Parser(sent)
                parsed = parser.process()
            except AssertionError:
                return False, ant

            for aux in parsed:
                root = dict(aux.get_by_address(0)[u'deps'])['root'][0]

                #print root
                deps_root = dict(aux.get_by_address(root)[u'deps'])

                #print deps_root
            
                if u'auxpass' in deps_root.keys():
                    
                    if u'nmod' in deps_root:

                        subj = deps_root[u'nsubjpass'][0]
                        deps_subj = dict(aux.get_by_address(subj)[u'deps'])
                        
                        aux_tense = aux.get_by_address(deps_root[u'auxpass'][0])[u'tag']
                        v_aux = None

                        if aux_tense == 'VB' and u'aux' in deps_root.keys():
                            aux_tense = aux.get_by_address(deps_root[u'aux'][0])[u'tag']
                            v_aux = aux.get_by_address(deps_root[u'aux'][0])[u'word']
                            del deps_root[u'aux']
                        elif aux_tense == 'VBG' and u'aux' in deps_root.keys():
                            #aux_tense = aux.get_by_address(deps_root[u'aux'][0])[u'tag']
                            v_aux = aux.get_by_address(deps_root[u'aux'][0])[u'word']
                            del deps_root[u'aux']
                        elif aux_tense == 'VBN' and u'aux' in deps_root.keys():
                            v_aux = aux.get_by_address(deps_root[u'aux'][0])[u'word']
                            if v_aux.lower() in ("has", "have"):
                                v_aux = aux.get_by_address(deps_root[u'aux'][0])[u'word']
                            else:
                                aux_tense = 'MD'
                            del deps_root[u'aux']
                           
                        del deps_root[u'auxpass']
                        del deps_root[u'nsubjpass']

                        if len(deps_root[u'nmod']) > 1:
                            mod = deps_root[u'nmod'][1]
                            mod2 = deps_root[u'nmod'][0]
                            deps_mod = dict(aux.get_by_address(mod)[u'deps'])
                            deps_mod2 = dict(aux.get_by_address(mod2)[u'deps'])
                            if u'case' in deps_mod:
                                if aux.get_by_address(deps_mod[u'case'][0])[u'word'].lower() != 'by':
                                    return False, ant
                                del deps_mod[u'case']
                                del deps_root[u'nmod']
                                subj_tag = aux.get_by_address(mod)[u'tag']
                                subj_word =aux.get_by_address(mod)[u'word']  
                                final_subj = {}
                                build(mod, deps_mod, aux, final_subj)
                                
                                final_obj = {}
                                build(subj, deps_subj, aux, final_obj)
                                
                                final_mod2 = {}
                                build(mod2, deps_mod2, aux, final_mod2)

                                final_root = {}
                                build(root, deps_root, aux, final_root, False)
                                
                                final_subj = recover_punct(final_subj, s)
                                final_obj = recover_punct(final_obj, s)
                                final_mod2 = recover_punct(final_mod2, s)
                                
                                sentence1 = print_sentence_voice(final_subj, final_obj, aux.get_by_address(root)[u'word'], v_aux, aux_tense, subj_tag, subj_word, final_mod2, final_root)
                                s1 = self.transformation(sentence1, ant)
                                return True, s1
                            elif u'case' in deps_mod2:
                                if aux.get_by_address(deps_mod2[u'case'][0])[u'word'].lower() != 'by':
                                    return False, ant
                                del deps_mod2[u'case']
                                del deps_root[u'nmod']
                                subj_tag = aux.get_by_address(mod2)[u'tag']
                                subj_word = aux.get_by_address(mod)[u'word']
                                
                                final_subj = {}
                                build(mod2, deps_mod2, aux, final_subj)
                                
                                final_obj = {}
                                build(subj, deps_subj, aux, final_obj)
                                
                                final_mod2 = {}
                                build(mod, deps_mod, aux, final_mod2)

                                final_root = {}
                                build(root, deps_root, aux, final_root, False)

                                final_subj = recover_punct(final_subj, s)
                                final_obj = recover_punct(final_obj, s)
                                final_mod2 = recover_punct(final_mod2, s)
                                final_root = recover_punct(final_root, s)
                                sentence1 = print_sentence_voice(final_subj, final_obj, aux.get_by_address(root)[u'word'], v_aux, aux_tense, subj_tag, subj_word, final_mod2, final_root)
                                s1 = self.transformation(sentence1, ant)
                                return True, s1
                            else:
                                return False, ant

                        else:
                            mod = deps_root[u'nmod'][0]
    
                            deps_mod =  dict(aux.get_by_address(mod)[u'deps'])

                            if u'case' in deps_mod:
                                if aux.get_by_address(deps_mod[u'case'][0])[u'word'].lower() != 'by':
                                    return False, ant
                                #print deps_mod

                                del deps_mod[u'case']
                                del deps_root[u'nmod']

                                subj_tag = aux.get_by_address(mod)[u'tag']
                                subj_word = aux.get_by_address(mod)[u'word']
                    
                                final_subj = {}
                                build(mod, deps_mod, aux, final_subj)

                                final_obj = {}
                                build(subj, deps_subj, aux, final_obj)
                        
                                final_root = {}
                                build(root, deps_root, aux, final_root, False)

                                final_subj = recover_punct(final_subj, s)
                                final_obj = recover_punct(final_obj, s)
                                final_root = recover_punct(final_root, s)

                                #print final_subj
                                #print final_obj


                                sentence1 = print_sentence_voice(final_subj, final_obj, aux.get_by_address(root)[u'word'], v_aux, aux_tense, subj_tag, subj_word, final_root)
                                #print simpl
                                s1 = self.transformation(sentence1, ant)
                                return True, s1
                            else:
                                return False, ant
                    else: 
                        return False, ant
                else:
                    return False, ant

                

        ## MAIN OF TRANSFORMATION
        ## control recursion: check whether there is no simplification to be done
        if sent == ant:
            return sent

        flag = False

        ant = sent

        ## tokenizer 
        tokenizer = StanfordTokenizer()
        sent_tok = tokenizer.tokenize(sent)

        s = sent_tok
        
        ## dealing with questions
        ## TODO: improve this control with parser information.
        if s[0].lower() in ("what", "where", "when", "whose", "who", "which", "whom", "whatever", "whatsoever", "whichever", "whoever", "whosoever", "whomever", "whomsoever", "whoseever", "whereever") and s[-1] == "?":
            return ant

        ## deal with apposition
        flag, simpl = appositive_phrases(sent, ant)
        if flag:
            return simpl
        
        
        ## analyse whether or not a sentence has simplification clues (in this case, discourse markers or relative pronouns)
        a = Analysis(s, self.cc, self.relpron)

        flag_cc, type_cc = a.analyse_cc()

        ## if sentence has a marker that requires attention
        if flag_cc:
            
            ## parser the parser needs to be called for each case, otherwise it breaks (iterator problems)
            ## TODO: optmise the parser calls
            try:
                parser = Parser(sent)
                parsed = parser.process()

            except AssertionError:
                return ant
        
            ## reads parsed sentence
            for aux in parsed:
                    
                ## root
                root = dict(aux.get_by_address(0)[u'deps'])['root'][0]

                    
                ## root dependencies
                deps_root = dict(aux.get_by_address(root)[u'deps'])


                ## search for 'advcl' clause (for cases with 'although', 'though', ...)
                if 'advcl' in deps_root.keys():
                    flag, simpl = conjoint_clauses(aux, root, deps_root, ant, type_cc, u'advcl')
                    if flag:
                        return simpl
                ## search for 'conj' clause (for cases with 'and' and 'but' in the middle of the sentence)
                if 'conj' in deps_root.keys():
                    flag, simpl = conjoint_clauses(aux, root, deps_root, ant, type_cc, u'conj')
                    if flag:
                        return simpl

                else:
                    flag = False #if there is no 'advcl', then do not simplify

                    
    
        flag_rc, type_rc = a.analyse_rc()

        ## if sentence has a relative pronoun
        if flag_rc:
                
    
            ## parser
            try:
                parser = Parser(sent)
                parsed = parser.process()

            except AssertionError:
                return ant
            
            for aux in parsed:
                
                ## root
                root = dict(aux.get_by_address(0)[u'deps'])['root'][0]

                ## root dependencies
                deps_root = dict(aux.get_by_address(root)[u'deps'])

                ## check where is the dependency of the relative clause
                if u'nsubj' in deps_root:
                    flag, simpl = relative_clauses(aux, root, deps_root, ant, u'nsubj')
                    if flag:
                        return simpl
                elif u'dobj' in deps_root:
                    flag, simpl = relative_clauses(aux, root, deps_root, ant, u'dobj')
                    if flag:
                        return simpl

                else:
                    flag = False

        


        ## deal with passive voice
        flag, simpl = passive_voice(sent, ant)
        if flag:
            return simpl

        
        
        if flag== False:
            return ant
        #else:
        #    return simpl

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
