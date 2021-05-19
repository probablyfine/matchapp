from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.metrics import dp,sp
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.app import App
from SharedComponents import LeftLabel, PlaintextSepChooser, PlaintextEncodingChooser, ErrorMsg, HelpMsg, TkSaveDialog
from pathlib import Path

import tkinter as tk
from tkinter import filedialog

Builder.load_string( '''
<ExportMatchesPanel>:
    check_clip: check_clip
    check_file: check_file
    check_space: check_space
    check_sort: check_sort
    txt_nmatch: txt_nmatch
    orientation: 'vertical'
    padding: ('70dp','100dp')
    spacing: '50dp'
    BoxLayout: # topbar
        orientation: 'horizontal'
        size_hint_y: 0.3
        LeftLabel:
            text: 'Export matches...'
            font_size: '22sp'
            valign: 'middle'
        Button:
            text: 'Help'
            size_hint_x: 0.1
            size_hint_y: 0.35
            pos_hint: {'center_y':0.75}
            on_release: root.show_help()
    BoxLayout: # opts_box
        orientation: 'horizontal'
        size_hint_y: 0.4
        BoxLayout: # left_opts_box
            orientation: 'vertical'
            size_hint_y: None
            height: '115dp'
            BoxLayout: # nmatches_box
                orientation: 'horizontal'
                LeftLabel:
                    text: '     Keep the top'
                    size_hint_x: None
                    size_hint_y: None
                    width: '120dp'
                    height: '32dp'
                    valign: 'middle'
                TextInput:
                    id: txt_nmatch
                    text: '1'
                    readonly: True
                    size_hint: (None,None)
                    height: '32dp'
                    width: '40dp'
                    font_size: '16sp'
                BoxLayout: # updown_box
                    orientation: 'vertical'
                    size_hint: (None,None)
                    height: '32dp'
                    width: '40dp'
                    Button:
                        text: '+'
                        size_hint: (None,None)
                        height: '16dp'
                        width: '25dp'
                        on_release: root.nmatch_up()
                    Button:
                        text: '-'
                        size_hint: (None,None)
                        height: '16dp'
                        width: '25dp'
                        on_release: root.nmatch_down()
                LeftLabel:
                    size_hint_y: None
                    height: '32dp'
                    text: 'match(es)'
                    valign: 'middle'
            BoxLayout: # spacer_box
                orientation: 'horizontal'
                CheckBox:
                    id: check_space
                    size_hint_x: None
                    width: '50dp'
                    active: True
                    disabled: True
                LeftLabel:
                    text: 'Add spacer between groups of matches'
                    valign: 'middle'
            BoxLayout: # sort_box
                orientation: 'horizontal'
                CheckBox:
                    id: check_sort
                    active: True
                    size_hint_x: None
                    width: '50dp'
                LeftLabel:
                    text: 'Sort rows by similarity'
                    valign: 'middle'
        BoxLayout: # right_opts_box
            orientation: 'vertical'
            size_hint_y: None
            height: '70dp'
            BoxLayout: # clip_box
                orientation: 'horizontal'
                CheckBox:
                    id: check_clip
                    group: 'export_opts'
                    size_hint_x: None
                    width: '50dp'
                LeftLabel
                    text: 'Copy matches to clipboard'
                    valign: 'middle'
            BoxLayout: # file_box
                orientation: 'horizontal'
                CheckBox:
                    id: check_file
                    group: 'export_opts'
                    active: True
                    size_hint_x: None
                    width: '50dp'
                LeftLabel:
                    text: 'Save matches to file'
                    valign: 'middle'
    BoxLayout: # btn_box
        orientation: 'horizontal'
        spacing: '15dp'
        size_hint_y: 0.3
        Button:
            text: 'Back'
            font_size: '16sp'
            on_release: root.back_callback()
        Button:
            text: 'Export'
            font_size: '16sp'
            on_release: root.export_callback()
''')
    
class ExportMatchesPanel( BoxLayout):
    check_clip = ObjectProperty(None)
    check_file = ObjectProperty(None)
    check_space = ObjectProperty(None)
    check_sort = ObjectProperty(None)
    txt_nmatch = ObjectProperty(None)
    def __init__( self, **kwargs):
        super( ExportMatchesPanel, self).__init__( **kwargs)
        
        self.check_clip.bind( active=self.export_opts_callback)
        self.check_file.bind( active=self.export_opts_callback)
        
        self.sep = None
        self.encoding = None
        
    def nmatch_up( self):
        max = App.get_running_app().backend.max_n_matches
        if int(self.txt_nmatch.text) >= max:
            return
        self.txt_nmatch.text = str( int(self.txt_nmatch.text) + 1)
        self.check_space.disabled = False
        
    def nmatch_down( self):
        if self.txt_nmatch.text == '1':
            return
        self.txt_nmatch.text = str( int(self.txt_nmatch.text) - 1)
        if self.txt_nmatch.text == '1':
            self.check_space.disabled = True
            
    def show_help( self):
        help_text = '''- [u]Keep the top [i]n[/i] matches[/u]: choose how many alternate matches you want to review. If you only want the top-scoring match for each row, select \'1\'.\n\n- [u]Add spacer between groups of matches[/u]: if you export multiple alternate matches, this option adds a blank spacer row between separate groups of matches, which helps guide the eye during manual review.\n\n- [u]Sort rows by similarity[/u]: if enabled, rows will be sorted by match score. If disabled, the original row order from your input spreadsheet will be preserved.\n\n- [u]Copy matches to clipboard[/u]: choose this option if you want to paste the matches into Excel or Google Sheets.\n\n- [u]Save matches to file[/u]: choose this option if you want to save the matches to a spreadsheet file (.xlsx, .csv, or .txt).\n'''
        self._popup = HelpMsg( help_text, title='Help', size_hint=(0.9,0.9))
        self._popup.open()
        
    def export_opts_callback( self, check, value):
        if (self.check_clip.active == False) & (self.check_file.active == False):
            check.active = True
            
    def match_opts_callback( self, check, value):
        if (self.check_all.active == False) & (self.check_best.active == False):
            check.active = True
        if self.check_all.active == True:
            self.check_space.disabled = False
        else:
            self.check_space.disabled = True
            
    def back_callback( self,):
        app = App.get_running_app()
        app.backend.drop_appends()
        app.nav_to( 'append_screen', 'right')
        
    def prep_export( self, *args):
        backend = App.get_running_app().backend
        self.matches_for_export = backend.clean_matches_for_export( int(self.txt_nmatch.text), 
                                                                    restore_row_order=(not self.check_sort.active), 
                                                                    use_spacer=self.check_space.active)
    def export_callback( self):
        self._popup = Popup( size=('410dp','150dp'), size_hint=(None,None), auto_dismiss=False, title='Please wait')
        self._popup.content = Label( text='Working... this can take a long time for large files, and \nthis window will stop responding until finished.')
        self._popup.open()
        # wait for popup to actually open before starting to load
        Clock.schedule_once( self.export_really, 0.1)
        
    def export_really( self, obj):
        backend = App.get_running_app().backend
        
        if self.check_clip.active:
            self.prep_export()
            self.matches_for_export.to_clipboard( index=False)
            self._popup.dismiss()
        else:
            with TkSaveDialog( 'matches.xlsx', [('Spreadsheet','.xlsx .csv .txt')]) as dialog:
                filename = dialog.get_filename()
            self._popup.dismiss()
            if filename != '':
                self.save_export( filename)
                
    def save_export( self, filename):
        self.out_file = Path( filename)
        self.out_file = self.out_file.with_suffix( self.out_file.suffix.lower())
        self.plaintext_opts()
            
    def plaintext_opts( self, obj=None):
        
        if (self.out_file.suffix == '.csv') | (self.out_file.suffix == '.txt'):
            self._popup.dismiss()
            self._popup = Popup( size=('300dp','350dp'), size_hint=(None,None), title='Select plaintext delimiter', auto_dismiss=False)
            self._popup.content = PlaintextSepChooser( self._popup.dismiss, self.delim_opts_next)
            self._popup.open()
        else:
            self.save_really()
            
    def delim_opts_next( self, obj):
        delim_choice = self._popup.content.get_delim_choice()
        if delim_choice == '':
            return
        else:
            self.sep = delim_choice
            self._popup.dismiss()
            self._popup = Popup( size=('450dp','200dp'), size_hint=(None,None), title='Select plaintext encoding', auto_dismiss=False)
            self._popup.content = PlaintextEncodingChooser( self._popup.dismiss, self.enc_opts_ok)
            self._popup.open()
            
    def enc_opts_ok( self, obj):
        enc_choice = self._popup.content.dropbtn.text
        if enc_choice == '[use default]':
            self.encoding = None
        else:
            self.encoding = enc_choice.split(' ')[0]
        self.save_really()
            
    def save_really( self):
        backend = App.get_running_app().backend
        try:
            if self.out_file.suffix == '.xlsx':
                self.prep_export()
                self.matches_for_export.to_excel( str(self.out_file), index=False)
                self._popup.dismiss()
                
            elif (self.out_file.suffix == '.csv') | (self.out_file.suffix == '.txt'):
                self.prep_export()
                self.matches_for_export.to_csv( str(self.out_file), 
                                                index=False, 
                                                sep=self.sep, 
                                                encoding=self.encoding)
                self._popup.dismiss()
                
            else:
                raise Exception( 'Filetype must be .xlsx, .csv, or .txt')
            
        except Exception as error:
            self._popup.dismiss()
            error_type = str(type(error)).split('\'')[1]
            self._popup = ErrorMsg( error_text='Error saving {}.\n\n{}: {}'.format(self.out_file.parts[-1], error_type, error))
            self._popup.open()