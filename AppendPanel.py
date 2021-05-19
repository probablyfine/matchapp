from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.checkbox import CheckBox
from kivy.metrics import dp,sp
from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from SharedComponents import LeftLabel,LeftSpinner,RightLabel,HelpMsg

Builder.load_string( '''
<AppendList>:
    scroll_box: scroll_box
    lbl: lbl
    padding: ('30dp',0)
    BoxLayout:
        orientation: 'vertical'
        padding: (0,'10dp')
        spacing: '5dp'
        LeftLabel:
            id: lbl
            valign: 'middle'
            font_size: '16sp'
            size_hint_y: None
            height: '32dp'
        BoxLayout:
            orientation: 'horizontal'
            spacing: '10dp'
            size_hint_y: None
            height: '32dp'
            Button:
                text: 'Select all'
                size_hint_y: None
                height: '32dp'
                on_release: root.select_all()
            Button:
                text: 'Select none'
                size_hint_y: None
                height: '32dp'
                on_release: root.select_none()
        ScrollView:
            BoxLayout:
                id: scroll_box
                orientation: 'vertical'
                size_hint_y: None
                padding: ('10dp','15dp')
                
<AppendPanel>:
    append_area: append_area
    orientation: 'vertical'
    padding: ('30dp','30dp')
    BoxLayout:
        orientation: 'horizontal'
        size_hint_y: 0.1
        LeftLabel:
            text: 'Select columns to append to output...'
            font_size: '22sp'
            valign: 'middle'
        Button:
            text: 'Help'
            size_hint_x: 0.1
            size_hint_y: 0.5
            pos_hint: {'center_y':0.75}
            on_release: root.show_help()
    BoxLayout:
        id: append_area
        orientation: 'horizontal'
        size_hint_y: 0.75
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
            text: 'Next'
            font_size: '16sp'
            pos_hint: {'center_y':0.25}
            on_release: root.next_callback()
''')

font_size = '16sp'
row_height = '32dp'

class AppendList( BoxLayout):
    scroll_box = ObjectProperty(None)
    lbl = ObjectProperty(None)
    def __init__( self, **kwargs):
        super( AppendList, self).__init__( **kwargs)
        
        self.scroll_box.bind( minimum_height=self.scroll_box.setter('height'))
        
        self.columns = {}
        
    def select_all( self):
        for k,v in self.columns.items():
            v.chk.active = True
    
    def select_none( self):
        for k,v in self.columns.items():
            if v.chk.disabled == False:
                v.chk.active = False
            
    def enable_all( self):
        for k,v in self.columns.items():
            v.chk.disabled = False
            
    def new_column( self, text):
        c = BoxLayout( orientation='horizontal', padding=(0,'5dp'), size_hint_y=None, height=row_height, size_hint_x=1)
        c.chk = CheckBox( active=False, size_hint_x=None, width='40dp')
        c.add_widget( c.chk)
        c.lbl = LeftLabel( text=text, valign='middle', font_size=font_size)
        c.add_widget( c.lbl)
        self.scroll_box.add_widget(c)
        return c
        
    def populate_columns( self, columns):
        self.depopulate_columns()
        self.columns = { t: self.new_column(t) for t in columns }
        
    def depopulate_columns( self):
        if len( self.columns) == 0:
            return
        for k,v in self.columns.items():
            self.scroll_box.remove_widget(v)
        self.columns = {}
    
class AppendPanel( BoxLayout):
    append_area = ObjectProperty(None)
    def __init__( self, **kwargs):
        super( AppendPanel, self).__init__( **kwargs)
        
        self.column_list1 = AppendList( size_hint_x=0.4)
        self.column_list2 = AppendList( size_hint_x=0.4)
        self.append_area.add_widget( self.column_list1)
        self.append_area.add_widget( self.column_list2)
        
    def show_help( self):
        help_text = '''- Use the check boxes on the [b]left[/b] and [b]right[/b] to select columns from each spreadsheet. [b]Checked columns will appear in the output[/b].\n\n- These columns will not be used for matching or ranking.\n\n- You cannot uncheck any column that was used for matching in a previous step.\n'''
        self._popup = HelpMsg( help_text, title='Help', size_hint=(0.75,0.6))
        self._popup.open()
        
    def populate( self):
        app = App.get_running_app()
        self.column_list1.populate_columns( app.backend.columns1)
        self.column_list2.populate_columns( app.backend.columns2)
        self.column_list1.lbl.text = app.backend.labels[0]
        self.column_list2.lbl.text = app.backend.labels[1]
        
    def back_callback( self):
        app = App.get_running_app()
        app.backend.reset_matches()
        app.nav_to( 'alsocompare_screen', 'right')
        
    def next_callback( self):
        self._popup = Popup( size=('410dp','150dp'), size_hint=(None,None), auto_dismiss=False, title='Please wait')
        self._popup.content = Label( text='Working... this can take a long time for large files, and \n this window will stop responding until finished.')
        self._popup.open()
        
        # wait for popup to actually open before starting to load
        Clock.schedule_once( self.do_append, 0.1)
            
    def do_append( self, obj):
        app = App.get_running_app()
        backend = app.backend
        
        backend.appends1 = [] # reset so going back through app doesn't break it
        backend.appends2 = [] # reset so going back through app doesn't break it
        for k,v in self.column_list1.columns.items():
            if v.chk.disabled:
                continue
            if v.chk.active:
                backend.append_column( 1, k)
                backend.appends1.append( k)
        for k,v in self.column_list2.columns.items():
            if v.chk.disabled:
                continue
            if v.chk.active:
                backend.append_column( 2, k)
                backend.appends2.append( k)
        
        self._popup.dismiss()
        
        self.nav_to_next()
        
    def set_match_cols( self, cols1, cols2):
        self.column_list1.enable_all()
        self.column_list1.select_none()
        for c in cols1:
            self.column_list1.columns[c].chk.disabled = True
            self.column_list1.columns[c].chk.active = True
            
        self.column_list2.enable_all()
        self.column_list2.select_none()
        for c in cols2:
            self.column_list2.columns[c].chk.disabled = True
            self.column_list2.columns[c].chk.active = True
        
    def nav_to_next( self):
        App.get_running_app().nav_to( 'exportmatches_screen', 'left')