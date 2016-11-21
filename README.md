# simpatico_ss
Syntactic Simplification for the SIMPATICO project.

This system implements the syntactic simplification rules proposed by Siddharthan (2004).
Our implementation uses the Stanford Dependency Parser available at NLTK. 

-----------------------------------------------------------------------
**First Release**

This release deals with the simplification of conjoint clauses, relative clauses and appositive phrases.
Simplifications are made according to the parser tree output, given priority to the relations that are in the top of the tree.
Sentences are simplified recursively until there is nothing more to be simplified.

The generation phase is still working as part of the transformation phase.

-----------------------------------------------------------------------
**How to run**

`python __main__.py examples`

-----------------------------------------------------------------------

Siddharthan, A. (2004): Syntactic Simplification and Text Cohesion. PhD Thesis, November 2003 OR Technical Report TR-597, University of Cambridge, August 2004. 
