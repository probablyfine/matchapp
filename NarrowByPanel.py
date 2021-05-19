from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.metrics import dp,sp
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from SharedComponents import LeftLabel, LeftSpinner, HelpMsg, ErrorMsg

Builder.load_string( '''
<ColumnMerger>:
    orientation: 'vertical'
    padding: '70dp','20dp'
    lrlbl: lrlbl
    left_box: left_box
    right_box: right_box
    cancel_btn: cancel_btn
    merge_btn: merge_btn
    BoxLayout:
        orientation: 'horizontal'
        padding: '5dp',0
        spacing: '20dp'
        size_hint_y: None
        height: '32dp'
        Label:
            markup: True
            text: '[u]Available Columns[/u]'
            font_size: '18sp'
            size_hint_x: 0.5
        Label:
            markup: True
            text: '[u]Selected Columns[/u]'
            font_size: '18sp'
            size_hint_x: 0.5
    BoxLayout:
        orientation: 'horizontal'
        spacing: '10dp'
        BoxLayout:
            padding: '5dp','5dp'
            canvas.before:
                Color:
                    rgba: 0, 0, 0, 1
                Rectangle:
                    pos: self.pos
                    size: self.size
            ScrollView:
                BoxLayout:
                    orientation: 'vertical'
                    id: left_box
                    size_hint_y: None
                    height: self.minimum_height
        Label:
            size_hint_x: None
            width: '20dp'
            text_size: self.size
            valign: 'middle'
            font_size: '20sp'
            id: lrlbl
        BoxLayout:
            padding: '5dp','5dp'
            canvas.before:
                Color:
                    rgba: 0, 0, 0, 1
                Rectangle:
                    pos: self.pos
                    size: self.size
            ScrollView:
                BoxLayout:
                    orientation: 'vertical'
                    id: right_box
                    size_hint_y: None
                    height: self.minimum_height
    BoxLayout:
        orientation: 'horizontal'
        padding: 0,'10dp'
        size_hint_y: None
        height: '50dp'
        Label:
            size_hint_x: None
            width: '170dp'
            text: 'New column name: '
        TextInput:
            multiline: False
            id: new_col_text
    BoxLayout:
        orientation: 'horizontal'
        padding: 0,'10dp'
        spacing: '20dp'
        size_hint_y: None
        height: '60dp'
        Button:
            text: 'Cancel'
            id: cancel_btn
        Button:
            text: 'Create Merged Column'
            id: merge_btn
            
<ColumnSelectSection>:
    lbl: lbl
    shape_lbl: shape_lbl
    dropdown: dropdown
    new_col_btn: new_col_btn
    padding: ('10dp','40dp')
    spacing: '45dp'
    orientation: 'vertical'
    BoxLayout:
        orientation: 'horizontal'
        spacing: '10dp'
        Label:
            id: lbl
            font_size: '16sp'
            size_hint_x: None
            width: self.texture_size[0]
        Label:
            id: shape_lbl
            font_size: '12sp'
            size_hint_x: None
            width: self.texture_size[0]
            
    BoxLayout:
        orientation: 'horizontal'
        spacing: '5dp'
        LeftSpinner:
            id: dropdown
            size_hint_y: None
            height: '32dp'
            font_size: '16sp'
        Button:
            id: new_col_btn
            text: 'Add merged column'
            font_size: '16sp'
            size_hint_x: None
            size_hint_y: None
            height: '32dp'
            width: '160dp'
        
<NarrowByPanel>:
    select_box: select_box
    back_btn: back_btn
    next_btn: next_btn
    orientation: 'vertical'
    padding: ('75dp','100dp')
    BoxLayout:
        orientation: 'horizontal'
        size_hint_y: 0.3
        LeftLabel:
            text: 'Select columns to use for match...'
            font_size: '22sp'
            valign: 'top'
            size_hint_x: 0.9
        Button:
            text: 'Help'
            size_hint_x: 0.1
            size_hint_y: 0.25
            pos_hint: {'center_y':1}
            on_release: root.show_help()
    BoxLayout:
        id: select_box
        orientation: 'vertical'
        size_hint_y: 0.5
        spacing: '30dp'
        padding: (0,'20dp')
    BoxLayout:
        orientation: 'horizontal'
        size_hint_y: 0.2
        spacing: '15dp'
        Button:
            id: back_btn
            text: 'Back'
            font_size: '16sp'
        Button:
            id: next_btn
            text: 'Next'
            font_size: '16sp'
''')

class ColumnMerger( BoxLayout):
    lrlbl = ObjectProperty(None)
    left_box = ObjectProperty(None)
    right_box = ObjectProperty(None)
    cancel_btn = ObjectProperty(None)
    merge_btn = ObjectProperty(None)
    def __init__( self, **kwargs):
        super( ColumnMerger, self).__init__( **kwargs)
        self.right_buttons = []
        self.left_buttons = []
        self.lrlbl.text = ' >\n <'
        
    def populate( self, columns):
        self.left_buttons = []
        for col in columns:
            self.left_buttons.append( Button( text=col, size_hint_y=None, height='32dp'))
        for w in self.left_buttons:
            w.bind( on_release=self.move_right)
            self.left_box.add_widget( w)
            
    def move_right( self, btn):
        self.left_box.remove_widget( btn)
        self.right_box.add_widget( btn)
        self.right_buttons.append( self.left_buttons.pop( self.left_buttons.index(btn)))
        btn.unbind( on_release=self.move_right)
        btn.bind( on_release=self.move_left)
        
    def move_left( self, btn):
        self.right_box.remove_widget( btn)
        self.left_box.add_widget( btn)
        self.left_buttons.append( self.right_buttons.pop( self.right_buttons.index(btn)))
        btn.unbind( on_release=self.move_left)
        btn.bind( on_release=self.move_right)
        
class ColumnSelectSection( BoxLayout):
    lbl = ObjectProperty(None)
    shape_lbl = ObjectProperty(None)
    dropdown = ObjectProperty(None)
    new_col_btn = ObjectProperty(None)
    def __init__( self, text, **kwargs):
        super( ColumnSelectSection, self).__init__( **kwargs)
        self.lbl.text = text
        
    def populate( self, columns):
        self.dropdown.text = columns[0]
        self.dropdown.values = columns
        
    def depopulate( self):
        self.dropdown.text = ''
        self.dropdown.values = []
        
class NarrowByPanel( BoxLayout):
    select_box = ObjectProperty(None)
    back_btn = ObjectProperty(None)
    next_btn = ObjectProperty(None)
    
    def __init__( self, **kwargs):
        super( NarrowByPanel, self).__init__( **kwargs)
        
        self.select_section1 = ColumnSelectSection( text='Column1:')
        self.select_section2 = ColumnSelectSection( text='Column2:')
        
        self.select_section1.new_col_btn.bind( on_release=lambda *args: self.show_col_merger( 1))
        self.select_section2.new_col_btn.bind( on_release=lambda *args: self.show_col_merger( 2))
        
        self.select_box.add_widget( self.select_section1)
        self.select_box.add_widget( self.select_section2)
        
        self.back_btn.bind( on_release=self.back_callback)
        self.next_btn.bind( on_release=self.next_callback)
        
    def show_col_merger( self, which):
        colm = ColumnMerger()
        app = App.get_running_app()
        if which == 1:
            cols = app.backend.columns1
        else:
            cols = app.backend.columns2
        colm.populate( cols)
        colm.which = which
        popup = Popup( title='Create merged column')
        colm.cancel_btn.bind( on_release=popup.dismiss)
        colm.merge_btn.bind( on_release=self.do_col_merge)
        popup.content = colm
        popup.open()
        self.merge_popup = popup
        
    def do_col_merge( self, *args):
        app = App.get_running_app()
        backend = app.backend
        colm = self.merge_popup.content
        if len( colm.right_buttons) < 2:
            _popup = ErrorMsg( error_text='Choose at least 2 columns to merge together.')
            _popup.open()
            return
        col = colm.ids.new_col_text.text
        if col == '':
            _popup = ErrorMsg( error_text='Enter a name for the merged column that will be created.')
            _popup.open()
            return
        try:
            if colm.which == 1:
                df = backend.grouper_helper.df1
            else:
                df = backend.grouper_helper.df2
            col_out = backend.merge_cols( df, [b.text for b in colm.right_buttons])
            new_col_name = col
            ndupe = 1
            while any(df.columns == new_col_name):
                new_col_name = col + '.' + str(ndupe)
                ndupe += 1
                if ndupe > 5000:
                    raise Exception( 'Maybe try a different name for the merged column?')
            df.insert( 0, new_col_name, col_out)
            if colm.which == 1:
                backend.columns1 = df.columns
                self.populate_dropdown1()
            else:
                backend.columns2 = df.columns
                self.populate_dropdown2()
            app.panels['alsocompare_screen'].reset_panel()
            app.panels['append_screen'].populate()
            self.merge_popup.dismiss()
        except Exception as error:
            self.merge_popup.dismiss()
            error_type = str(type(error)).split('\'')[1]
            error_msg  = error
            _popup = ErrorMsg( error_text='Error creating new column: {}. {}'.format( error_type, error_msg))
            _popup.open()
        
    def show_help( self):
        help_text = '''- Use the drop-down menus to select one column from each spreadsheet to use for matching.\n\n- These columns will be used to [b]identify the potential matches[/b] between the two sheets.\n\n- If needed, you can first create a [b]merged column[/b] from two or more existing columns. This is useful (for example) for combining FirstName+LastName, or Street+City+State+Zip.\n'''
        self._popup = HelpMsg( help_text, title='Help', size_hint=(0.85,0.65))
        self._popup.open()
        
    def populate_dropdowns( self):
        self.populate_dropdown1()
        self.populate_dropdown2()
        
    def populate_dropdown1( self):
        app = App.get_running_app()
        self.select_section1.populate( app.backend.columns1)
        nrows,ncols = app.backend.grouper_helper.df1.shape
        self.select_section1.lbl.text = app.backend.labels[0]
        self.select_section1.shape_lbl.text = f'({nrows} rows, {ncols} cols)'
        
    def populate_dropdown2( self):
        app = App.get_running_app()
        self.select_section2.populate( app.backend.columns2)
        nrows,ncols = app.backend.grouper_helper.df2.shape
        self.select_section2.lbl.text = app.backend.labels[1]
        self.select_section2.shape_lbl.text = f'({nrows} rows, {ncols} cols)'
        
    def back_callback( self, btn):
        self.select_section1.depopulate()
        self.select_section2.depopulate()
        app = App.get_running_app()
        app.backend.narrow_by = [None,None]
        app.nav_to( 'load_screen', 'right')
        
    def next_callback( self, btn):
        app = App.get_running_app()
        app.backend.narrow_by = [self.select_section1.dropdown.text, self.select_section2.dropdown.text] #overwrite, no issues with going back_btn
        app.nav_to( 'alsocompare_screen', 'left')
        
        