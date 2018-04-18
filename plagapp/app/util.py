from app import app
import os
import glob
import sys

sys.path.append(app.config['PLAGCOMPS_LOC'])

from plagcomps.shared.util import IntrinsicUtility

def get_file_options():
    static_file_loc = os.path.join(app.config['APP_ROOT'], 'static/sample_docs')
    sample_corpus_loc = os.path.join(app.config['PLAGCOMPS_LOC'], 'plagcomps/sample_corpus')

    # Grab document options from both the plagapp static sample docs
    # and the sample corpus directory in the plagcomps repo
    local_file_options = glob.glob(static_file_loc + '/*.txt')
    sample_corpus_options = glob.glob(sample_corpus_loc + '/*.txt')
    file_options = [os.path.basename(f) for f in local_file_options + sample_corpus_options]
    without_extensions = [os.path.splitext(f)[0] for f in file_options]

    full_paths = [os.path.join(static_file_loc, f) for f in local_file_options] + \
                 [os.path.join(sample_corpus_loc, f) for f in sample_corpus_options]

    # If on the comps machine, also grab the full training set of corpus
    training_rel_paths, training_full_paths = get_training_set_files()
    without_extensions += training_rel_paths
    full_paths += training_full_paths

    return full_paths, without_extensions


def get_training_set_files():
    util = IntrinsicUtility()
    full_paths = util.get_n_training_files()
    relative_paths = util.get_relative_training_set(IntrinsicUtility.TRAINING_LOC)
    # Strip leading '/' and remove '/'s to prepare for URL
    relative_paths = [r[1:].replace('/', '-') for r in relative_paths]

    return relative_paths, full_paths


def get_file_short_names():
    full_paths, file_names = get_file_options()
    return list(zip(file_names, file_names))

def get_file_to_full_paths():
    full_paths, file_names = get_file_options()

    return {name : full for name, full in zip(file_names, full_paths)}


def get_sent_feature_options():
    options = [
        #'average_word_length'

        'stopword_percentage',
        'punctuation_percentage',
        'syntactic_complexity',
        'avg_internal_word_freq_class',
        'avg_external_word_freq_class',
        'yule_k_characteristic',
        'average_syllables_per_word',
        'simpsons_d',
        'sichels_s',
        'brunets_w',
        'hapax_legomena',
        'hapax_dislegomena',
        'yule_i',
        'dale_chall_readability_score',
        'polysyllablcount',
        'smog_index',
        'average_letter_per_word',
        'coleman_liau_index',
        'automated_readability_index',
        'linsear_write_formula',
        'gunning_fog_index',
        'honore_r_measure',
        'flesch_reading_ease',
        'flesch_kincaid_grade',
    ]

    return list(zip(options, options))

def get_word_feature_options():
    options = [
        'avg_internal_word_freq_class',
        'avg_external_word_freq_class',
    ]

    return list(zip(options, options))

def get_para_feature_options():
    options = [
        #'average_word_length'
        'stopword_percentage',
        'punctuation_percentage',
        'syntactic_complexity',
        'avg_internal_word_freq_class',
        'avg_external_word_freq_class',
        'yule_k_characteristic',
        'average_syllables_per_word',
        'simpsons_d',
        'sichels_s',
        'brunets_w',
        'hapax_legomena',
        'hapax_dislegomena',
        'yule_i',
        'dale_chall_readability_score',
        'polysyllablcount',
        'smog_index',
        'average_letter_per_word',
        'coleman_liau_index',
        'automated_readability_index',
        'linsear_write_formula',
        'gunning_fog_index',
        'honore_r_measure',
        'flesch_reading_ease',
        'flesch_kincaid_grade',
    ]

    return list(zip(options, options))

def get_atom_options():
    options = [
        'paragraph',
        'sentence',
        'word'
    ]

    return list(zip(options, options))

def get_cluster_options():
    options = [
        'kmeans',
        'agglom',
        'hmm',
        'none',
        'cos'
    ]

    return list(zip(options, options))


def get_similarity_options():
    options = [
        'euclidean',
        'cosine',
        'correlation',
        'cityblock',
        'chebyshev'
    ]

    return list(zip(options, options))
