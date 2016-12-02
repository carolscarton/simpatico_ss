# simpatico_ss
Syntactic Simplification for the SIMPATICO project.

This system implements the syntactic simplification rules proposed by Siddharthan (2004) and Siddharthan and Angrosh (2014).
Our implementation uses the Stanford Dependency Parser available at CoreNLP (http://stanfordnlp.github.io/CoreNLP/).
The Dependency parser is initialised as a server using the code available at https://github.com/Wordseer/stanford-corenlp-python (please refer to this for the specific license).

-----------------------------------------------------------------------
**First Release**

This release deals with the simplification of conjoint clauses, relative clauses, appositive phrases and passive voice.
Simplifications are made according to the parser tree output, given priority to the relations that are in the top of the tree.
Sentences are simplified recursively until there is nothing more to be simplified.

-----------------------------------------------------------------------
**External Resources/Tool**
Apart from the CoreNLP server code, we also use two external libraries:

-- NodeBox (https://www.nodebox.net/code/index.php/Linguistics#verb_conjugation)
-- Truecaser (https://github.com/nreimers/truecaser)

Such libraries are embedded in this code, but please refer to their licenses before using them. 

For the truecaser a model file .obj is required. Please download the English pre-trained model from https://github.com/nreimers/truecaser/releases and unzip the file on the truecaser folder. You can also train your own truecaser model following the instructions provided in https://github.com/nreimers/truecaser.

-----------------------------------------------------------------------
**How to run**

`python __main__.py examples`

The path for the Stanford CoreNLP tool should be changed in simpatico_ss/util.py before use.
The systems also expect a file called 'english_distributions.obj' in the truecaser folder. Please use the instructions in External Resources/Tool section.

-----------------------------------------------------------------------
**References**
Siddharthan, A. (2004): Syntactic Simplification and Text Cohesion. PhD Thesis, November 2003 OR Technical Report TR-597, University of Cambridge, August 2004. 
Siddharthan, A. and  Mandya, A. (2014): Hybrid text simplification using synchronous dependency grammars with hand-written and automatically harvested rules. Proceedings of the 14th Conference of the European Chapter of the Association for Computational Linguistics (EACL 2014), Gothenburg, Sweden. 
