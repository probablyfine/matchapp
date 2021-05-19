from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.rst import RstDocument
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.metrics import dp,sp
from kivy.app import App
from SharedComponents import LeftLabel, RightLabel, LeftButton, PlaintextEncodingChooser, PlaintextSepChooser, HelpMsg, ErrorMsg, TkOpenDialog

Builder.load_string( '''
<DataFrameNameChooser>:
    name_input: name_input
    cancel_btn: cancel_btn
    next_btn: next_btn
    orientation: 'vertical'
    BoxLayout:
        orientation: 'horizontal'
        padding: ('15dp','10dp')
        LeftLabel:
            size_hint: (None,None)
            height: '32dp'
            width: '60dp'
            font_size: '16sp'
            text: 'Name:'
            valign: 'middle'
        TextInput:
            id: name_input
            multiline: False
            write_tab: False
            font_size: '16sp'
            size_hint_y: None
            height: '32dp'
    BoxLayout:
        orientation: 'horizontal'
        padding: ('15dp','15dp')
        Button:
            id: cancel_btn
            text: 'Cancel'
        Button:
            id: next_btn
            text: 'OK'
            
<FileSection>:
    file_label: file_label
    browse_btn: browse_btn
    path_input: path_input
    orientation: 'horizontal'
    padding: ('10dp','40dp')
    LeftLabel:
        id: file_label
        font_size: '16sp'
        size_hint_x: 0.2
        size_hint_y: None
        height: '32dp'
        valign: 'middle'
    TextInput:
        id: path_input
        multiline: False
        write_tab: False
        font_size: '16sp'
        size_hint_x: 0.65
        size_hint_y: None
        height: '32dp'
    Button:
        id: browse_btn
        text: 'Browse'
        font_size: '16sp'
        size_hint_x: 0.15
        size_hint_y: None
        height: '32dp'
        on_release: root.browse_callback()
            
<LoadPanel>:
    opts_btn: opts_btn
    file_sections_box: file_sections_box
    load_btn: load_btn
    orientation: 'vertical'
    padding: ('75dp','120dp')
    BoxLayout:
        orientation: 'horizontal'
        size_hint_y: 0.35
        spacing: '15dp'
        LeftLabel:
            text: 'Select files...'
            font_size: '22sp'
            valign: 'top'
            size_hint_x: 0.8
        Button:
            text: 'About'
            size_hint_x: 0.1
            size_hint_y: 0.25
            pos_hint: {'center_y':1}
            on_release: root.show_about()
        Button:
            text: 'Help'
            size_hint_x: 0.1
            size_hint_y: 0.25
            pos_hint: {'center_y':1}
            on_release: root.show_help()
    BoxLayout:
        size_hint_y: 0.35
        id: file_sections_box
        orientation: 'vertical'
    BoxLayout:
        size_hint_y: 0.3
        orientation: 'horizontal'
        spacing: '15dp'
        Button:
            id: opts_btn
            size_hint_x: 0.25
            text: 'Advanced Options'
            font_size: '16sp'
        Button:
            id: load_btn
            size_hint_x: 0.75
            text: 'Load'
            font_size: '16sp'
''')

class DataFrameNameChooser( BoxLayout):
    '''
    popup for choosing the name/label of a dataframe
    '''
    name_input = ObjectProperty(None)
    cancel_btn = ObjectProperty(None)
    next_btn   = ObjectProperty(None)
    
    def __init__( self, cancel_callback, next_callback, default_name, **kwargs):
        super( DataFrameNameChooser, self).__init__( **kwargs)
        
        self.name_input.text = default_name
        self.cancel_btn.bind( on_release=cancel_callback)
        self.next_btn.bind( on_release=next_callback)
        self.name_input.focus = True
        
    def get_text( self):
        return self.name_input.text

class FileSection( BoxLayout):
    '''
    contains the filepath text input plus browse button. also manages naming and plaintext config via popups
    '''
    file_label = ObjectProperty(None)
    browse_btn = ObjectProperty(None)
    path_input = ObjectProperty(None)
    def __init__( self, text, default_dataset_name, **kwargs):
        super( FileSection, self).__init__( **kwargs)
        
        # will need to store the chosen sep and encoding for csv/plaintext
        self.sep = None
        self.encoding = None
        
        self.dataset_name = default_dataset_name
        self.file_label.text = text
        
    def get_path( self):
        return self.path_input.text
        
    def set_path( self, filename):
        self.path_input.text = filename
        
        file_ext = filename.split('.')[-1].lower()
        
        if (file_ext == 'csv') | (file_ext == 'txt'):
            self._popup = Popup( size=('300dp','350dp'), size_hint=(None,None), title='Select plaintext delimiter', auto_dismiss=False)
            self._popup.content = PlaintextSepChooser( self.delim_opts_cancel, self.delim_opts_next)
            self._popup.open()
        else:
            self.sep = None
            self.encoding = None
            self.choose_name()
            
    def delim_opts_cancel( self, btn=None):
        self.path_input.text = ''
        self.sep = None
        self._popup.dismiss()
        
    def delim_opts_next( self, btn=None):
        delim_choice = self._popup.content.get_delim_choice()
        if delim_choice == '':
            return
        else:
            self.sep = delim_choice
            self._popup.dismiss()
            self._popup = Popup( size=('450dp','200dp'), size_hint=(None,None), title='Select plaintext encoding', auto_dismiss=False)
            self._popup.content = PlaintextEncodingChooser( self.enc_opts_cancel, self.enc_opts_ok)
            self._popup.open()
            
    def enc_opts_cancel( self, btn=None):
        self.path_input.text = ''
        self.encoding = None
        self._popup.dismiss()
        
    def enc_opts_ok( self, btn=None):
        enc_choice = self._popup.content.dropbtn.text
        if enc_choice == '[use default]':
            self.encoding = None
        else:
            self.encoding = enc_choice.split(' ')[0]
        self._popup.dismiss()
        self.choose_name()
        
    def choose_name( self):
        self._popup = Popup( size=('400dp','200dp'), size_hint=(None,None), title='Choose a name for this dataset...', auto_dismiss=False)
        self._popup.content = DataFrameNameChooser( self.choose_name_cancel, self.choose_name_next, self.dataset_name)
        self._popup.open()
        
    def choose_name_cancel( self, btn):
        self.path_input.text = ''
        self._popup.dismiss()
        
    def choose_name_next( self, btn):
        name = self._popup.content.get_text()
        if name == '':
            return
        self.dataset_name = name
        self._popup.dismiss()
        self.path_input.cursor = (len(self.path_input.text),0)
        self.set_focus()
        
    def set_focus( self):
        self.path_input.focus = True
        
    def bind_enter_keypress( self, callback):
        self.path_input.bind( on_text_validate=callback)
        
    def browse_callback( self):
        self._popup = Popup( background_color=[0,0,0,0.5], 
                             background='bg.png', 
                             separator_color=[0,0,0,0],
                             title=' ', 
                             auto_dismiss=False)
        self._popup.open()
        # wait for popup to actually open before starting to load
        Clock.schedule_once( self.browse_actually, 0.1)
        
    def browse_actually( self, obj):
        with TkOpenDialog( [('Spreadsheet','.xlsx .csv .txt')]) as dialog:
            filename = dialog.get_filename()
        self._popup.dismiss()
        if filename != '':
            self.set_path( filename)
        
class LoadPanel( BoxLayout):
    '''
    high-level load panel, contains FileSection widgets and big load button
    '''
    file_sections_box = ObjectProperty(None)
    load_btn = ObjectProperty(None)
    opts_btn = ObjectProperty(None)
    def __init__( self, **kwargs):
        super( LoadPanel, self).__init__( **kwargs)
        
        self.file_section1 = FileSection( text='Populate to:', default_dataset_name='File1')
        self.file_section2 = FileSection( text='Populate from:', default_dataset_name='File2')
        
        self.file_sections_box.add_widget( self.file_section1)
        self.file_sections_box.add_widget( self.file_section2)
        
        self.load_btn.bind( on_release=self.load_callback)
        self.opts_btn.bind( on_release=self.opts_callback)
        
        # set focus to the first textinput
        self.file_section1.set_focus()
        
    def opts_callback( self, *args):
        App.get_running_app().nav_to( 'searchconfig_screen', 'right')
        
    def show_help( self):
        help_text = '- In SQL terminology, this software implements a "left join" on one or more inexact keys.\n\n- Use the [b]"Browse"[/b] buttons to select the two spreadsheets you want to match. When prompted, give each sheet a name.\n\n- The [b]"Populate to"[/b] sheet is the one you want to populate with matches. In SQL terminology it is the "left" table. The match output will contain one (or optionally more) match result for each row in this sheet. [b]This is typically the sheet with the fewest rows.[/b]\n\n- The [b]"Populate from"[/b] sheet should contain the potential matches for the rows in the first sheet. In SQL terminology this is the "right" table. [u]Note:[/u] not every row in this sheet will necessarily populate into the first sheet, and rows from this sheet can populate more than once into the first one.\n'
        self._popup = HelpMsg( help_text, title='Help', size_hint=(0.92,0.92))
        self._popup.open()
        
    def show_about( self):
        about_text = 'This GUI and related code is written by Steve Suway. The GUI is built using Kivy. Matching computations are performed using string_grouper, which is written by Chris van den Berg. string_grouper\'s matching functionality builds upon sparse_dot_topn, which is an open-source project by ING Bank. ASCII transliteration is done using Unidecode, written by Tomaz Solc. Other packages this code relies on include NumPy, SciPy, and pandas.'
        self._popup = HelpMsg( about_text, title='About', size_hint=(0.75,0.60))
        self._popup.open()
        
    def load_callback( self, btn=None):
        file1 = self.file_section1.get_path()
        file2 = self.file_section2.get_path()
        if (file1 == '') | (file2 == ''):
            return
            
        self._popup = Popup( size=('425dp','150dp'), size_hint=(None,None), auto_dismiss=False, title='Please wait')
        self._popup.content = Label( text='Loading files... this can take a long time for large files, and \nthis window will stop responding until finished.')
        self._popup.open()
        
        # wait for popup to actually open before starting to load
        Clock.schedule_once( self.do_load, 0.1)
        
    def do_load( self, obj):
        app = App.get_running_app()
        
        app.backend.labels[0] = self.file_section1.dataset_name
        app.backend.labels[1] = self.file_section2.dataset_name
        
        if app.backend.labels[0] == app.backend.labels[1]:
            app.backend.labels[1] += '(2)'
        
        file1 = self.file_section1.get_path()
        file2 = self.file_section2.get_path()
            
        sep1 = self.file_section1.sep
        sep2 = self.file_section2.sep
        encoding1 = self.file_section1.encoding
        encoding2 = self.file_section2.encoding
        
        load_successful = app.backend.init_fast_match( file1, file2, sep1, sep2, encoding1, encoding2)
        
        self._popup.dismiss()
        
        if load_successful:
            app.panels['narrowby_screen'].populate_dropdowns()
            app.panels['alsocompare_screen'].reset_panel()
            app.panels['append_screen'].populate()
            app.nav_to( 'narrowby_screen', 'left')
        else:
            error_type = app.backend.grouper_helper.error_type
            error_msg  = app.backend.grouper_helper.error_msg
            if app.backend.grouper_helper.file1_load_successful:
                problem_file = app.backend.labels[1]
            else:
                problem_file = app.backend.labels[0]
            errtxt = 'Error loading {}.\n\n{}: {}'.format(problem_file, error_type, error_msg)
            if error_type == 'UnicodeDecodeError':
                errtxt += '\n\nThis probably means you selected the wrong encoding. Try re-loading your plaintext file and select a different encoding when prompted.'
            self._popup = ErrorMsg( error_text=errtxt)
            self._popup.open()
    