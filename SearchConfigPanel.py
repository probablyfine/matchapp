from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.checkbox import CheckBox
from kivy.metrics import dp,sp
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.app import App
from kivy.properties import ObjectProperty
from SharedComponents import LeftLabel, HelpMsg, ErrorMsg

Builder.load_string( '''
<SearchConfigPanel>:
    sim_input: sim_input
    nmatch_input: nmatch_input
    ngram_input: ngram_input
    excl_input: excl_input
    check_case: check_case
    check_amperland: check_amperland
    check_unidecode: check_unidecode
    check_shortstr: check_shortstr
    check_whitesp: check_whitesp
    orientation: 'vertical'
    padding: ('60dp','60dp')
    spacing: '40dp'
    BoxLayout:
        size_hint_y: 0.10
        LeftLabel:
            text: 'Advanced match options...'
            font_size: '22sp'
            valign: 'middle'
    BoxLayout:
        orientation: 'horizontal'
        size_hint_y: 0.7
        spacing: '100dp'
        BoxLayout:
            orientation: 'vertical'
            BoxLayout:
                orientation: 'horizontal'
                BoxLayout:
                    size_hint: (None,None)
                    height: '32dp'
                    width:  '32dp'
                    Button:
                        text: '?'
                        size_hint: (None,None)
                        height: '20dp'
                        width: '20dp'
                        pos_hint: {'center_y':0.5}
                        on_release: root.help_sim()
                LeftLabel:
                    valign: 'middle'
                    size_hint: (None,None)
                    height: '32dp'
                    width: '180dp'
                    text: 'Min. match score (0-1):'
                TextInput:
                    id: sim_input
                    multiline: False
                    input_filter: 'float'
                    write_tab: False
                    font_size: '16sp'
                    size_hint: (None,None)
                    height: '32dp'
                    width: '80dp'
            BoxLayout:
                orientation: 'horizontal'
                BoxLayout:
                    size_hint: (None,None)
                    height: '32dp'
                    width:  '32dp'
                    Button:
                        text: '?'
                        size_hint: (None,None)
                        height: '20dp'
                        width: '20dp'
                        pos_hint: {'center_y':0.5}
                        on_release: root.help_nmatch()
                LeftLabel:
                    valign: 'middle'
                    size_hint: (None,None)
                    height: '32dp'
                    width: '180dp'
                    text: 'Max number of matches:'
                TextInput:
                    id: nmatch_input
                    multiline: False
                    input_filter: 'int'
                    write_tab: False
                    font_size: '16sp'
                    size_hint: (None,None)
                    height: '32dp'
                    width: '80dp'
            BoxLayout:
                orientation: 'horizontal'
                BoxLayout:
                    size_hint: (None,None)
                    height: '32dp'
                    width:  '32dp'
                    Button:
                        text: '?'
                        size_hint: (None,None)
                        height: '20dp'
                        width: '20dp'
                        pos_hint: {'center_y':0.5}
                        on_release: root.help_ngram()
                LeftLabel:
                    valign: 'middle'
                    size_hint: (None,None)
                    height: '32dp'
                    width: '180dp'
                    text: 'N-gram size:'
                TextInput:
                    id: ngram_input
                    multiline: False
                    input_filter: 'int'
                    write_tab: False
                    font_size: '16sp'
                    size_hint: (None,None)
                    height: '32dp'
                    width: '80dp'
            BoxLayout:
                orientation: 'horizontal'
                BoxLayout:
                    size_hint: (None,None)
                    height: '32dp'
                    width:  '32dp'
                    Button:
                        text: '?'
                        size_hint: (None,None)
                        height: '20dp'
                        width: '20dp'
                        pos_hint: {'center_y':0.5}
                        on_release: root.help_excl()
                LeftLabel:
                    valign: 'middle'
                    size_hint: (None,None)
                    height: '32dp'
                    width: '180dp'
                    text: 'Characters to ignore:'
                TextInput:
                    id: excl_input
                    multiline: False
                    write_tab: False
                    font_size: '16sp'
                    size_hint: (None,None)
                    height: '32dp'
                    width: '80dp'
            Label:
                size_hint_y: None
                height: '32dp'
        BoxLayout:
            orientation: 'vertical'
            BoxLayout:
                orientation: 'horizontal'
                BoxLayout:
                    size_hint: (None,None)
                    height: '32dp'
                    width:  '32dp'
                    Button:
                        text: '?'
                        size_hint: (None,None)
                        height: '20dp'
                        width: '20dp'
                        pos_hint: {'center_y':0.5}
                        on_release: root.help_case()
                LeftLabel:
                    valign: 'middle'
                    size_hint: (None,None)
                    height: '32dp'
                    width: '150dp'
                    text: 'Ignore case:'
                CheckBox:
                    id: check_case
                    size_hint: (None,None)
                    height: '32dp'
                    width: '15dp'
            BoxLayout:
                orientation: 'horizontal'
                BoxLayout:
                    size_hint: (None,None)
                    height: '32dp'
                    width:  '32dp'
                    Button:
                        text: '?'
                        size_hint: (None,None)
                        height: '20dp'
                        width: '20dp'
                        pos_hint: {'center_y':0.5}
                        on_release: root.help_amperland()
                LeftLabel:
                    valign: 'middle'
                    size_hint: (None,None)
                    height: '32dp'
                    width: '150dp'
                    text: 'Convert ampersands:'
                CheckBox:
                    id: check_amperland
                    size_hint: (None,None)
                    height: '32dp'
                    width: '15dp'
            BoxLayout:
                orientation: 'horizontal'
                BoxLayout:
                    size_hint: (None,None)
                    height: '32dp'
                    width:  '32dp'
                    Button:
                        text: '?'
                        size_hint: (None,None)
                        height: '20dp'
                        width: '20dp'
                        pos_hint: {'center_y':0.5}
                        on_release: root.help_unidecode()
                LeftLabel:
                    valign: 'middle'
                    size_hint: (None,None)
                    height: '32dp'
                    width: '150dp'
                    text: 'ASCII transliteration:'
                CheckBox:
                    id: check_unidecode
                    size_hint: (None,None)
                    height: '32dp'
                    width: '15dp'
            BoxLayout:
                orientation: 'horizontal'
                BoxLayout:
                    size_hint: (None,None)
                    height: '32dp'
                    width:  '32dp'
                    Button:
                        text: '?'
                        size_hint: (None,None)
                        height: '20dp'
                        width: '20dp'
                        pos_hint: {'center_y':0.5}
                        on_release: root.help_shortstr()
                LeftLabel:
                    valign: 'middle'
                    size_hint: (None,None)
                    height: '32dp'
                    width: '150dp'
                    text: 'Short string support:'
                CheckBox:
                    id: check_shortstr
                    size_hint: (None,None)
                    height: '32dp'
                    width: '15dp'
            BoxLayout:
                orientation: 'horizontal'
                BoxLayout:
                    size_hint: (None,None)
                    height: '32dp'
                    width:  '32dp'
                    Button:
                        text: '?'
                        size_hint: (None,None)
                        height: '20dp'
                        width: '20dp'
                        pos_hint: {'center_y':0.5}
                        on_release: root.help_whitesp()
                LeftLabel:
                    valign: 'middle'
                    size_hint: (None,None)
                    height: '32dp'
                    width: '150dp'
                    text: 'Ignore whitespace:'
                CheckBox:
                    id: check_whitesp
                    size_hint: (None,None)
                    height: '32dp'
                    width: '15dp'
    BoxLayout:
        size_hint_y: 0.2
        Button:
            text: 'OK'
            font_size: '16sp'
            on_release: root.ok_callback()
''')
        
class SearchConfigPanel( BoxLayout):
    sim_input = ObjectProperty(None)
    nmatch_input = ObjectProperty(None)
    ngram_input = ObjectProperty(None)
    excl_input = ObjectProperty(None)
    check_case = ObjectProperty(None)
    check_amperland = ObjectProperty(None)
    check_unidecode = ObjectProperty(None)
    check_shortstr = ObjectProperty(None)
    check_whitesp = ObjectProperty(None)
    def __init__( self, **kwargs):
        super( SearchConfigPanel, self).__init__( **kwargs)
        
        self.backend = App.get_running_app().backend
        
        self.sim_input.text = str( self.backend.min_similarity)
        self.sim_input.bind( text=self.sim_input_updated)
        
        self.nmatch_input.text = str( self.backend.max_n_matches)
        self.nmatch_input.bind( text=self.nmatch_input_updated)
        
        self.ngram_input.text = str( self.backend.ngram_size)
        self.ngram_input.bind( text=self.ngram_input_updated)
        
        self.excl_input.text = self.backend.excl_chars
        
        self.check_amperland.active = self.backend.advanced_opts['amperland']
        self.check_unidecode.active = self.backend.advanced_opts['unidecode']
        self.check_shortstr.active  = self.backend.advanced_opts['shortstr']
        self.check_case.active      = self.backend.ignore_case
        self.check_whitesp.active   = self.backend.ignore_whitesp
        
    def sim_input_updated( self, sim_input, text):
        if '-' in text:
            sim_input.text = text.replace( '-', '')
        elif text == '':
            return
        elif float(text) > 1:
            sim_input.text = '1'
            
    def nmatch_input_updated( self, nmatch_input, text):
        if '-' in text:
            nmatch_input.text = text.replace( '-', '')
        elif text == '':
            return
        elif int(text) < 1:
            nmatch_input.text = '1'
            
    def ngram_input_updated( self, ngram_input, text):
        if '-' in text:
            ngram_input.text = text.replace( '-', '')
        elif text == '':
            return
        elif int(text) < 1:
            ngram_input.text = '1'
            
    def help_sim( self):
        help_text = 'Set the minimum match score allowed for potential matches. The valid range is between 0 and 1. Scores below this number will not populate into the output. It is generally recommend to keep this set to 0 and manually review matches with low scores.\n\n[b]Note[/b]: If an entry in the [b]Populate to[/b] sheet has no match in the [b]Populate from[/b] sheet with a score greater than this number, the entry will [i]not[/i] be dropped from the output. Rather, the entry will not be paired with any entry from the [b]Populate from[/b] sheet, and the match score for the entry will be left blank.\n'
        self._popup = HelpMsg( help_text, title='Minimum match score', size_hint=(0.75,0.7))
        self._popup.open()
        
    def help_nmatch( self):
        help_text = 'Set the maximum number of matches to consider for each entry in the [b]Populate to[/b] sheet. Decreasing this can lead to more false negatives (dropped matches that are actually good). Increasing this can lead to more false positives (keeping matches that are not good). [b]For large datasets you may get better results if you increase this number.[/b]\n'
        self._popup = HelpMsg( help_text, title='Maximum number of matches', size_hint=(0.7,0.6))
        self._popup.open()
        
    def help_ngram( self):
        help_text = 'The match algorithm converts character strings into a set of "features" based on small groups of sequential characters called "n-grams". The n-gram size sets the number of sequential characters to use for feature extraction. An n-gram size of 3 generally works well, but if all your words/strings are very short a size of 2 could be more accurate.\n'
        self._popup = HelpMsg( help_text, title='N-gram size', size_hint=(0.7,0.6))
        self._popup.open()
        
    def help_excl( self):
        help_text = 'Provide a list of characters that should be ignored when computing match scores. These characters will be removed from each entry before matching.\n\n[b]Note1[/b]: Do not include any delimiters between characters in this list. Just type each character.\n\n[b]Note2[/b]: You cannot include multiple-character sequences. For example, if you are trying to exclude the sequence "com", this will remove all c\'s, o\'s, and m\'s individually.\n\n[b]Note3[/b]: The modified entry will be used to compute match scores, but the original entry will always be preserved in the final output sheet. \n'
        self._popup = HelpMsg( help_text, title='Ignore characters', size_hint=(0.8,0.8))
        self._popup.open()
        
    def help_case( self):
        help_text = 'Ignore whether strings are written in upper- or lower-case. If enabled, "hello" will be considered identical to "HELLO".\n\n[b]Note[/b]: The case-corrected entry will be used to compute match scores, but the original entry will always be preserved in the final output sheet.\n'
        self._popup = HelpMsg( help_text, title='Ignore case', size_hint=(0.65,0.55))
        self._popup.open()
        
    def help_amperland( self):
        help_text = 'Replace ampersands (&) with "and". Example: if enabled, "Health & Safety" will be considered identical to "Health and Safety".\n\n[b]Note[/b]: The modified entry will be used to compute match scores, but the original entry will always be preserved in the final output sheet.\n'
        self._popup = HelpMsg( help_text, title='Convert ampersands', size_hint=(0.65,0.55))
        self._popup.open()
        
    def help_unidecode( self):
        help_text = "Enable to strip accents/diacritics and to transliterate non-Latin characters. Examples: if enabled, ö is equal to o; å is equal to a, ş is equal to s; δ is equal to d; щ is equal to shch; the Hangul character hieut is equal to h.\n\n[b]Note[/b]: The modified entry will be used to compute match scores, but the original entry will always be preserved in the final output sheet.\n"
        self._popup = HelpMsg( help_text, title='ASCII transliteration', size_hint=(0.65,0.55))
        self._popup.open()
        
    def help_shortstr( self):
        help_text = 'If disabled, words/strings shorter than the n-gram size (default=3) will not be matched. If enabled, short strings will be padded to the length of the n-gram size. This allows match scores to be computed for short strings. \n\n[b]Note1[/b]: Match scores may be less accurate for padded words/strings, though these scores are often still useful.\n\n[b]Note2[/b]: The padded entry will be used to compute match scores, but the original entry will always be preserved in the final output sheet.\n'
        self._popup = HelpMsg( help_text, title='Short string support', size_hint=(0.75,0.65))
        self._popup.open()
        
    def help_whitesp( self):
        help_text = 'If enabled, whitespace will be stripped from each entry before matching. This includes spaces, tabs, line-breaks, etc.\n\n[b]Note[/b]: The modified entry will be used to compute match scores, but the original entry will always be preserved in the final output sheet.\n'
        self._popup = HelpMsg( help_text, title='Ignore whitespace', size_hint=(0.65,0.5))
        self._popup.open()
        
    def ok_callback( self):
        if self.sim_input.text == '':
            self._popup = ErrorMsg( error_text='Please enter a value for the minimum match score.')
            self._popup.open()
            return
        if self.nmatch_input.text == '':
            self._popup = ErrorMsg( error_text='Please enter a value for the maximum number of matches.')
            self._popup.open()
            return
        if self.ngram_input.text == '':
            self._popup = ErrorMsg( error_text='Please enter a value for the n-gram size.')
            self._popup.open()
            return
        backend = App.get_running_app().backend
        backend.min_similarity = float(self.sim_input.text)
        backend.max_n_matches  = int(self.nmatch_input.text)
        backend.ngram_size     = int(self.ngram_input.text)
        backend.excl_chars     = self.excl_input.text
        backend.ignore_whitesp = self.check_whitesp.active
        backend.ignore_case    = self.check_case.active
        backend.advanced_opts  = {'amperland': self.check_amperland.active,
                                  'unidecode': self.check_unidecode.active,
                                  'shortstr':  self.check_shortstr.active}
        backend.generate_regex()
        App.get_running_app().nav_to( 'load_screen', 'left')
        