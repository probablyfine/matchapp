from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.metrics import dp,sp
from kivy.properties import ObjectProperty
from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder

from SharedComponents import LeftLabel,LeftSpinner,RightLabel,HelpMsg

Builder.load_string( '''
<CompareSection>:
    orientation: 'horizontal'
    padding: (0,'10dp')
    spacing: '10dp'
    size_hint_y: None
    height: '50dp'
    delete_btn: delete_btn
    drop1: drop1
    drop2: drop2
    Button:
        id: delete_btn
        text: 'Delete'
        size_hint: (None,None)
        height: '32dp'
        width: '60dp'
    RightLabel:
        size_hint_x: None
        width: '80dp'
        valign: 'middle'
        text: app.backend.labels[0]
    LeftSpinner:
        id: drop1
        size_hint: (1,None)
        height: '32dp'
        text: app.backend.columns1[0]
        values: app.backend.columns1
    RightLabel:
        size_hint_x: None
        width: '80dp'
        valign: 'middle'
        text: app.backend.labels[1]
    LeftSpinner:
        id: drop2
        size_hint: (1,None)
        height: '32dp'
        text: app.backend.columns2[0]
        values: app.backend.columns2
        
<AlsoComparePanel>:
    scroll_content: scroll_content
    compare_box: compare_box
    orientation: 'vertical'
    padding: ('30dp','30dp')
    BoxLayout:
        orientation: 'horizontal'
        size_hint_y: 0.1
        LeftLabel:
            text: 'Select additional columns to compare (optional)...'
            font_size: '22sp'
            valign: 'top'
            size_hint_x: 0.9
        Button:
            text: 'Help'
            size_hint_x: 0.1
            size_hint_y: 0.5
            pos_hint: {'center_y':0.75}
            on_release: root.show_help()
    ScrollView:
        size_hint_y: 0.75
        BoxLayout:
            id: scroll_content
            orientation: 'vertical'
            size_hint_y: None
            size_hint_x: 1
            BoxLayout:
                id: compare_box
                orientation: 'vertical'
                padding: (0,'10dp')
                size_hint_y: None
                size_hint_x: 1
            Button:
                text: 'Add'
                size_hint_y: None
                size_hint_x: None
                height: '32dp'
                width: '60dp'
                on_release: root.add_section()
    BoxLayout:
        orientation: 'horizontal'
        padding: (0,'10dp')
        size_hint_y: 0.15
        Button:
            text: 'Back'
            font_size: '16sp'
            pos_hint: {'center_y':0.25}
            on_release: root.back_callback()
        Button:
            text: 'Run Match'
            font_size: '16sp'
            pos_hint: {'center_y':0.25}
            on_release: root.next_callback()
''')

class CompareSection( BoxLayout):
    delete_btn = ObjectProperty(None)
    drop1 = ObjectProperty(None)
    drop2 = ObjectProperty(None)
    def __init__( self, delete_callback, root_id, **kwargs):
        super( CompareSection, self).__init__( **kwargs)
        self.delete_btn.bind( on_release=delete_callback)
        self.delete_btn.root_id = root_id
        
class AlsoComparePanel( BoxLayout):
    scroll_content = ObjectProperty(None)
    compare_box = ObjectProperty(None)
    def __init__( self, **kwargs):
        super( AlsoComparePanel, self).__init__( **kwargs)
        
        self.scroll_content.bind( minimum_height=self.scroll_content.setter('height'))
        self.compare_box.bind( minimum_height=self.compare_box.setter('height'))
        
        self.sections = dict()
        self.nsection = 0
        
    def show_help( self):
        help_text = '''- Optionally, select additional columns for matching. To add columns, press the [b]"Add..."[/b] button and use the drop-down menus to select a column from each sheet. You can add as many additional comparisons as you like.\n\n- If you use this feature, an [b]average similarity[/b] over all match columns will be used to rank matches. This average will be appended to the output.\n'''
        self._popup = HelpMsg( help_text, title='Help', size_hint=(0.75,0.6))
        self._popup.open()
        
    def add_section( self):
        section = CompareSection( self.delete_section, str(self.nsection))
        self.compare_box.add_widget( section)
        self.sections[str(self.nsection)] = section
        self.nsection += 1
        
    def delete_section( self, btn):
        self.compare_box.remove_widget( self.sections.pop( btn.root_id))
        
    def reset_panel( self):
        for k,v in self.sections.items():
            self.compare_box.remove_widget( v)
        self.sections = dict()
        self.nsection = 0
        
    def back_callback( self):
        App.get_running_app().nav_to( 'narrowby_screen', 'right')
        
    def next_callback( self):
        self._popup = Popup( size=('410dp','150dp'), size_hint=(None,None), auto_dismiss=False, title='Please wait')
        self._popup.content = Label( text='Working... this can take a long time for large files, and \n this window will stop responding until finished.')
        self._popup.open()
        
        # wait for popup to actually open before starting to load
        Clock.schedule_once( self.run_match, 0.1)
        
    def run_match( self, *args):
        self.set_also_compare()
        
        app = App.get_running_app()
        cols1 = [app.panels['narrowby_screen'].select_section1.dropdown.text]
        cols2 = [app.panels['narrowby_screen'].select_section2.dropdown.text]
        for k,v in self.sections.items():
            cols1.append( v.drop1.text)
            cols2.append( v.drop2.text)
        app.panels['append_screen'].set_match_cols( cols1, cols2) # this just sets which checkboxes are grayed out
        
        backend = app.backend
        
        backend.do_fast_match()
        backend.compare_columns()
        
        self._popup.dismiss()
        app.nav_to( 'append_screen', 'left')
        
    def set_also_compare( self):
        backend = App.get_running_app().backend
        
        also_compare = []
        for k,v in self.sections.items():
            if (backend.narrow_by[0] == v.drop1.text) and (backend.narrow_by[1] == v.drop2.text):
                continue
            also_compare.append( (v.drop1.text,v.drop2.text))
            
        backend.also_compare = also_compare #overwrite, no issues with going back through app