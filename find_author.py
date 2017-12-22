import os.path, math, re

def clean_up(str):
    ''' Return a version of string str in which all letters have been
    converted to lowercase and punctuation characters have been stripped 
    from both ends. Inner punctuation is left untouched.
    '''
    punctuation = '''!"',;:.-?)([]<>*#\n\t\r'''
    result = str.lower().strip(punctuation)
    return result

def get_words(text):
    ''' Return a structure holding all words in text
    Do not include surrounding punctuation in words (use clean_up).

    Let's define a token to be each entry of the list that you get
    from calling the string method split on a line of the file.
    
    We subsequently define a word to be a non-empty token from the file
    that isn't completely made up of punctuation.
    
    text is a non-empty list of strings each ending in \n.
    At least one line in text contains a word.
    '''
    words = []

    # To do: Complete this function's body to meet its specification.
    for line in text:
        line=line.split()
        for word in line:
            if clean_up(word).strip()=="":
                continue
            else:
                words.append(clean_up(word).strip())
    return words

def split_on_separators(original, separators):
    ''' Return a list of non-empty, non-blank strings from the original string
    determined by splitting the string on any of the separators.
    separators is a string of single-character separators.
    [hint: explore the re.split() function from the regular expression library]
    '''

    # To do: Complete this function's body to meet its specification.
    result = re.split(separators, original)
    result = [elem for elem in result if elem.strip()]
    return result

def get_sentences(text):
    ''' Return a list of sentences from text with terminating punctuation removed.
    text is guaranteed to have at least one sentence.

    Terminating punctuation is defined as !?.

    A sentence is defined as a non-empty string of non-terminating
    punctuation surrounded by terminating punctuation
    or beginning or end of file
    text is a non-empty list of strings each ending in \n.
    '''
    # Hint: convert text to a single long string
    text_as_string = ''.join(text)
    sentences = split_on_separators(text_as_string,'[!?.]')
    
    return sentences


def average_word_length(words):
    ''' Return the average length of all words. Do not
    include surrounding punctuation in words. 

    words is a non-empty list of strings containing all individual words in the file
    as returned by the get_words() function.
    '''
    # To do: Replace this function's body to meet its specification.
    total_length=0
    for word in words:
        total_length+=len(word)

    return float(total_length)/len(words)

def dict_of_words(words):
    d={}
    for word in words:
        d[word]=d.get(word,0)+1
    return d

def type_token_ratio(words):
    ''' Return the Type Token Ratio (TTR) for these words.
    TTR is the number of different words divided by the total number of words.

    words is a non-empty list of strings containing all individual words in the file
    as returned by the get_words() function.
    '''
    # To do: Replace this function's body to meet its specification.
    return float(len(dict_of_words(words)))/len(words)
                
def hapax_legomana_ratio(words):
    ''' Return the hapax_legomana ratio for these words.
    This ratio is the number of words that occur exactly once divided
    by the total number of words.

    words is a non-empty list of strings containing all individual words in the file
    as returned by the get_words() function.
    '''
    
    # To do: Replace this function's body to meet its specification.
    unique_words=0
    for key, value in dict_of_words(words).iteritems():
        if value==1:
            unique_words+=1
    return float(unique_words)/len(words)
              
    
def average_sentence_length(sentences):
    ''' Return the average number of words per sentence in sentences.
    Sentences consist of non-empty strings of non-terminating
    punctuation (.?!), as returned by the get_sentences() function
    
    To calculate average sentence length, you need to get the number 
    of words per sentence
    [hint: see if you can reuse get_words() here] 
    '''
    # Solution 
    return float(len(get_words(sentences))) / len(sentences)  
    

def avg_sentence_complexity(sentences):
    '''Return the average number of phrases per sentence.
    Sentences consist of non-empty strings of non-terminating
    punctuation (.?!), as returned by the get_sentences() function
    
    Phrases are then substrings of a sentence separated by
    one or more of the following delimiters ':;,'
    '''
    # To do: Replace this function's body to meet its specification.
    phrases=[]
    for sentence in sentences:
        phrases+=split_on_separators(sentence,'[:;,]')
    return float(len(phrases))/len(sentences)

def get_text_from_valid_file(prompt):
    '''Use prompt (a string) to ask the user to type the name of a file.
    Keep asking until they give a valid filename.

    When a valid filename is supplied, use variable text to store a list 
    containing all lines in the file.
    (Hint: readlines() gives us a list of strings one for each line of the file)
    The function should return both text and the valid filename
    '''
    text = []
    
    # To do: Complete this function's body to meet its specification.
    mystery_dir = 'mystery'
    while True:
        try:
            filename = raw_input(prompt)
            with open("%s/%s" % (mystery_dir, filename)) as f:
                text=f.readlines()
            break
        except:
            print "Please type a valid filename. Ensure the file is located in the folder 'mystery'\n"
    
    return text, filename

 
def compare_signatures(sig1, sig2, weight):
    '''Return a non-negative real number indicating the similarity of two 
    linguistic signatures. The smaller the number the more similar the 
    signatures. Zero indicates identical signatures.
    
    sig1 and sig2 are 5-element lists with the following elements
    0  : average word length (float)
    1  : TTR (float)
    2  : Hapax Legomana Ratio (float)
    3  : average sentence length (float)
    4  : average sentence complexity (float)

    weight is a list of multiplicative weights to apply to each
    linguistic feature.
    '''
    result = 0.0

    # Solution:

    for i in range(5):
        result += math.fabs(sig1[i]-sig2[i]) * weight[i]
    return result

def read_signature(filename):
    '''Read a linguistic signature from filename and return it as 
    list of features.
    '''

    # Solution
    
    file = open(filename, 'r')
    # the first feature is a string so it doesn't need casting to float
    result = [file.readline()]
    # all remaining features are real numbers
    for line in file:
        result.append(float(line.strip()))
    return result


if __name__ == '__main__':
    
    prompt = 'enter the name of the file with unknown author: '
    text, mystery_filename = get_text_from_valid_file(prompt)
    
    words = get_words(text)
    sentences = get_sentences(text)
    
    # calculate the signature for the mystery file
    mystery_signature = []
    mystery_signature.append(average_word_length(words))
    mystery_signature.append(type_token_ratio(words))
    mystery_signature.append(hapax_legomana_ratio(words))
    mystery_signature.append(average_sentence_length(sentences))
    mystery_signature.append(avg_sentence_complexity(sentences))

    weights = [11, 33, 50, 0.4, 4]
    
    signatures_dir = 'signatures'
    files = os.listdir(signatures_dir)

    # we will assume that there is at least one signature in that directory
    this_file = files[0]
    signature = read_signature('%s/%s'%(signatures_dir, this_file))
    best_score = compare_signatures(mystery_signature, signature[1:], weights)
    best_author = signature[0]

    for this_file in files[1:]:
        signature = read_signature('%s/%s'%(signatures_dir,this_file))
        score = compare_signatures(mystery_signature, signature[1:], weights)
        if score < best_score:
            best_score = score
            best_author = signature[0]
    print "best author match for %s: %s with score %s"%(mystery_filename, best_author, best_score)    
    
