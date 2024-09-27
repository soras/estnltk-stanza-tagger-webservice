This folder contains models for EstNLTK's StanzaSyntaxTagger and StanzaSyntaxEnsembleTagger.

You can download the latest models from: [`https://s3.hpc.ut.ee/estnltk/estnltk_resources/stanza_syntax_2023-01-21.zip`](https://s3.hpc.ut.ee/estnltk/estnltk_resources/stanza_syntax_2023-01-21.zip) 

Unpack the content of `/stanza_syntax/models_2023-01-21` into this folder, so that the structure of this folder looks like this:

	    ├── et
	    │   ├── depparse
	    │   │   ├── ensemble_models
	    │   │   │   ├── model_10.pt
	    │   │   │   ├── model_1.pt
	    │   │   │   ├── model_2.pt
	    │   │   │   ├── model_3.pt
	    │   │   │   ├── model_4.pt
	    │   │   │   ├── model_5.pt
	    │   │   │   ├── model_6.pt
	    │   │   │   ├── model_7.pt
	    │   │   │   ├── model_8.pt
	    │   │   │   └── model_9.pt
	    │   │   ├── edt.pt
	    │   │   ├── morph_analysis.pt
	    │   │   ├── morph_extended.pt
	    │   │   └── stanza_depparse.pt
	    │   ├── lemma
	    │   │   └── edt.pt
	    │   ├── pos
	    │   │   └── edt.pt
	    │   ├── pretrain
	    │   │   └── edt.pt
	    │   └── tokenize
	    │       └── edt.pt
	    ├── readme.md
	    └── resources.json


