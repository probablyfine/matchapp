from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner, SpinnerOption
from kivy.uix.dropdown import DropDown
from kivy.uix.popup import Popup
from kivy.metrics import dp,sp
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.app import App
import tkinter as tk
from tkinter import filedialog

Builder.load_string( '''
#: import Metrics kivy.metrics.Metrics

<LeftLabel>
    text_size: self.size
    halign: 'left'
    
<RightLabel>
    text_size: self.size
    halign: 'right'
    
<LeftButton>
    text_size: self.size
    halign: 'left'
    valign: 'middle'
    padding: '15dp','5dp'
    
<LeftSpinner>
    text_size: self.size
    halign: 'left'
    valign: 'middle'
    padding: '15dp',0
    
<SpinnerOpts>
    text_size: self.size
    halign: 'left'
    valign: 'middle'
    padding: '15dp',0
    
<PlaintextSepChooser>:
    orientation: 'vertical'
    padding: '5dp','5dp'
    BoxLayout:
        orientation: 'vertical'
        size_hint_y: 0.8
        padding: 0,'15dp'
        BoxLayout:
            orientation: 'horizontal'
            LeftLabel:
                text: 'Comma'
                valign: 'middle'
            CheckBox:
                group: 'delim'
                id: toggle_comma
        BoxLayout:
            orientation: 'horizontal'
            LeftLabel:
                text: 'Tab'
                valign: 'middle'
            CheckBox:
                group: 'delim'
                id: toggle_tab
        BoxLayout:
            orientation: 'horizontal'
            LeftLabel:
                text: 'Space'
                valign: 'middle'
            CheckBox:
                group: 'delim'
                id: toggle_space
        BoxLayout:
            orientation: 'horizontal'
            LeftLabel:
                text: 'Semicolon'
                valign: 'middle'
            CheckBox:
                group: 'delim'
                id: toggle_semicolon
        BoxLayout:
            orientation: 'horizontal'
            LeftLabel:
                text: 'Other'
                valign: 'middle'
            TextInput:
                multiline: False
                font_size: '16sp'
                size_hint_y: None
                height: '32dp'
                size_hint_x: None
                width: '75dp'
                id: delim_other
    BoxLayout:
        orientation: 'horizontal'
        size_hint_y: 0.2
        Button:
            text: 'Cancel'
            id: cancel_button
        Button:
            text: 'OK'
            id: next_button
            
<ErrorMsg>
    width: '450dp'
    height: error_box.height + 50 * Metrics.dp
    size_hint: None,None
    BoxLayout:
        size_hint: (None,None)
        height: self.minimum_height + 25 * Metrics.dp
        width: root.width - 25 * Metrics.dp
        id: error_box
        orientation: 'vertical'
        Label:
            id: error_label
            size_hint_y: None
            height: self.texture_size[1]
            text_size: (self.width,None)
            padding: ('20dp','20dp')
            text: root.error_text
        Label:
            size_hint_y: None
            height: '15dp'
            text: ''
        Button:
            size_hint_y: None
            width: '100dp'
            height: '40dp'
            id: dismiss_btn
            text: 'Dismiss'
            on_release: root.dismiss()

<HelpMsg>:
    help_text: help_text
    title: 'Help'
    BoxLayout:
        orientation: 'vertical'
        padding: ('20dp','20dp')
        LeftLabel:
            id: help_text
            markup: True
            valign: 'middle'
            size_hint_y: 0.8
        Button:
            text: 'OK'
            size_hint_y: 0.2
            on_release: root.dismiss()
''')

font_size = '16sp'
row_height = '32dp'

class LeftLabel( Label):
    def __init__( self, **kwargs):
        super( LeftLabel, self).__init__( **kwargs)

class RightLabel( Label):
    def __init__( self, **kwargs):
        super( RightLabel, self).__init__( **kwargs)
        
class LeftButton( Button):
    def __init__( self, **kwargs):
        super( LeftButton, self).__init__( **kwargs)
        
class SpinnerOpts( SpinnerOption):
    def __init__( self, **kwargs):
        super( SpinnerOpts, self).__init__( **kwargs)
    
class LeftSpinner( Spinner):
    def __init__( self, **kwargs):
        super( LeftSpinner, self).__init__( option_cls=SpinnerOpts, **kwargs)
        
class PlaintextSepChooser( BoxLayout):
    '''
    popup for chosing plaintext separator
    '''
    def __init__( self, cancel_callback, next_callback, **kwargs):
        super( PlaintextSepChooser, self).__init__( **kwargs)
        
        self.ids['toggle_comma'].active = True
            
        self.ids['delim_other'].bind( focus=self.other_delim_focus)
        self.ids['cancel_button'].bind( on_press=cancel_callback)
        self.ids['next_button'].bind( on_press=next_callback)
        
    def other_delim_focus( self, textinput, value):
        if value:
            for k in self.ids.keys():
                if 'toggle' in k:
                    self.ids[k].active = False
                    
    def get_delim_choice( self):
        if self.ids['toggle_comma'].active:
            return ','
        elif self.ids['toggle_semicolon'].active:
            return ';'
        elif self.ids['toggle_space'].active:
            return ' '
        elif self.ids['toggle_tab'].active:
            return '\t'
        else:
            return self.ids['delim_other'].text
        
class PlaintextEncodingChooser( BoxLayout):
    '''
    popup for choosing plaintext encoding
    '''
    def __init__( self, cancel_callback, ok_callback, **kwargs):
        super( PlaintextEncodingChooser, self).__init__( **kwargs)
        
        self.orientation = 'vertical'
        
        encodings = App.get_running_app().backend.encodings

        dropdown = DropDown()
        for enc in encodings:
            btn = LeftButton( text=enc, size_hint=(1,None), height=row_height)
            btn.bind( on_release=lambda btn: dropdown.select( btn.text))
            dropdown.add_widget( btn)
        
        dropbtn = LeftButton( text=encodings[0], size_hint=(1,None), height=row_height)
        dropbtn.bind( on_release=dropdown.open)
        dropdown.bind(on_select=lambda instance, x: setattr(dropbtn, 'text', x))
        
        dropdown_box = BoxLayout( padding=('20dp','10dp'))
        dropdown_box.add_widget( dropbtn)
        self.add_widget( dropdown_box)
        self.dropbtn = dropbtn
        
        cancel_button = Button( text='Cancel')
        ok_button = Button( text='OK')
        
        cancel_button.bind( on_release=cancel_callback)
        ok_button.bind( on_release=ok_callback)
        
        button_box = BoxLayout( orientation='horizontal', padding=('20dp','10dp'))
        button_box.add_widget( cancel_button)
        button_box.add_widget( ok_button)
        
        self.add_widget( button_box)
        
class ErrorMsg( Popup):
    error_text = ObjectProperty(None)
    def __init__( self, error_text, title='Error...', **kwargs):
        self.error_text = error_text
        super( ErrorMsg, self).__init__( title=title, **kwargs)
        
class HelpMsg( Popup):
    help_text = ObjectProperty(None)
    def __init__( self, text, **kwargs):
        super( HelpMsg, self).__init__( **kwargs)
        self.help_text.text = text
        
class TkOpenDialog(): 
    def __init__( self, filetypes): 
        self.filetypes = filetypes
          
    def __enter__( self): 
        tkroot = tk.Tk()
        tkroot.title( 'Open...')
        tkroot.wm_attributes( '-topmost', 1)
        tkroot.geometry( '0x0+-2000+-2000')
        tkroot.update()
        self.tkroot = tkroot
        return self
      
    def get_filename( self):
        return filedialog.askopenfilename( filetypes=self.filetypes)
        
    def __exit__( self, exc_type, exc_value, exc_traceback): 
        self.tkroot.update()
        self.tkroot.destroy()
        self.tkroot.quit()
        
class TkSaveDialog():
    def __init__( self, initialfile, filetypes):
        self.initialfile = initialfile
        self.filetypes = filetypes
        
    def __enter__( self): 
        tkroot = tk.Tk()
        tkroot.title( 'Save As...')
        tkroot.wm_attributes( '-topmost', 1)
        tkroot.geometry( '0x0+-2000+-2000')
        tkroot.update()
        self.tkroot = tkroot
        return self
        
    def get_filename( self):
        return filedialog.asksaveasfilename( initialfile=self.initialfile, filetypes=self.filetypes)
        
    def __exit__( self, exc_type, exc_value, exc_traceback): 
        self.tkroot.update()
        self.tkroot.destroy()
        self.tkroot.quit()