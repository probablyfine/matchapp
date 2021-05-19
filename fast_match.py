from string_grouper import StringGrouper, compute_pairwise_similarities
import pandas as pd
import numpy as np
import re
import string
from unidecode import unidecode
        
class GrouperHelper:
    '''
    class to make string_grouper easier for our use-case. this class has shrunk considerably as
    string_grouper has added new features, and it probably makes sense to re-factor this code eventually.
    '''
    def __init__( self, filename1, filename2, sep1=None, encoding1=None, sep2=None, encoding2=None):
        '''
        Parameters:
            filename1,filename2 (string): path to file (xlsx, csv, txt)
            sep1,sep2 (string or None): separator character if loading csv/txt
            encoding1, encoding2 (string or None): encoding to use if loading csv/txt
        '''
        
        self.file1_load_successful = False
        self.file2_load_successful = False
        
        try:
            print( 'loading first file...')
            # load (first input file)
            self.df1 = self._load_df( filename1, sep1, encoding1)
            self.file1_load_successful = True
            print( f'loaded {filename1} with {self.df1.shape[0]} rows and {self.df1.shape[1]} columns.')
            
            print( 'loading second file...')
            # load (second input file)
            self.df2 = self._load_df( filename2, sep2, encoding2)
            self.file2_load_successful = True
            print( f'loaded {filename2} with {self.df2.shape[0]} rows and {self.df2.shape[1]} columns.')
            
        except Exception as error:
            self.error_type = str(type(error)).split('\'')[1]
            self.error_msg  = error
        
    def _load_df( self, filename, sep, encoding):
        file_ext = filename.split('.')[-1].lower()
        
        if file_ext == 'xlsx':
            df = pd.read_excel( filename)
            
        elif (file_ext == 'csv') | (file_ext == 'txt'):
            kwargs = dict()
            if sep is not None:
                kwargs['sep'] = sep
            if encoding is not None:
                kwargs['encoding'] = encoding
            if len(kwargs) > 0:
                df = pd.read_csv( filename, **kwargs)
            else:
                df = pd.read_csv( filename)
            
        else:
            raise Exception( 'filetype must be .xlsx, .csv, or .txt')
            
        return df
        
    def do_match( self, col1, col2, labels, advanced_opts, excl_chars='', **kwargs):
        '''
        builds list of all possible matches. kwargs will be passed to StringGrouper.
        Parameters:
            col1 (string): column in df1 to compare.
            col2 (string): column in df2 to compare.
            labels (2-tuple of strings): labels to append to column names to keep track of which file they came from
            advanced_opts (dict): booleans for 'amperland', 'unidecode', 'shortstr'
            excl_chars (string/iterable): characters to strip out
        '''
            
        if 'ngram_size' in kwargs:
            ngram_size = kwargs['ngram_size']
        else:
            ngram_size = 3
        if 'regex' in kwargs:
            regex = kwargs['regex']
        else:
            regex = r'[,-./\']|\s'
            
        print( 'prepping first input...')
        s1 = self.df1[col1].dropna().astype(str)
        s1 = clean_series( s1, advanced_opts, excl_chars, ngram_size, regex)
        
        print( 'prepping second input...')
        s2 = self.df2[col2].dropna().astype(str)
        s2 = clean_series( s2, advanced_opts, excl_chars, ngram_size, regex)
        
        print( 'doing initial match...')
        sg = StringGrouper( s1, s2, ignore_index=False, **kwargs).fit()
        self.matches_list = sg.get_matches()
        
        # append the columns used for matching (original ones, not cleaned versions)
        self.append_col( self.df1, col1, col1+' ({})'.format(labels[0]), 'left_index')
        self.append_col( self.df2, col2, col2+' ({})'.format(labels[1]), 'right_index')
        
        print( 'ok.')
        
    def append_col( self, df, col_in, col_out, idx_col):
        '''
        used to populate the list of possible matches with other data columns.
        Parameters:
            df (DataFrame): source of new column to append
            col_in (string): the column in df you want to append
            col_out (string): what to rename the new column, once appended
            idx_col (string): the column in matches_list that contains indices into df.
        '''
        self.matches_list.loc[:,col_out] = df.loc[self.matches_list[idx_col],col_in].reset_index( drop=True)

def clean_series( s, advanced_opts, excl_chars, ngram_size, regex):
    '''
    clean the inputs prior to matching.
    Parameters:
        s (Series): data to clean. must be a pandas Series containing only strings.
        advanced_opts (dict): booleans for 'amperland', 'unidecode', 'shortstr'
        excl_chars (string/iterable): characters to strip out
        ngram_size (int): number of chars to use for generating ngrams
        regex (string): the regex to be passed to StringGrouper
    '''
    print( 'stripping unwanted characters...')
    for c in excl_chars:
        s = s.str.replace( c, '')
    
    # replace ampersands:
    if advanced_opts['amperland']:
        print( 'converting ampersands...')
        s = s.str.replace( '&', 'and')
    
    # replace non-asciis
    if advanced_opts['unidecode']:
        print( 'replacing accents and transliterating non-latin characters...')
        s = do_unidecode( s)
    
    # pad short strings so they don't get dropped
    if advanced_opts['shortstr']:
        print( 'padding short strings...')
        s = pad_series( s, ngram_size, regex)
        
    return s
    
def pad_series( s, ngram_size, regex):
    '''
    pad short strings so they dont get dropped by match.
    s is a Series, must be all strings.
    '''
    
    # Series containing the length of every string in 's', after applying the regex
    s_re = s.apply( lambda x: len( re.sub( regex, r'', x)))
    
    # mask to select only the strings shorter than ngram_size, but larger than 0 so we dont cause empty values to get matched
    mask = (s_re < ngram_size) & (s_re > 0)
    
    # select the appropriate values, do string addition to pad (and string multiplication for variable-length padding)
    s.update( s[mask] + s_re[mask].apply( lambda x: '_' * (ngram_size - x))) # modify in-place, uses index to align
    
    return s
    
def do_unidecode( s):
    '''
    ASCII transliteration.
    s is a Series, must be all strings.
    could use unicodedata.normalize( 'NFD', 'รก').encode( 'ascii', 'ignore').decode( 'utf-8')
    instead of unidecode, but unidecode works with a much wider variety of characters.
    '''
    return s.apply( lambda x: unidecode(x) if any( [ix not in string.printable for ix in x]) else x)
    
def pairwise_compare( a, b, advanced_opts, excl_chars='', **kwargs):
    '''
    make pair-wise comparisons between two data sequences. NaNs in either sequence will propagate to the result.
    Parameters:
        a (sequence): first sequence of data
        b (sequence): second sequence of data. must be same length as a.
        advanced_opts (dict): booleans for 'amperland', 'unidecode', 'shortstr'
        excl_chars (string/iterable): characters to strip out
    '''
    print( 'starting pairwise comparison...')
    print( 'preparing inputs...')
    # convert to pandas Series
    s1 = pd.Series(a)
    s2 = pd.Series(b)
    
    # length of first input
    n = s1.shape[0]
    
    # crash if second input length doesnt match
    if s2.shape[0] != n:
        raise Exception( 'length of a and b must match')
        
    if 'ngram_size' in kwargs:
        ngram_size = kwargs['ngram_size']
    else:
        ngram_size = 3
    if 'regex' in kwargs:
        regex = kwargs['regex']
    else:
        regex = r'[,-./\']|\s'
    
    print( 'handling missing values...')
    # used for keeping track of NaNs
    mask = (s1.isna() | s2.isna())
    nan_idx = s1[mask].index # can use s1 or s2 here, indices should be identical
    s1 = s1[~mask].astype(str)
    s2 = s2[~mask].astype(str)
    
    s1 = clean_series( s1, advanced_opts, excl_chars, ngram_size, regex)
    s2 = clean_series( s2, advanced_opts, excl_chars, ngram_size, regex)
    
    print( 'computing pairwise similarities...')
    matches = compute_pairwise_similarities( s1, s2)
        
    print( 'handling missing values...')
    s_nan = pd.Series( data=np.nan, index=nan_idx)
    matches = matches.append( s_nan, ignore_index=False)
    matches.sort_index( inplace=True)
    
    print( 'ok.')
    return matches