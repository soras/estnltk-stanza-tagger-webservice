
# Webservices for EstNLTK's Stanza-based Syntax Taggers

This is a web service for EstNLTK's Stanza-based syntax taggers. The service is based on FastAPI and should be run as a Docker container using the included `Dockerfile`. The required models are automatically downloaded upon building the image.

The API uses the following endpoints:

- `POST /estnltk/tagger/stanza_syntax` - the main endpoint for obtaining Stanza-based syntax annotations
- `GET /estnltk/tagger/stanza_syntax/about` - returns information about the webservice
- `GET /estnltk/tagger/stanza_syntax/status` - returns the status of the webservice
- `POST /estnltk/tagger/stanza_syntax_ensemble` - the main endpoint for obtaining Stanza-based syntax annotations using ensemble models
- `GET /estnltk/tagger/stanza_syntax_ensemble/about` - returns information about the webservice
- `GET /estnltk/tagger/stanza_syntax_ensemble/status` - returns the status of the webservice

## Configuration

The service should be run as a Docker container using the included `Dockerfile`. The API is exposed on port `8000`. The following environment variables can be used to change webservice behavior:

- `STANZE_MODELS_DIR` - path to stanza's models directory (`stanza_resources` by default).
- `MAX_CONTENT_LENGHT` - maximum lenght of the POST request body size in characters.

The container uses uvicorn as the ASGI server. The entrypoint of the container is `["uvicorn", "app:app", "--host", "0.0.0.0", "--proxy-headers"]`. Any additional  [uvicorn parameters](https://uvicorn.dev/deployment/) can be passed to the container at runtime as CMD arguments.

## Required models

When using the web service without Docker, the models should be obtained as described below. Models with small size are already included in this repository, but larger models must be downloaded separately, see `stanza_resources/readme.md` for details. After all necessary models have been downloaded, the folder structure of models should look like this:

```text
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
```

## Quick testing of the webservice

To quickly test if the webservice has been set up properly and appears to run OK, try the following `curl` query:

```shell
curl http://127.0.0.1:5000/estnltk/tagger/stanza_syntax -H "Content-Type: application/json" -d '{"text": "Eriti kaval kääbik", "meta": {}, "layers": "{\"sentences\": {\"name\": \"sentences\", \"attributes\": [], \"parent\": null, \"enveloping\": \"words\", \"ambiguous\": false, \"serialisation_module\": null, \"meta\": {}, \"spans\": [{\"base_span\": [[0, 5], [6, 11], [12, 18]], \"annotations\": [{}]}]}, \"compound_tokens\": {\"name\": \"compound_tokens\", \"attributes\": [\"type\", \"normalized\"], \"parent\": null, \"enveloping\": \"tokens\", \"ambiguous\": false, \"serialisation_module\": null, \"meta\": {}, \"spans\": []}, \"tokens\": {\"name\": \"tokens\", \"attributes\": [], \"parent\": null, \"enveloping\": null, \"ambiguous\": false, \"serialisation_module\": null, \"meta\": {}, \"spans\": [{\"base_span\": [0, 5], \"annotations\": [{}]}, {\"base_span\": [6, 11], \"annotations\": [{}]}, {\"base_span\": [12, 18], \"annotations\": [{}]}]}, \"morph_extended\": {\"name\": \"morph_extended\", \"attributes\": [\"normalized_text\", \"lemma\", \"root\", \"root_tokens\", \"ending\", \"clitic\", \"form\", \"partofspeech\", \"punctuation_type\", \"pronoun_type\", \"letter_case\", \"fin\", \"verb_extension_suffix\", \"subcat\"], \"parent\": \"morph_analysis\", \"enveloping\": null, \"ambiguous\": true, \"serialisation_module\": null, \"meta\": {}, \"spans\": [{\"base_span\": [0, 5], \"annotations\": [{\"normalized_text\": \"Eriti\", \"lemma\": \"eriti\", \"root\": \"eriti\", \"root_tokens\": [\"eriti\"], \"ending\": \"0\", \"clitic\": \"\", \"form\": \"\", \"partofspeech\": \"D\", \"punctuation_type\": null, \"pronoun_type\": null, \"letter_case\": \"cap\", \"fin\": null, \"verb_extension_suffix\": [], \"subcat\": null}]}, {\"base_span\": [6, 11], \"annotations\": [{\"normalized_text\": \"kaval\", \"lemma\": \"kaval\", \"root\": \"kaval\", \"root_tokens\": [\"kaval\"], \"ending\": \"0\", \"clitic\": \"\", \"form\": \"pos sg nom\", \"partofspeech\": \"A\", \"punctuation_type\": null, \"pronoun_type\": null, \"letter_case\": null, \"fin\": null, \"verb_extension_suffix\": [], \"subcat\": null}]}, {\"base_span\": [12, 18], \"annotations\": [{\"normalized_text\": \"kääbik\", \"lemma\": \"kääbik\", \"root\": \"kääbik\", \"root_tokens\": [\"kääbik\"], \"ending\": \"0\", \"clitic\": \"\", \"form\": \"com sg nom\", \"partofspeech\": \"S\", \"punctuation_type\": null, \"pronoun_type\": null, \"letter_case\": null, \"fin\": null, \"verb_extension_suffix\": [], \"subcat\": null}]}]}, \"words\": {\"name\": \"words\", \"attributes\": [\"normalized_form\"], \"parent\": null, \"enveloping\": null, \"ambiguous\": true, \"serialisation_module\": null, \"meta\": {}, \"spans\": [{\"base_span\": [0, 5], \"annotations\": [{\"normalized_form\": null}]}, {\"base_span\": [6, 11], \"annotations\": [{\"normalized_form\": null}]}, {\"base_span\": [12, 18], \"annotations\": [{\"normalized_form\": null}]}]}, \"morph_analysis\": {\"name\": \"morph_analysis\", \"attributes\": [\"normalized_text\", \"lemma\", \"root\", \"root_tokens\", \"ending\", \"clitic\", \"form\", \"partofspeech\"], \"parent\": \"words\", \"enveloping\": null, \"ambiguous\": true, \"serialisation_module\": null, \"meta\": {}, \"spans\": [{\"base_span\": [0, 5], \"annotations\": [{\"normalized_text\": \"Eriti\", \"lemma\": \"eriti\", \"root\": \"eriti\", \"root_tokens\": [\"eriti\"], \"ending\": \"0\", \"clitic\": \"\", \"form\": \"\", \"partofspeech\": \"D\"}]}, {\"base_span\": [6, 11], \"annotations\": [{\"normalized_text\": \"kaval\", \"lemma\": \"kaval\", \"root\": \"kaval\", \"root_tokens\": [\"kaval\"], \"ending\": \"0\", \"clitic\": \"\", \"form\": \"sg n\", \"partofspeech\": \"A\"}]}, {\"base_span\": [12, 18], \"annotations\": [{\"normalized_text\": \"kääbik\", \"lemma\": \"kääbik\", \"root\": \"kääbik\", \"root_tokens\": [\"kääbik\"], \"ending\": \"0\", \"clitic\": \"\", \"form\": \"sg n\", \"partofspeech\": \"S\"}]}]}}", "output_layer": "stanza_syntax"}'
```

Expected result:

```json
{"ambiguous":false,"attributes":["id","lemma","upostag","xpostag","feats","head","deprel","deps","misc"],"enveloping":null,"meta":{},"name":"stanza_syntax","parent":"morph_extended","serialisation_module":null,"spans":[{"annotations":[{"deprel":"advmod","deps":"_","feats":{},"head":2,"id":1,"lemma":"eriti","misc":"_","upostag":"D","xpostag":"D"}],"base_span":[0,5]},{"annotations":[{"deprel":"amod","deps":"_","feats":{"nom":"nom","pos":"pos","sg":"sg"},"head":3,"id":2,"lemma":"kaval","misc":"_","upostag":"A","xpostag":"A"}],"base_span":[6,11]},{"annotations":[{"deprel":"root","deps":"_","feats":{"com":"com","nom":"nom","sg":"sg"},"head":0,"id":3,"lemma":"k\u00e4\u00e4bik","misc":"_","upostag":"S","xpostag":"S"}],"base_span":[12,18]}]}
```
