from ctypes import windll
try:
    windll.user32.SetProcessDpiAwarenessContext(-4)
except:
    pass
import kivy
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.app import App
from kivy.metrics import dp,sp
from kivy.core.window import Window
from kivy.config import Config
from kivy.metrics import Metrics
from kivy.clock import Clock

from LoadPanel import LoadPanel
from NarrowByPanel import NarrowByPanel
from SearchConfigPanel import SearchConfigPanel
from AlsoComparePanel import AlsoComparePanel
from AppendPanel import AppendPanel
from ExportMatchesPanel import ExportMatchesPanel
from MatchBackend import MatchBackend

class MatchApp( App):
    '''
    this is the main app holding all panels/components
    '''
    
    def build( self):
        
        self.title = 'matchapp'
        
        self.backend = MatchBackend()
        
        self.panels = dict()
        
        # handles nav between different "screens"
        self.screenman = ScreenManager()
        
        self.add_panel( LoadPanel(), 'load_screen')
        self.add_panel( NarrowByPanel(), 'narrowby_screen')
        self.add_panel( SearchConfigPanel(), 'searchconfig_screen')
        self.add_panel( AlsoComparePanel(), 'alsocompare_screen')
        self.add_panel( AppendPanel(), 'append_screen')
        self.add_panel( ExportMatchesPanel(), 'exportmatches_screen')
        
        return self.screenman
        
    def add_panel( self, panel, name):
        screen = Screen( name=name)
        screen.add_widget( panel)
        self.screenman.add_widget( screen)
        self.panels[name] = panel
        
    def nav_to( self, screen, direction):
        self.screenman.transition.direction = direction
        self.screenman.current = screen
        
def main():
    Config.set( 'input', 'mouse', 'mouse,disable_multitouch') # section, option, value
    Window.size = (dp(800), dp(500))
    MatchApp().run()
    
if __name__ == '__main__':
    main()