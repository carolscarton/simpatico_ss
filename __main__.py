import sys  

reload(sys)  
sys.setdefaultencoding('utf8')

from simpatico_ss.simplify import Simplify
import sys

doc = sys.argv[1]

s = Simplify(doc)

simp_doc = s.simplify()

for simp in simp_doc:
    print simp

#print simp_doc

#parser = Parser(doc)

#print parser.process()

#parse_sents = parser.process()

#a = [[parser for parser in dep_graphs] for dep_graphs in parser.process()]

#for i in parse_sents:
#    for d in i:
#        for a in d.triples():
#            print a
        #for t in range(1,50):
        #    if d.contains_address(t):
        #        b = d.get_by_address(t)
        #        print b[u'word']

#print sum([[parse.tree() for parse in dep_graphs] for dep_graphs in parser.process()],[])
