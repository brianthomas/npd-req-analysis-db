'''

Simple little script to take text from requirements and use it
to create a model of significant terms (a dictionary) 
to support term (keyword) extraction from text.

Created on June 6, 2017

@author: thomas
'''

# the minimum number of times a term must occur in training corpus
# before its considered significant enough to include in the model
# dictionary
MIN_TERM_OCCUR = 1

import logging
logging.basicConfig(level=logging.WARN)
logging.getLogger('gensim.models.phrases').setLevel(logging.WARN)

def createTermDictionaryFromText (inputfile, output_dict_model, min_term_occur):
    
    import codecs
    from nltk.corpus import stopwords
    from npd.textmining import EnglishStemmer, DocTextProcessor
    import npd.parser as parser
    from ocio.textmining.extraction import UnstructuredTextTermExtractor
    
    print ("Training using file: "+inputfile+" with minimum term threshold:"+str(min_term_occur))

    print (" * Parsing requirements file")
    # obtain our corpus, based on content of requirements
    corpus = [ req['content'] for req in parser.parse(inputfile)] 

    all_stopwords = set(stopwords.words('english'))

    more_stopwords = {'all', 'came', 'come', 'have', 'like', 'may', 'would', 'yet', 'us', 'upon', 'will', 'would' }
    for word in more_stopwords: all_stopwords.add(word)

    print (" * Creating trained model from text")
    dict_model = UnstructuredTextTermExtractor.train( corpus, 
                                                      stop_words=all_stopwords,
                                                      preprocess_text_tool=DocTextProcessor(),
                                                      stemming_tool=EnglishStemmer(),
                                                      min_term_count=min_term_occur,
                                                      preserve_case=True,
                                                    )
    
    print (" * Writing pickled output to file:"+ output_dict_model)
    dict_model.save(output_dict_model)

    print (" * Finished")

if __name__ == '__main__':
    import argparse
    ''' Run the application '''
    
    # Use nargs to specify how many arguments an option should take.
    ap = argparse.ArgumentParser(description='OpenData training Appliance -- creates term model (dictionary) from opengov json formatted data.')
    ap.add_argument('-i', '--input', type=str, help='Input xlsm to pull content from')
    ap.add_argument('-m', '--output_dict_model', type=str, help='Output model file to write to (in pickled form)')
    ap.add_argument('-mt', '--min_term_threshold', type=int, default=MIN_TERM_OCCUR, help='Minimum number of times term must occur in training to be included in the model dictionary ')
   
    # parse argv
    opts = ap.parse_args()
    
    if not opts.input:
        print ("the --input <file> parameter must be specified")
        ap.print_usage()
        exit()
        
    if not opts.output_dict_model:
        print ("the --output_dict_model <file> parameter must be specified")
        ap.print_usage()
        exit()
    
    createTermDictionaryFromText(opts.input, opts.output_dict_model, opts.min_term_threshold)
    
    
    
