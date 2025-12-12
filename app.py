import logging
import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from estnltk_core.common import load_text_class
from estnltk_core.converters import layer_to_dict, json_to_layers

from settings import settings
from ensemble_tagger import StanzaSyntaxEnsembleTagger
from stanza_tagger import StanzaSyntaxTagger


logger = logging.getLogger(__name__)

app = FastAPI(redoc_url=None)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"]
)

Text = load_text_class()
stanza_tagger = StanzaSyntaxTagger(input_type='morph_extended', 
                                   input_morph_layer='morph_extended',
                                   dir=settings.stanza_models_dir)
ensemble_tagger = StanzaSyntaxEnsembleTagger(dir=settings.stanza_models_dir)

class Request(BaseModel):
    text: str
    meta: dict
    layers: str
    output_layer: str = None
    parameters: dict = None

@app.post('/estnltk/tagger/stanza_syntax')
def tagger_stanza_syntax(body: Request):
    if len(str(body)) > settings.max_content_length:
        raise HTTPException(status_code=413, detail="Request body too large")
    try:
        logger.debug(body)
        text = Text(body.text)
        text.meta = body.meta
        layers = json_to_layers(text, json_str=body.layers)
        for layer in Text.topological_sort(layers):
            text.add_layer(layer)
        layer = stanza_tagger.make_layer(text, layers)
        if body.output_layer is not None:
            layer.name = body.output_layer
        return layer_to_dict(layer)
    
    except ValueError as e:
        # If tagger.make_layer throws a ValueError, report about a missing layer
        raise HTTPException(status_code=400, detail='Error at input processing: {}'.format(str(e)))
    except Exception:
        raise HTTPException(status_code=500, detail='Internal error at input processing')

@app.get('/estnltk/tagger/stanza_syntax/about')
def tagger_stanza_syntax_about():
    return 'Tags dependency syntactic analysis using EstNLTK StanzaSyntaxTagger\'s webservice.'


@app.get('/estnltk/tagger/stanza_syntax/status')
def tagger_stanza_syntax_status():
    return 'OK'

#
# Endpoints for StanzaSyntaxEnsembleTaggerWorker
#

@app.post('/estnltk/tagger/stanza_syntax_ensemble')
def tagger_stanza_syntax_ensemble(body: Request):
    if len(str(body)) > settings.max_content_length:
        raise HTTPException(status_code=413, detail="Request body too large")
    try:
        logger.debug(body)
        text = Text(body.text)
        text.meta = body.meta
        layers = json_to_layers(text, json_str=body.layers)
        for layer in Text.topological_sort(layers):
            text.add_layer(layer)
        layer = ensemble_tagger.make_layer(text, layers)
        if body.output_layer is not None:
            layer.name = body.output_layer
        # No need to do layer_to_json: Response obj will handle the conversion
        return layer_to_dict(layer)
    
    except ValueError as e:
        # If tagger.make_layer throws a ValueError, report about a missing layer
        raise HTTPException(status_code=400, detail='Error at input processing: {}'.format(str(e)))
    except Exception:
        logger.exception('Internal error at input processing')
        raise HTTPException(status_code=500, detail='Internal error at input processing')

@app.get('/estnltk/tagger/stanza_syntax_ensemble/about')
def tagger_stanza_syntax_ensemble_about():
    return 'Tags dependency syntactic analysis using EstNLTK StanzaSyntaxEnsembleTagger\'s webservice.'


@app.get('/estnltk/tagger/stanza_syntax_ensemble/status')
def tagger_stanza_syntax_ensemble_status():
    return 'OK'