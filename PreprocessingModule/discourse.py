filepath = "../ASRModule/Transcripts/"  # Transcript path

from allennlp.predictors.predictor import Predictor
import sys

model_url = "https://storage.googleapis.com/allennlp-public-models/coref-spanbert-large-2020.02.27.tar.gz"
predictor = Predictor.from_path(model_url)
def main():
    text_filename = sys.argv[1]
    final_filepath = filepath + text_filename
    text = open(final_filepath, "r").read()
    write_transcripts(final_filepath, coref_resolved(text))  # Resolved text

def coref_resolved(document: str) -> str:
    spacy_document = predictor._spacy(document)  # spaCy Doc
    clusters = predictor.predict(document).get("clusters")
    return replace_corefs(spacy_document, clusters)

def replace_corefs(document, clusters) -> str:
    resolved = list(tok.text_with_ws for tok in document)
    all_spans = [span for cluster in clusters for span in cluster]  # Flattened list of all spans
    for cluster in clusters:
        noun_indices = get_span_noun_indices(document, cluster)  # Get array of indices of (NOUN or PROPNOUN) in each cluster
        if noun_indices:
            mention_span, mention = get_cluster_head(document, cluster, noun_indices)  # Get head span and its (start, end) = first (NOUN or PROPNOUN) found
            for coref in cluster:
                # We don't want to replace the head itself && coref does not contain other spans (nested mentions)
                if coref != mention and not is_containing_other_spans(coref, all_spans):
                    core_logic_part(document, coref, resolved, mention_span)
    return "".join(resolved)

def get_span_noun_indices(document, cluster):
    spans = [document[span[0]:span[1]+1] for span in cluster]  # Get array of total spans
    spans_pos = [[token.pos_ for token in span] for span in spans]   # Get parts-of-speech (POS) tag for each span
    
    # span_noun_indices = list of indices of spans_pos arrays IF spans_pos array contains at least 1 NOUN or PROPNOUN
    # IF condition is executed for each spans_pos array
    span_noun_indices = [i for i, span_pos in enumerate(spans_pos) 
        if any(pos in span_pos for pos in ['NOUN', 'PROPN'])]

    return span_noun_indices

def get_cluster_head(document, cluster, noun_indices):
    head_idx = noun_indices[0]
    head_start, head_end = cluster[head_idx]
    head_span = document[head_start:head_end+1]
    return head_span, [head_start, head_end]

def is_containing_other_spans(span, all_spans):
    return any([s[0] >= span[0] and s[1] <= span[1] and s != span for s in all_spans]) 

def core_logic_part(document, coref, resolved, mention_span):
    final_token = document[coref[1]]
    if final_token.tag_ in ["PRP$", "POS"]:  # PRP$: Possessive pronoun, POS: Possessive ending 
        resolved[coref[0]] = mention_span.text + "'s" + final_token.whitespace_
    else:
        resolved[coref[0]] = mention_span.text + final_token.whitespace_
    for i in range(coref[0] + 1, coref[1] + 1):
        resolved[i] = ""
    return resolved

def write_transcripts(final_filepath, transcript):
    f= open(final_filepath,"w+")
    f.write(transcript)
    f.close()

main()