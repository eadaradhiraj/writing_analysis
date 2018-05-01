# Import the actual Flask app
from app import app
from flask import render_template, redirect, jsonify, request, url_for
import sys
import os, csv, json

from .forms import PlagSelection
from .plag_detector import PlagDetector
from .util import *


sample_corpus_loc = os.path.join(app.config['PLAGCOMPS_LOC'], 'plagcomps/sample_corpus')

@app.route('/index/')
@app.route('/')
def main_page():
    return render_template('index.html')

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/select_doc/')
def select_doc():
    return render_template('select_doc.html',
                    docs = get_file_short_names(), para_features = get_para_feature_options(), sent_features=get_sent_feature_options(), word_features = get_word_feature_options(),cluster_methods = get_cluster_options(), atom_options = get_atom_options())#, similarity_measures = get_similarity_options())

@app.route('/view_doc')
def view_doc():
    doc_name = request.args.get('doc')
    file_to_full_path = get_file_to_full_paths()
    if doc_name in file_to_full_path:
        full_path = file_to_full_path[doc_name]
    else:
        # TODO Make a nice error msg
        return 'some error'

    atom_type = request.args.get('atom')
    features = request.args.getlist('features')
    cluster_method = request.args.get('cluster_method')
    k = int(request.args.get('k'))

    all_passages = PlagDetector().get_passages(atom_type, features, cluster_method, k, full_path)
    feature_names = list(all_passages[0].features.keys())
    title = {"text": str(doc_name)}
    plag_cats =[str(passage.plag_spans[0][0]) for passage in all_passages if passage.plag_spans]
    data_d3_chart = [{"idx": passage.char_index_start, "conf": passage.plag_confidence} for passage in all_passages]

    return render_template('view_doc.html',
        atom_type = atom_type,
        cluster_method = cluster_method,
        k = k,
        passages = all_passages,
        features = feature_names,
        doc_name = doc_name,
        title=title,
        plag_cats=plag_cats, 
        data_d3_chart = data_d3_chart)
    

#@app.route('/view_source_doc/<doc_name>', methods=['GET'])
#def view_source_doc(doc_name):
@app.route('/test_source_doc')
def view_source_doc():
    full_path = os.path.join(app.config['APP_ROOT'], 'static/sample_docs/test2.txt')
    xml_path = os.path.join(app.config['APP_ROOT'], 'static/sample_docs/test2.xml')

    atom_type = 'paragraph'

    passages = PlagDetector().get_ground_truth_passages(atom_type, full_path, xml_path)
    
    return render_template('view_source_doc.html',
        passages = passages,
        atom_type = atom_type)


@app.route('/sample/')
def show_sample():
    '''
    Use a pickled file of passage objects parsed from static/training_sample.txt
    to sample the front-end
    '''
    #all_passages = PlagDetector().get_passages('pickle')
    all_passages = PlagDetector().get_passages()
    features = list(all_passages[0].features.keys())

    return render_template('view_doc.html',
        doc_name = 'Sample',
        passages = all_passages,
        features = features)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug = True, port=port)
