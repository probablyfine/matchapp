import pandas as pd
import os
from fast_match import GrouperHelper, pairwise_compare
import numpy as np
import itertools
#import pdb

class MatchBackend:
    
    def __init__( self):
        self.load_encodings()
        
        # names of input files
        self.labels = ['File1','File2']
        
        # columns in file1,file2 for initial search
        self.narrow_by = [None,None]
        
        # columns in file1,file2 for additional search terms
        self.also_compare = []
        
        # columns to append but not used for search (track separately)
        self.appends1 = []
        self.appends2 = []
        
        self.min_similarity = 0
        self.max_n_matches = 10
        
        self.excl_chars = r',-./\''
        self.ignore_whitesp = True
        self.generate_regex()
        
        self.ignore_case = True
        self.ngram_size = 3
        
        self.advanced_opts = {'amperland': True,
                              'unidecode': True,
                              'shortstr':  True}
        
        self.sim_avg_col    = 'similarity: average'
        self.orig_order_col = 'original row order'
        self.nofields_col   = 'num. fields used for avg.'
        
    def generate_regex( self):
        if self.ignore_whitesp:
            self.regex = '\s'
        else:
            self.regex = ''
            
    def load_encodings( self):
        try:
            df_encodings = pd.read_excel( 'encodings.xlsx').fillna('')
            df_encodings['Languages'] = df_encodings['Languages'].astype(str).apply( lambda x: '({})'.format(x))
            self.encodings = ['[use default]'] + df_encodings['Codec'].astype(str).str.cat( df_encodings['Languages'], sep=' ').tolist()
            self.df_encodings = df_encodings
        except:
            self.encodings = ['[use default]']
        
    def init_fast_match( self, file1, file2, sep1, sep2, encoding1, encoding2):
        self.grouper_helper = GrouperHelper( file1, 
                                             file2, 
                                             sep1=sep1, 
                                             sep2=sep2, 
                                             encoding1=encoding1, 
                                             encoding2=encoding2)
                                             
        if self.grouper_helper.file1_load_successful & self.grouper_helper.file2_load_successful:
            self.columns1 = self.grouper_helper.df1.columns
            self.columns2 = self.grouper_helper.df2.columns
            return True
        else:
            return False
            
    def merge_cols( self, df, cols):
        if len(cols) == 1:
            return df[cols[0]].copy()
        col_out = df[cols[0]].fillna('').astype(str)
        for c in cols[1:]:
            col_out = col_out.str.cat( df[c].fillna('').astype(str), sep=' ')
        return col_out
        
    def do_fast_match( self):
        self.grouper_helper.do_match( self.narrow_by[0], 
                                      self.narrow_by[1], 
                                      self.labels,
                                      self.advanced_opts,
                                      excl_chars=self.excl_chars,
                                      min_similarity=self.min_similarity, 
                                      max_n_matches=self.max_n_matches,
                                      regex=self.regex,
                                      ignore_case=self.ignore_case,
                                      ngram_size=self.ngram_size)
        
        self.match_columns_orig = self.grouper_helper.matches_list.columns.copy()
        
    def generate_append_col_label( self, col, source_label):
        return '{} ({})'.format( col, source_label)
    
    def generate_similarity_col_label( self, col1, source_label1, col2, source_label2):
        return 'similarity: {} ({}) vs {} ({})'.format( col1, source_label1, col2, source_label2)
        
    def compare_columns( self):
        if len( self.also_compare) == 0:
            return
        source_cols = [self.generate_append_col_label( self.narrow_by[0], self.labels[0])] # used for computing sim avg
        similarity_cols = ['similarity']
        for col_in1,col_in2 in self.also_compare:
            print( f'comparing: {col_in1} vs. {col_in2}')
            col_out1 = self.generate_append_col_label( col_in1, self.labels[0])
            col_out2 = self.generate_append_col_label( col_in2, self.labels[1])
            
            self.grouper_helper.append_col( self.grouper_helper.df1, col_in1, col_out1, 'left_index')
            self.grouper_helper.append_col( self.grouper_helper.df2, col_in2, col_out2, 'right_index')
            sim_col = self.generate_similarity_col_label( col_in1, self.labels[0], col_in2, self.labels[1])
            self.grouper_helper.matches_list.loc[:,sim_col] = pairwise_compare( self.grouper_helper.matches_list[col_out1], 
                                                                                self.grouper_helper.matches_list[col_out2], 
                                                                                self.advanced_opts,
                                                                                excl_chars=self.excl_chars,
                                                                                regex=self.regex,
                                                                                ignore_case=self.ignore_case,
                                                                                ngram_size=self.ngram_size)
            source_cols.append( col_out1)
            similarity_cols.append( sim_col)
            
        # compute the number of non-null fields
        #self.grouper_helper.matches_list[self.nofields_col] = self.grouper_helper.matches_list[source_cols].notna().sum( axis=1)
        self.grouper_helper.matches_list.loc[:,self.nofields_col] = self.grouper_helper.matches_list[similarity_cols].notna().sum( axis=1)
        
        # compute average similarity between all possible matches
        self.grouper_helper.matches_list.loc[:,self.sim_avg_col] = self.grouper_helper.matches_list[similarity_cols].sum( axis=1) / self.grouper_helper.matches_list[self.nofields_col]
        
    def append_column( self, which, col):
        if which == 1:
            self.grouper_helper.append_col( self.grouper_helper.df1, col, self.generate_append_col_label(col,self.labels[0]), 'left_index')
        elif which == 2:
            self.grouper_helper.append_col( self.grouper_helper.df2, col, self.generate_append_col_label(col,self.labels[1]), 'right_index')
            
    def reset_matches( self):
        cols = self.match_columns_orig
        self.grouper_helper.matches_list = self.grouper_helper.matches_list[cols].copy()
        
    def drop_appends( self):
        if len(self.also_compare) == 0:
            return
        cols_to_drop = []
        for col_in1,col_in2 in self.also_compare:
            cols_to_drop.append( self.generate_append_col_label( col_in1, self.labels[0]))
            cols_to_drop.append( self.generate_append_col_label( col_in2, self.labels[1]))
        self.grouper_helper.matches_list.drop( labels=cols_to_drop, axis=1, inplace=True)
        
    def append_missing( self, matches_list):
        # find any rows that got dropped (presumably because initial match found no matches.)
        missing_mask = ~(self.grouper_helper.df1.index.isin( matches_list['left_index']))
        # if none missing, just return the list that was passed in, unchanged
        if missing_mask.sum() == 0:
            return matches_list
        col_lbl = self.labels[0]
        cols = [c for c in self.grouper_helper.df1.columns if self.generate_append_col_label(c,col_lbl) in matches_list.columns]
        # generate a new DataFrame containing the missing rows, plus properly re-named cols
        df_append = self.grouper_helper.df1.loc[missing_mask,cols].copy()
        df_append.rename( columns=lambda x: self.generate_append_col_label(x,col_lbl), inplace=True)
        df_append.index.rename( 'left_index', inplace=True) # otherwise indices from missing rows won't align with left_index column
        # append that new DataFrame to the list of matches and return the result
        return matches_list.append( df_append.reset_index(), ignore_index=True)
        
    def generate_column_order( self):
        # simavg, a, b, sim:a-b, c, sim:a-c, appends1, appends2
        if len(self.also_compare) == 0:
            cols_out = [self.orig_order_col]
        else:
            cols_out = [self.orig_order_col, self.sim_avg_col, self.nofields_col]
        
        # will result in 2 cols appended from the 2 files, plus a similarity column
        cols_out.append( self.generate_append_col_label( self.narrow_by[0], self.labels[0]))
        cols_out.append( self.generate_append_col_label( self.narrow_by[1], self.labels[1]))
        cols_out.append( self.generate_similarity_col_label( self.narrow_by[0], self.labels[0], self.narrow_by[1], self.labels[1]))
        
        # EACH pair in the list will result in 2 cols appended from the 2 files, plus a similarity column
        for a,b in self.also_compare:
            ap1 = self.generate_append_col_label( a, self.labels[0])
            ap2 = self.generate_append_col_label( b, self.labels[1])
            sim = self.generate_similarity_col_label( a, self.labels[0], b, self.labels[1])
            if ap1 not in cols_out:
                cols_out.append( ap1)
            if ap2 not in cols_out:
                cols_out.append( ap2)
            if sim not in cols_out:
                cols_out.append( sim)
        
        # will produce 1 column from first file per each entry in the list
        for a in self.appends1:
            ap1 = self.generate_append_col_label( a, self.labels[0])
            if ap1 not in cols_out:
                cols_out.append( ap1)
        
        # will produce 1 column from second file per each entry in the list
        for b in self.appends2:
            ap2 = self.generate_append_col_label( b, self.labels[1])
            if ap2 not in cols_out:
                cols_out.append( ap2)
        
        return cols_out
        
    def clean_matches_for_export( self, nmatch, restore_row_order=False, use_spacer=False):
        print( 'preparing to export...')
        # make a copy of the full list of matches
        matches_list = self.grouper_helper.matches_list.copy()
        # append any rows that may have been dropped in the initial match
        matches_list = self.append_missing( matches_list)
        
        # rename original similarity column
        new_lbl = self.generate_similarity_col_label( self.narrow_by[0], self.labels[0], self.narrow_by[1], self.labels[1])
        matches_list.rename( columns={'similarity': new_lbl}, inplace=True)
        
        # figure out which column to use to sort
        if self.sim_avg_col in matches_list.columns:
            sim_col = self.sim_avg_col
        else:
            sim_col = new_lbl
        self.sim_col = sim_col
        
        print( 'selecting top matches...')
        # select the top matches
        best_matches = matches_list.groupby( 'left_index').agg( {sim_col: 'max'}).reset_index()
        best_matches = best_matches.merge( matches_list, on=['left_index', sim_col])
        
        # resolve ties, and to ensure indexing succeeds later
        dupe_mask = best_matches['left_index'].duplicated()
        best_matches = best_matches[~dupe_mask]
        
        print( 'sorting...')
        # sort the top matches by similarity first, then by nfields. that way exact matches are sorted by nfields.
        if self.nofields_col in best_matches.columns:
            sortby = [sim_col,self.nofields_col]
            asc = [False,False]
        else:
            sortby = sim_col
            asc = False
        exact_mask = best_matches[sim_col] > 0.9999999
        best_matches.loc[exact_mask,sim_col] = 1.0
        best_matches = best_matches.sort_values( by=sortby, ascending=asc)
        
        if nmatch > 1:
            # use the sorted list of top matches to group+sort possible matches in the full list
            matches_list.set_index( 'left_index', inplace=True)
            best_matches.set_index( 'left_index', inplace=True)
            matches_list['sort order'] = 0
            print( 'appending sort order...')
            best_matches['sort order'] = [i for i in range( best_matches.shape[0])]
            matches_list.loc[best_matches.index,'sort order'] = best_matches.loc[best_matches.index,'sort order'].copy()
            matches_list.sort_values( by=['sort order',sim_col], ascending=[True,False], inplace=True)
            
            # restore the left_index column to track the original, unsorted row order
            matches_list.reset_index( drop=False, inplace=True)
            
            if use_spacer:
                print( 'appending blank row...')
                # append one blank row to the end of the df
                last_idx_plus_one = matches_list.index[-1] + 1
                matches_list.loc[last_idx_plus_one] = np.nan
                last_idx = matches_list.index[-1]
                idxfun = lambda x: x.index[:nmatch].tolist() + [last_idx] # top nmatch matches plus blank row
            else:
                idxfun = lambda x: x.index[:nmatch].tolist() # top nmatch matches (and no blank row)
            
            print( 'generating indices to extract alternate matches...')
            # generate indices to either 1) select top nmatch matches, or 2) select top nmatch matches AND a blank row
            # (the itertools.chain part just unrolls the 2d list of indices that come out of the DataFrame)
            new_idx = pd.Index( itertools.chain( *matches_list.groupby( 'sort order').apply( idxfun).values))
            
            print( 'extracting alternate matches...')
            # pare down to just top nmatches
            matches_list = matches_list.loc[new_idx]
            
            if use_spacer:
                print( 'populating row order into blank rows...')
                matches_list.reset_index( drop=True, inplace=True)         # otherwise all blank rows will have same index
                ridxfun = lambda x: x.index[-1] + 1                        # get last index for the group of alt matches, plus 1 to land on spacer row
                s_idx = matches_list.groupby('left_index').apply( ridxfun) # extract indices of each spacer row, with left_index as the indices for the resulting Series
                s_idx = pd.Series( s_idx.index.values, index=s_idx)        # swap indices and values of Series
                matches_list.loc[s_idx.index,'left_index'] = s_idx         # populate the correct left_index values to each spacer row
            
            matches_list.rename( columns={'left_index':self.orig_order_col}, inplace=True) # rename left_index to something more meaningful
            matches_list = matches_list.drop( columns=['right_index','sort order']) # drop unneeded col
            
            matches_list = matches_list[self.generate_column_order()]
            if restore_row_order:
                matches_list = matches_list.sort_values( by=[self.orig_order_col,self.sim_col], ascending=[True,False])
            
            # add 2 to account for header and 0-index
            matches_list[self.orig_order_col] += 2
            
            print( 'ok.')
            return matches_list
        else:
            # rename left_index to something more meaningful
            best_matches.rename( columns={'left_index':self.orig_order_col}, inplace=True)
            # drop unneeded col
            best_matches = best_matches.drop( columns=['right_index'])
            
            best_matches = best_matches[self.generate_column_order()]
            if restore_row_order:
                best_matches = best_matches.sort_values( by=self.orig_order_col)
                
            # add 2 to account for header and 0-index
            best_matches[self.orig_order_col] += 2
            
            print( 'ok.')
            return best_matches