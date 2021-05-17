
## Webservices for EstNLTK's `StanzaSyntaxTagger` and `StanzaSyntaxEnsembleTagger`

### Required models

The folder `stanza_resources` contains models required by EstNLTK's `StanzaSyntaxTagger` and `StanzaSyntaxEnsembleTagger`. Models with small size are already included in this repository, but larger models must be downloaded separately, see `stanza_resources/readme.md` for details. After all necessary models have been downloaded, the folder structure of models should look like this:


	└── stanza_resources
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


### Configuration

The configuration follows the configuration used in [https://github.com/liisaratsep/berttaggernazgul](https://github.com/liisaratsep/berttaggernazgul). 

The Docker image can be built with 3 configurations that can be defined by a build argument `NAURON_MODE`. By default, the image contains a Gunicorn + Flask API running `StanzaSyntaxTagger` and `StanzaSyntaxEnsembleTagger`. The `GATEWAY` configuration creates an image that only contains the API which posts requests to a RabbitMQ message queue server. The `WORKER` configuration creates a worker that picks up requests from the message queue and processes them.

The RabbitMQ server configuration can be defined with environment variables `MQ_HOST`, `MQ_PORT`, `MQ_USERNAME` and
 `MQ_PASSWORD`. The web server can be configured with the default Gunicorn parameters by using the `GUNICORN_` prefix.

Docker compose configuration to run separate a gateway and worker containers with RabbitMQ: 

TODO


### Quick testing of the webservice

To quickly test if the webservice has been set up properly and appears to run OK, try the following `curl` query:

	curl http://127.0.0.1:5000/estnltk/tagger/stanza_syntax -H "Content-Type: application/json" -d '{"text": "Eriti kaval kääbik", "meta": {}, "layers": "{\"sentences\": {\"name\": \"sentences\", \"attributes\": [], \"parent\": null, \"enveloping\": \"words\", \"ambiguous\": false, \"serialisation_module\": null, \"meta\": {}, \"spans\": [{\"base_span\": [[0, 5], [6, 11], [12, 18]], \"annotations\": [{}]}]}, \"compound_tokens\": {\"name\": \"compound_tokens\", \"attributes\": [\"type\", \"normalized\"], \"parent\": null, \"enveloping\": \"tokens\", \"ambiguous\": false, \"serialisation_module\": null, \"meta\": {}, \"spans\": []}, \"tokens\": {\"name\": \"tokens\", \"attributes\": [], \"parent\": null, \"enveloping\": null, \"ambiguous\": false, \"serialisation_module\": null, \"meta\": {}, \"spans\": [{\"base_span\": [0, 5], \"annotations\": [{}]}, {\"base_span\": [6, 11], \"annotations\": [{}]}, {\"base_span\": [12, 18], \"annotations\": [{}]}]}, \"morph_extended\": {\"name\": \"morph_extended\", \"attributes\": [\"normalized_text\", \"lemma\", \"root\", \"root_tokens\", \"ending\", \"clitic\", \"form\", \"partofspeech\", \"punctuation_type\", \"pronoun_type\", \"letter_case\", \"fin\", \"verb_extension_suffix\", \"subcat\"], \"parent\": \"morph_analysis\", \"enveloping\": null, \"ambiguous\": true, \"serialisation_module\": null, \"meta\": {}, \"spans\": [{\"base_span\": [0, 5], \"annotations\": [{\"normalized_text\": \"Eriti\", \"lemma\": \"eriti\", \"root\": \"eriti\", \"root_tokens\": [\"eriti\"], \"ending\": \"0\", \"clitic\": \"\", \"form\": \"\", \"partofspeech\": \"D\", \"punctuation_type\": null, \"pronoun_type\": null, \"letter_case\": \"cap\", \"fin\": null, \"verb_extension_suffix\": [], \"subcat\": null}]}, {\"base_span\": [6, 11], \"annotations\": [{\"normalized_text\": \"kaval\", \"lemma\": \"kaval\", \"root\": \"kaval\", \"root_tokens\": [\"kaval\"], \"ending\": \"0\", \"clitic\": \"\", \"form\": \"pos sg nom\", \"partofspeech\": \"A\", \"punctuation_type\": null, \"pronoun_type\": null, \"letter_case\": null, \"fin\": null, \"verb_extension_suffix\": [], \"subcat\": null}]}, {\"base_span\": [12, 18], \"annotations\": [{\"normalized_text\": \"kääbik\", \"lemma\": \"kääbik\", \"root\": \"kääbik\", \"root_tokens\": [\"kääbik\"], \"ending\": \"0\", \"clitic\": \"\", \"form\": \"com sg nom\", \"partofspeech\": \"S\", \"punctuation_type\": null, \"pronoun_type\": null, \"letter_case\": null, \"fin\": null, \"verb_extension_suffix\": [], \"subcat\": null}]}]}, \"words\": {\"name\": \"words\", \"attributes\": [\"normalized_form\"], \"parent\": null, \"enveloping\": null, \"ambiguous\": true, \"serialisation_module\": null, \"meta\": {}, \"spans\": [{\"base_span\": [0, 5], \"annotations\": [{\"normalized_form\": null}]}, {\"base_span\": [6, 11], \"annotations\": [{\"normalized_form\": null}]}, {\"base_span\": [12, 18], \"annotations\": [{\"normalized_form\": null}]}]}, \"morph_analysis\": {\"name\": \"morph_analysis\", \"attributes\": [\"normalized_text\", \"lemma\", \"root\", \"root_tokens\", \"ending\", \"clitic\", \"form\", \"partofspeech\"], \"parent\": \"words\", \"enveloping\": null, \"ambiguous\": true, \"serialisation_module\": null, \"meta\": {}, \"spans\": [{\"base_span\": [0, 5], \"annotations\": [{\"normalized_text\": \"Eriti\", \"lemma\": \"eriti\", \"root\": \"eriti\", \"root_tokens\": [\"eriti\"], \"ending\": \"0\", \"clitic\": \"\", \"form\": \"\", \"partofspeech\": \"D\"}]}, {\"base_span\": [6, 11], \"annotations\": [{\"normalized_text\": \"kaval\", \"lemma\": \"kaval\", \"root\": \"kaval\", \"root_tokens\": [\"kaval\"], \"ending\": \"0\", \"clitic\": \"\", \"form\": \"sg n\", \"partofspeech\": \"A\"}]}, {\"base_span\": [12, 18], \"annotations\": [{\"normalized_text\": \"kääbik\", \"lemma\": \"kääbik\", \"root\": \"kääbik\", \"root_tokens\": [\"kääbik\"], \"ending\": \"0\", \"clitic\": \"\", \"form\": \"sg n\", \"partofspeech\": \"S\"}]}]}}", "output_layer": "stanza_syntax"}'

Expected result:

    {"ambiguous":false,"attributes":["id","lemma","upostag","xpostag","feats","head","deprel","deps","misc"],"enveloping":null,"meta":{},"name":"stanza_syntax","parent":"morph_analysis","serialisation_module":null,"spans":[{"annotations":[{"deprel":"advmod","deps":"_","feats":{},"head":2,"id":1,"lemma":"eriti","misc":"_","upostag":"D","xpostag":"D"}],"base_span":[0,5]},{"annotations":[{"deprel":"amod","deps":"_","feats":{"n":"n","sg":"sg"},"head":3,"id":2,"lemma":"kaval","misc":"_","upostag":"A","xpostag":"A"}],"base_span":[6,11]},{"annotations":[{"deprel":"root","deps":"_","feats":{"n":"n","sg":"sg"},"head":0,"id":3,"lemma":"k\u00e4\u00e4bik","misc":"_","upostag":"S","xpostag":"S"}],"base_span":[12,18]}]}

