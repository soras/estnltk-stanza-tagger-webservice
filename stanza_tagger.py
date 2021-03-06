#
#  Original source:
#   https://github.com/estnltk/estnltk/blob/b9e121ac4da34757656f93636de83a1186f21ac9/estnltk/taggers/syntax/stanza_tagger/stanza_tagger.py
#
#  Modifications to the original code:
#  *) Removed SyntaxDependencyRetagger (flag add_parent_and_children), 
#     DeprelAgreementRetagger (flag mark_agreement_error) and 
#     UDValidationRetagger (flag mark_syntax_error) -- these
#     steps are optional and can be applied on the layer later;
#
#  *) Removed global variable RESOURCES: the location of the resources 
#     folder now needs to be specified via input argument dir;
#

import os
from random import Random
from collections import OrderedDict

import stanza
from estnltk.layer.layer import Layer
from estnltk.taggers.tagger import Tagger
from stanza.models.common.doc import Document


class StanzaSyntaxTagger(Tagger):
    """
    Tags dependency syntactic analysis with Stanza.
    The tagger assumes that the segmentation to sentences and words is completed before. Morphological analysis
    can be used, too.

    The tagger assumes that morph analysis is completed with VabaMorf module and follows EstMorph tagset.
    For using extended analysis, basic morph analysis layer must first exist.

    The tagger creates a syntax layer that features Universal Dependencies dependency-tags in attribute 'deprel'.
    When using only sentences for prediction, features and UPOS-tags from UD-tagset are used and displayed.
    Otherwise UPOS is the same as VabaMorf's part of speech tag and feats is based on VabaMorf's forms.

    An optional input_type flag allows choosing layer type to use as the base of prediction. Default is 'morph_analysis',
    which expects 'morph_analysis' as input. Values 'morph_extended' and 'sentences' can also be chosen. When using
    one of the morphological layers, the name of the morphological layer to use must be declared in input_morph_layer
    parameter (default 'morph_analysis').

    Names of layers to use can be changed using parameters sentences_layer, words_layer and input_morph_layer,
    if needed. To use GPU for parsing, parameter use_gpu must be set to True.
    Parameter add_parents_and_children adds attributes that contain the parent and children of a word.
    Tutorial:
    """

    conf_param = ['model_path', 'model_name', 'add_parent_and_children', 'syntax_dependency_retagger',
                  'input_type', 'dir', 'mark_syntax_error', 'mark_agreement_error', 'agreement_error_retagger',
                  'ud_validation_retagger', 'use_gpu', 'nlp']

    def __init__(self,
                 output_layer='stanza_syntax',
                 sentences_layer='sentences',
                 words_layer='words',
                 input_morph_layer='morph_analysis', # or 'morph_extended' if input_type='morph_extended'
                 input_type='morph_analysis',  # or 'morph_extended', 'sentences'
                 add_parent_and_children=False,
                 depparse_path=None,
                 mark_syntax_error=False,
                 mark_agreement_error=False,
                 use_gpu=False,
                 dir='stanza_resources',
                 ):

        self.add_parent_and_children = add_parent_and_children
        self.mark_syntax_error = mark_syntax_error
        self.mark_agreement_error = mark_agreement_error
        self.output_layer = output_layer
        self.output_attributes = ('id', 'lemma', 'upostag', 'xpostag', 'feats', 'head', 'deprel', 'deps', 'misc')
        self.input_type = input_type
        self.dir = dir
        self.use_gpu = use_gpu

        if add_parent_and_children:
            #self.syntax_dependency_retagger = SyntaxDependencyRetagger(conll_syntax_layer=output_layer)
            #self.output_attributes += ('parent_span', 'children')
            raise NotImplementedError('Applying SyntaxDependencyRetagger is not supported in the web service.')

        if mark_syntax_error:
            #self.ud_validation_retagger = UDValidationRetagger(output_layer=output_layer)
            #self.output_attributes += ('syntax_error', 'error_message')
            raise NotImplementedError('Applying UDValidationRetagger is not supported in the web service.')

        if mark_agreement_error:
            if not add_parent_and_children:
                raise ValueError('`add_parent_and_children` must be True for marking agreement errors.')
            else:
                #self.agreement_error_retagger = DeprelAgreementRetagger(output_layer=output_layer)
                #self.output_attributes += ('agreement_deprel',)
                raise NotImplementedError('Applying DeprelAgreementRetagger is not supported in the web service.')

        if self.input_type not in ['sentences', 'morph_analysis', 'morph_extended']:
            raise ValueError('Invalid input type {}'.format(input_type))

        if depparse_path and not os.path.isfile(depparse_path):
            raise ValueError('Invalid path: {}'.format(depparse_path))
        elif depparse_path and os.path.isfile(depparse_path):
            self.model_path = depparse_path
        else:
            if input_type == 'morph_analysis':
                self.model_path = os.path.join(dir, 'et', 'depparse', 'morph_analysis.pt')
            if input_type == 'morph_extended':
                self.model_path = os.path.join(dir, 'et', 'depparse', 'morph_extended.pt')
            if input_type == 'sentences':
                self.model_path = os.path.join(dir, 'et', 'depparse', 'stanza_depparse.pt')

        if not os.path.isfile(self.model_path):
            raise FileNotFoundError('Necessary models missing, download from https://entu.keeleressursid.ee/public-document/entity-9791 '
                             'and extract folders `depparse` and `pretrain` to root directory defining '
                             'StanzaSyntaxTagger under the subdirectory `stanza_resources/et`')

        if input_type == 'sentences':
            if not os.path.isfile(os.path.join(dir, 'et', 'pretrain', 'edt.pt')):
                raise FileNotFoundError(
                    'Necessary pretrain model missing, download from https://entu.keeleressursid.ee/public-document/entity-9791 '
                    'and extract folder `pretrain` to root directory defining '
                    'StanzaSyntaxTagger under the subdirectory `stanza_resources/et`')

        if self.input_type == 'sentences':
            self.input_layers = [sentences_layer, words_layer]
            self.nlp = stanza.Pipeline(lang='et', processors='tokenize,pos,lemma,depparse',
                                       dir=self.dir,
                                       tokenize_pretokenized=True,
                                       depparse_model_path=self.model_path,
                                       use_gpu=self.use_gpu,
                                       logging_level='WARN')  # Logging level chosen so it does not display
            # information about downloading model

        elif self.input_type in ['morph_analysis', 'morph_extended']:
            self.input_layers = [sentences_layer, input_morph_layer, words_layer]
            self.nlp = stanza.Pipeline(lang='et', processors='depparse',
                                       dir=self.dir,
                                       depparse_pretagged=True,
                                       depparse_model_path=self.model_path,
                                       use_gpu=self.use_gpu,
                                       logging_level='WARN')

    def _make_layer(self, text, layers, status=None):
        rand = Random()
        rand.seed(4)

        if self.input_type in ['morph_analysis', 'morph_extended']:

            sentences_layer = layers[self.input_layers[0]]
            data = []

            for sentence in sentences_layer:
                sentence_analysis = []

                # TODO Replace sentence.__getattr__ with appropriate code
                for i, span in enumerate(sentence.__getattr__(self.input_layers[1])):
                    annotation = rand.choice(span.annotations)
                    id = i + 1
                    wordform = span.text
                    lemma = annotation['lemma']

                    feats = ''

                    if annotation['form']:
                        feats = annotation['form']

                    if not feats:
                        feats = '_'

                    else:
                        # Make and join keyed features.
                        feats = '|'.join([a + '=' + a for a in feats.strip().split(' ') if a])
                    xpos = annotation['partofspeech']  # xpos and upos have the same value
                    dict = {'id': id, 'text': wordform, 'lemma': lemma, 'feats': feats, 'upos': xpos, 'xpos': xpos}
                    sentence_analysis.append(dict)

                data.append(sentence_analysis)

            document = Document(data)

        # Stanza pipeline on pretagged tokens/sentences.
        else:
            sentences_layer = layers[self.input_layers[0]]
            document = [sentence.text for sentence in sentences_layer]

        parent_layer = layers[self.input_layers[1]]

        layer = Layer(name=self.output_layer,
                      text_object=text,
                      attributes=self.output_attributes,
                      parent=self.input_layers[1],
                      ambiguous=False,
                      )

        doc = self.nlp(document)

        extracted_data = [analysis for sentence in doc.to_dict() for analysis in sentence]

        for line, span in zip(extracted_data, parent_layer):
            id = line['id']
            lemma = line['lemma']
            upostag = line['upos']
            xpostag = line['xpos']
            feats = OrderedDict()  # Stays this way if word has no features.
            if 'feats' in line.keys():
                feats = feats_to_ordereddict(line['feats'])
            head = line['head']
            deprel = line['deprel']

            attributes = {'id': id, 'lemma': lemma, 'upostag': upostag, 'xpostag': xpostag, 'feats': feats,
                          'head': head, 'deprel': deprel, 'deps': '_', 'misc': '_'}

            layer.add_annotation(span, **attributes)

        if self.add_parent_and_children:
            # Add 'parent_span' & 'children' to the syntax layer.
            self.syntax_dependency_retagger.change_layer(text, {self.output_layer: layer})

        if self.mark_syntax_error:
            # Add 'syntax_error' & 'error_message' to the layer.
            self.ud_validation_retagger.change_layer(text, {self.output_layer: layer})

        if self.mark_agreement_error:
            # Add 'agreement_deprel' to the layer.
            self.agreement_error_retagger.change_layer(text, {self.output_layer: layer})

        return layer


def feats_to_ordereddict(feats_str):
    """
    Converts feats string to OrderedDict (as in MaltParserTagger and UDPipeTagger)
    """
    feats = OrderedDict()
    if feats_str == '_':
        return feats
    feature_pairs = feats_str.split('|')
    for feature_pair in feature_pairs:
        key, value = feature_pair.split('=')
        feats[key] = value
    return feats
