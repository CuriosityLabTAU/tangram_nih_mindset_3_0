import os

from tangram_selection_not_using import *
from tangram_game import *

from zero_screen_room import *
from first_screen_room import *
from selection_screen_room import *
from solve_tangram_room import *
from party_screen_room import *
from game_facilitator import *

from text_handling import *

from interaction_control import *
from game import *
from tablet import *

from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import Layout
from kivy.uix.image import Image
from kivy.uix.dropdown import DropDown
from kivy.uix.spinner import Spinner
from kivy.lang import Builder
from kivy.base import runTouchApp
from kivy.clock import Clock
from kivy.app import App
from kivy.animation import Animation
from kivy.core.window import Window
from kivy_communication import *
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.audio import SoundLoader

from random import choice

try:
    from jnius import autoclass
    from android.runnable import run_on_ui_thread

    android_api_version = autoclass('android.os.Build$VERSION')
    AndroidView = autoclass('android.view.View')
    # AndroidPythonActivity = autoclass('org.renpy.android.PythonActivity')
    AndroidPythonActivity = autoclass('org.kivy.android.PythonActivity')

    Logger.debug(
        'Application runs on Android, API level {0}'.format(
            android_api_version.SDK_INT
        )
    )
except ImportError:
    def run_on_ui_thread(func):
        def wrapper(*args):
            Logger.debug('{0} called on non android platform'.format(
                func.__name__
            ))
        return wrapper


GAME_WITH_ROBOT = True  # False
ROBOT_SOUND_FROM_TABLET = False # False
#rinat
STUDY_SITE = 'MIT-JIBO'      #'TAU'      # MIT   #MIT-JIBO
ROBOT_TEXT = './tablet_app/robot_text/robot_text_long_w1.json'

class MyScreenManager (ScreenManager):
    the_tablet = None

# MyScreenManager:
#    SetupScreenRoom:
#    ZeroScreenRoom:
#    FirstScreenRoom:
#    SelectionScreenRoom:
#    SolveTangramRoom:r

root_widget = Builder.load_string('''

<SetupScreenRoom>:
    name: 'setup_screen_room'
    Widget:
        TextInput:
            id: roscore_ip
            name: 'roscore_ip'
            text: '192.168.122.1'
            text: '192.168.0.100'
            text: '192.168.0.105'
            text: '132.66.50.139'
            text: '132.66.198.164'
            text: '192.168.1.104'
            font_size: 16
            multiline: False
            size: root.width * 0.4, root.height * 0.07
            pos: root.width * 0.18, root.height * 0.8 - self.height * 0.5

        Button:
            id: connect_button
            name: 'connect_button'
            background_color: 0.1,0.5,0.2,1
            background_normal: ''
            text: 'Connect'
            font_size: 16
            size: root.width * 0.15, root.height * 0.07
            pos: root.width * 0.62, root.height * 0.8 - self.height * 0.5
            on_press: app.press_connect_button(roscore_ip.text)

<ZeroScreenRoom>:
    start_button: start_button
    subject_id: subject_id
    name: 'zero_screen_room'
    Widget:
        canvas.before:
            Color:
                rgba: 0.2,0.3,0.4,1
            Rectangle:
                pos: self.pos
                size: self.size
        Label:
            text: "Subject ID:"
            font_size:16
            size: root.width * 0.05, root.height * 0.07
            pos: root.width * 0.1, root.height * 0.8 - self.height * 0.5

        LoggedTextInput:
            id: subject_id
            name: 'subject_id'
            text: ''
            multiline: False
            font_size: 16
            size: root.width * 0.4, root.height * 0.07
            pos: root.width * 0.18, root.height * 0.8 - self.height * 0.5

        LoggedSpinner:
            id: condition_spinner
            text: 'condition'
            font_size: 16
            background_color: 0.2,0.2,0.2,1
            values: ('c-g-','c+g-','c-g+','c+g+')
            size: root.width * 0.15, root.height * 0.07
            pos: root.width * 0.62, root.height * 0.8 - self.height * 0.5
            on_text: app.condition_selected()

        LoggedButton:
            id: start_button
            name: 'start_button'
            background_color: 0.5,0.2,0.2,1
            background_normal: ''
            text: 'Start'
            font_size: 16
            size: root.width * 0.15, root.height * 0.07
            pos: root.width * 0.8, root.height * 0.8 - self.height * 0.5
            on_press: app.press_start_button()
       
        LoggedSpinner:
            id: world_spinner
            text: 'world (w1-w10)'
            font_size: 16
            background_color: 0.2,0.2,0.2,1
            values: ('w1','w2','w3','w4','w5','w6','w7','w8','w9','w10')
            size: root.width * 0.15, root.height * 0.07
            pos: root.width * 0.62, root.height * 0.7 - self.height * 0.5
            on_text: app.world_selected()
    
        # LoggedSpinner:
        #     id: gender_spinner
        #     text: 'gender'
        #     font_size: 16
        #     background_color: 0.2,0.2,0.2,1
        #     values: ('m','f')
        #     size: root.width * 0.15, root.height * 0.07
        #     pos: root.width * 0.62, root.height * 0.6 - self.height * 0.5
        #     on_text: app.gender_selected()
            
        LoggedButton:
            id: tega_sleep_button
            name: 'tega_sleep_button'
            background_color: 0.5,0.5,0.5,1
            background_normal: ''
            text: '- -'
            font_size: 16
            size: root.width * 0.15, root.height * 0.07
            pos: root.width * 0.08, root.height * 0.5 - self.height * 0.5
            on_press: app.press_robot_init()

        LoggedButton:
            id: goto_last_game_button
            name: 'goto_last_game_button'
            background_color: 0.5,0.5,0.5,1
            background_normal: ''
            text: 'continue'
            font_size: 16
            size: root.width * 0.15, root.height * 0.07
            pos: root.width * 0.08, root.height * 0.4 - self.height * 0.5
            on_press: app.press_load_transition('last_game')

        # LoggedButton:
        #     id: goto_game4_button
        #     name: 'goto_game4_button'
        #     background_color: 0.5,0.5,0.5,1
        #     background_normal: ''
        #     text: 'game4'
        #     font_size: 16
        #     size: root.width * 0.15, root.height * 0.07
        #     pos: root.width * 0.25, root.height * 0.4 - self.height * 0.5
        #     on_press: app.press_load_transition('game4')
        # 
        # LoggedButton:
        #     id: goto_game6_button
        #     name: 'goto_game6_button'
        #     background_color: 0.5,0.5,0.5,1
        #     background_normal: ''
        #     text: 'game6'
        #     font_size: 16
        #     size: root.width * 0.15, root.height * 0.07
        #     pos: root.width * 0.42, root.height * 0.4 - self.height * 0.5
        #     on_press: app.press_load_transition('game6')
        # 
        # LoggedButton:
        #     id: goto_game8_button
        #     name: 'goto_game8_button'
        #     background_color: 0.5,0.5,0.5,1
        #     background_normal: ''
        #     text: 'game8'
        #     font_size: 16
        #     size: root.width * 0.15, root.height * 0.07
        #     pos: root.width * 0.59, root.height * 0.4 - self.height * 0.5
        #     on_press: app.press_load_transition('game8')
        # 
        # LoggedButton:
        #     id: goto_game10_button
        #     name: 'goto_game10_button'
        #     background_color: 0.5,0.5,0.5,1
        #     background_normal: ''
        #     text: 'game10'
        #     font_size: 16
        #     size: root.width * 0.15, root.height * 0.07
        #     pos: root.width * 0.76, root.height * 0.4 - self.height * 0.5
        #     on_press: app.press_load_transition('game10')


<FirstScreenRoom>:
    name: 'first_screen_room'
    Widget:
        Image:
            id: background_image
            size: root.size
            pos: root.pos
            source: './tablet_app/images/worlds/w1/TangramGame_Open.png'
            allow_stretch: True
            keep_ratio: False
        LoggedButton:
            id: yes_button
            name: 'yes_button'
            borders: 2, 'solid', (1,1,0,1)
            background_normal: './tablet_app/images/worlds/w1/PriceBtn.png'
            background_down: './tablet_app/images/worlds/w1/PriceBtn_on.png'
            size: root.width * 0.25, root.height * 0.25
            pos: root.width * 0.5 - self.width * 0.5, root.height * 0.8 - self.height * 0.5
            on_press: app.press_yes_button()
            opacity: 0

<SelectionScreenRoom>:
    name: 'selection_screen_room'
    Widget:
        Image:
            id: background_image
            size: root.size
            pos: root.pos
            source: './tablet_app/images/worlds/w1/TangramGame_Selection.png'
            allow_stretch: True
            keep_ratio: False
        TangramSelectionWidget:
            id: tangram_selection_widget
        QuestionMarkWidget:
            id: question_mark_widget
            size: root.size
            pos: root.pos
        PricesWonWidget:
            id: prices_won_widget
            size: (root.size[0] * 0.7,root.size[1])
            pos: root.pos
        LoggedButton:
            id: stop_button
            name: 'stop_button'
            background_color: 0, 0, 0, 0
            #background_normal:  './tablet_app/images/reset_button.jpg'
            #background_down:  './tablet_app/images/reset_button_down.jpg'
            #border: (0,0,0,0)
            size: root.width * 0.03, root.width * 0.03
            pos: root.width * 0.98 - self.width * 0.5, root.height * 0.975 - self.height * 0.5
            on_press: app.press_stop_button()


<TangramSelectionWidget>
    name: 'tangram_selection_widget'

<PricesWonWidget>
    Image:
        id: price1
        size: root.width * 0.10, root.width * 0.10
        pos: root.width * 0.1, root.height * 0.85
        source: './tablet_app/images/Price_w1_1.gif'
        opacity: 0

    Image:
        id: price2
        size: root.width * 0.10, root.width * 0.10
        pos: root.width * 0.2, root.height * 0.85
        source: './tablet_app/images/Price_w1_2.gif'
        opacity: 0

    Image:
        id: price3
        size: root.width * 0.10, root.width * 0.10
        pos: root.width * 0.3, root.height * 0.85
        source: './tablet_app/images/Price_w1_3.gif'
        opacity: 0

    Image:
        id: price4
        size: root.width * 0.10, root.width * 0.10
        pos: root.width * 0.4, root.height * 0.85
        source: './tablet_app/images/Price_w1_1.gif'
        opacity: 0

    Image:
        id: price5
        size: root.width * 0.10, root.width * 0.10
        pos: root.width * 0.5, root.height * 0.85
        source: './tablet_app/images/Price_w1_2.gif'
        opacity: 0

    Image:
        id: price6
        size: root.width * 0.10, root.width * 0.10
        pos: root.width * 0.6, root.height * 0.85
        source: './tablet_app/images/Price_w1_3.gif'
        opacity: 0

    Image:
        id: price7
        size: root.width * 0.10, root.width * 0.10
        pos: root.width * 0.7, root.height * 0.85
        source: './tablet_app/images/Price_w1_1.gif'
        opacity: 0

    Image:
        id: price8
        size: root.width * 0.10, root.width * 0.10
        pos: root.width * 0.8, root.height * 0.85
        source: './tablet_app/images/Price_w1_2.gif'
        opacity: 0

    Image:
        id: price9
        size: root.width * 0.10, root.width * 0.10
        pos: root.width * 0.9, root.height * 0.85
        source: './tablet_app/images/Price_w1_3.gif'
        opacity: 0

    Image:
        id: price10
        size: root.width * 0.10, root.width * 0.10
        pos: root.width * 1, root.height * 0.85
        source: './tablet_app/images/Price_w1_1.gif'
        opacity: 0

    Image:
        id: price11
        size: root.width * 0.10, root.width * 0.10
        pos: root.width * 1.1, root.height * 0.85
        source: './tablet_app/images/Price_w1_2.gif'
        opacity: 0

    Image:
        id: price12
        size: root.width * 0.10, root.width * 0.10
        pos: root.width * 1.2, root.height * 0.85
        source: './tablet_app/images/Price_w1_3.gif'
        opacity: 0

<QuestionMarkWidget>
    Image:
        id: question_mark
        size: (root.size[0] * 0.175, root.size[1] * 0.18833)
        pos: root.width * 0.742, root.height * 0.24
        source: './tablet_app/images/worlds/w1/TangramGame_Selection.png'
        opacity: 1

<SolveTangramRoom>:
    name: 'solve_tangram_room'
    Widget:
        Background:
            id: background_widget
            size: root.size
            pos: root.pos
        TreasureBox:
            id: treasure_box
            size: root.size
            pos: root.pos
        HourGlassWidget:
            id: hourglass_widget
        TangramGameWidget:
            id: tangram_game_widget
        LoggedButton:
            id: stop_button
            name: 'stop_button'
            background_color: 0, 0, 0, 0
            #background_normal:  './tablet_app/images/reset_button.jpg'
            #background_down:  './tablet_app/images/reset_button_down.jpg'
            border: (0,0,0,0)
            size: root.width * 0.04, root.width * 0.04
            pos: root.width * 0.975 - self.width * 0.5, root.height * 0.970 - self.height * 0.5
            on_press: app.press_stop_button()

<Background>:
    Image:
        id: background_image
        size: root.size
        pos: root.pos
        source: './tablet_app/images/tangram_background.jpg'
        allow_stretch: True
        keep_ratio: False

<TreasureBox>:
    Image:
        name: 'treasure_box'
        id: box
        source: './tablet_app/images/TreasureBoxLayers_B.gif'
        allow_stretch: True
        keep_ratio: False
    Image:
        name: 'price'
        id: price
        allow_stretch: True
        keep_ratio: False
        opacity: 0

<HourGlassWidget>:
    name: 'hour_glass_widget'
    Image:
        id:topSand
        source: './tablet_app/images/sand.jpg'
        allow_stretch: True
        keep_ratio: False
    Image:
        id:middleSand
        source: './tablet_app/images/sand.jpg'
        allow_stretch: True
        keep_ratio: False
    Image:
        id:bottomSand
        source: './tablet_app/images/sand.jpg'
        allow_stretch: True
        keep_ratio: False
    Image:
        id: hourglass
        source: './tablet_app/images/hour_glass.gif'
        allow_stretch: True
        keep_ratio: False
        pos: self.pos
        size: self.size

<TangramGameWidget>:
    name: 'tangram_game_widget'

<PartyScreenRoom>:
    name: 'party_screen_room'
    Widget:
        PartyScreenBackground:
            id: party_screen_background
            size: root.size
            pos: root.pos
        PartyScreenPricesWidget:
            id: party_screen_prices_widget
            size: root.size
            pos: root.pos

<PartyScreenBackground>:
    Image:
        id: background_image
        size: root.size
        pos: root.pos
        source: './tablet_app/images/TangramGame_Open.jpg'
        allow_stretch: True
        keep_ratio: False

<PartyScreenPricesWidget>
    Image:
        id: price1
        size: root.width * 0.10, root.width * 0.10
        pos: root.width * 0.15, root.height * 0.56
        source: './tablet_app/images/Price_w1_1.gif'
        opacity: 1

    Image:
        id: price5
        size: root.width * 0.10, root.width * 0.10
        pos: root.width * 0.2, root.height * 0.54
        source: './tablet_app/images/Price_w1_2.gif'
        opacity: 1

    Image:
        id: price12
        size: root.width * 0.10, root.width * 0.10
        pos: root.width * 0.25, root.height * 0.53
        source: './tablet_app/images/Price_w1_3.gif'
        opacity: 1

    Image:
        id: price7
        size: root.width * 0.10, root.width * 0.10
        pos: root.width * 0.30, root.height * 0.52
        source: './tablet_app/images/Price_w1_1.gif'
        opacity: 1

    Image:
        id: price2
        size: root.width * 0.10, root.width * 0.10
        pos: root.width * 0.35, root.height * 0.52
        source: './tablet_app/images/Price_w1_2.gif'
        opacity: 1

    Image:
        id: price9
        size: root.width * 0.10, root.width * 0.10
        pos: root.width * 0.40, root.height * 0.52
        source: './tablet_app/images/Price_w1_3.gif'
        opacity: 1

    Image:
        id: price4
        size: root.width * 0.10, root.width * 0.10
        pos: root.width * 0.45, root.height * 0.52
        source: './tablet_app/images/Price_w1_1.gif'
        opacity: 1

    Image:
        id: price11
        size: root.width * 0.10, root.width * 0.10
        pos: root.width * 0.50, root.height * 0.52
        source: './tablet_app/images/Price_w1_2.gif'
        opacity: 1

    Image:
        id: price6
        size: root.width * 0.10, root.width * 0.10
        pos: root.width * 0.55, root.height * 0.53
        source: './tablet_app/images/Price_w1_3.gif'
        opacity: 1

    Image:
        id: price10
        size: root.width * 0.10, root.width * 0.10
        pos: root.width * 0.60, root.height * 0.53
        source: './tablet_app/images/Price_w1_1.gif'
        opacity: 1

    Image:
        id: price8
        size: root.width * 0.10, root.width * 0.10
        pos: root.width * 0.65, root.height * 0.54
        source: './tablet_app/images/Price_w1_2.gif'
        opacity: 1

    Image:
        id: price3
        size: root.width * 0.10, root.width * 0.10
        pos: root.width * 0.7, root.height * 0.55
        source: './tablet_app/images/Price_w1_3.gif'
        opacity: 1


''')

# functions connecting to button pressed
class SetupScreenRoom(Screen):
    ip=''

class TangramMindsetApp(App):
    tangrams_solved = 0
    interaction = None
    sounds = None
    current_sound = None
    current_action = None
    screen_manager = None
    current = None
    game = None
    selection = None
    text_handler = None
    tablet_disabled = False
    yes_clicked_flag = False
    subject_gender = "m"
    study_world = None

    filled_all_data = False
    filled_subject_id = False
    filled_world = False
    filled_gender = True
    filled_condition = False

    def build(self):

        self.interaction = Interaction(
            [('robot', 'RobotComponent'),
             ('child', 'ChildComponent'),
             ('internal_clock', 'ClockComponent'),
             ('hourglass', 'HourglassComponent')
             ]
        )
        self.interaction.components['tablet'] = TabletComponent(self.interaction, 'tablet')
        self.interaction.components['game'] = GameComponent(self.interaction, 'game')
        self.interaction.components['game'].game_facilitator = GameFacilitator()

        self.str_screen = SolveTangramRoom(self.interaction.components['tablet'])

        self.interaction.components['tablet'].hourglass_widget = self.str_screen.ids['hourglass_widget']
        # self.interaction.components['hourglass'].widget = s.ids['hourglass_widget']
        self.interaction.components['tablet'].app = self
        self.interaction.components['robot'].gender = ""
        if not GAME_WITH_ROBOT:
            self.interaction.components['robot'].app = self
            self.interaction.components['robot'].load_text(filename=ROBOT_TEXT) #added in order to play sound files

        else:
            self.interaction.components['robot'].load_text(filename=ROBOT_TEXT)
            if STUDY_SITE == 'MIT':
                self.interaction.components['robot'].robot_name = 'tega'
            elif STUDY_SITE == 'MIT-JIBO':
                self.interaction.components['robot'].robot_name = 'jibo'
            elif STUDY_SITE == 'TAU':
                self.interaction.components['robot'].robot_name = 'nao'
        self.interaction.load(filename='./tablet_app/general_transitions.json')
        self.interaction.load_sequence(filename='./tablet_app/general_sequence.json')
        self.interaction.next_interaction()

        self.load_sounds()
        self.screen_manager = MyScreenManager()

        self.screen_manager.add_widget(SetupScreenRoom())
        try:
            with open('last_ip' + '.pkl', 'rb') as f:
                ip_text = pickle.load(f)
                self.screen_manager.get_screen('setup_screen_room').ids['roscore_ip'].text = ip_text
        except IOError as e:
            print "Unable to open ip file, probably first run so file doesn't exist yet."
        self.screen_manager.current = 'setup_screen_room'

        return self.screen_manager

    def on_start(self):
        print ('app: on_start')
        self.android_set_hide_menu()
        TangramGame.SCALE = round(self.root_window.size[0] / 60)
        TangramGame.window_size = self.root_window.size

    def init_communication(self, ip_addr):
        local_ip = ip_addr
        # if STUDY_SITE == 'TAU':
        #     local_ip = ip_addr
        # elif STUDY_SITE == 'MIT':
        #     local_ip = ip_addr

        KC.start(the_parents=[self, self.interaction.components['robot']], the_ip=local_ip)
        KL.start(mode=[DataMode.file, DataMode.communication, DataMode.ros], pathname=self.user_data_dir, the_ip=local_ip)

    def on_connection(self):
        KL.log.insert(action=LogAction.data, obj='TangramMindsetApp', comment='start')

        self.zero_screen = ZeroScreenRoom(self)
        self.android_set_hide_menu()
        self.zero_screen.ids['subject_id'].bind(text=self.zero_screen.ids['subject_id'].on_text_change)
        self.zero_screen.ids['subject_id'].bind(text=self.subject_id_changed)
        self.screen_manager.add_widget(self.zero_screen)
        self.screen_manager.add_widget(FirstScreenRoom(self.interaction.components['tablet']))
        self.screen_manager.add_widget(SelectionScreenRoom(self.interaction.components['tablet']))
        self.screen_manager.add_widget(PartyScreenRoom(self.interaction.components['tablet']))
        self.screen_manager.add_widget(self.str_screen)

        self.screen_manager.current = 'zero_screen_room'

    def subject_id_changed(self, *args):
        print args
        if len(args[1]) > 0:
            self.filled_subject_id = True
            self.update_filled()

    def load_sounds(self):
        # load all the wav files into a dictionary whose keys are the expressions from the transition.json
        sound_list = ['introduction', 'click_price']

        sound_list = os.listdir("./tablet_app/sounds/wav_tangram") #['Selection_tutorial_all_0_question_f.wav', 'robot_lose_c+g+_2.wav', 'selection_tutorial_c+g-_0.wav', 'tangram_tutorial_all_0_faster.wav'...
        # sound_list = ['Selection_tutorial_all_0_question_f.wav', 'robot_lose_c+g+_2.wav', 'selection_tutorial_c+g-_0.wav',


        self.sounds = {}
        for s in sound_list:
            self.sounds[s] = SoundLoader.load("./tablet_app/sounds/wav_tangram/" + s)
            print("sound ",s," was loaded")
            #self.sounds[s] = SoundLoader.load("./tablet_app/sounds/" + s)
        self.current_sound = None

    def data_received(self, data):
        # receive pid, session, condition, start stage information
        #if self.screen_manager.current == "zero_screen_room":
        if True:
            if "pid" in data:
               self.screen_manager.current = "zero_screen_room"

            info = data.split(",")
            print info
            for i in info:
                print i
                if "pid" in i:
                    self.zero_screen.ids['subject_id'].text = i.split(":")[1]
                elif "condition" in i:
                    val = i.split(":")[1]
                    if val in self.zero_screen.ids['condition_spinner'].values:
                        self.zero_screen.ids['condition_spinner'].text = val
                elif "world" in i:
                    val = i.split(":")[1]
                    if val in self.zero_screen.ids['world_spinner'].values:
                        self.zero_screen.ids['world_spinner'].text = val
                elif "start" in i:
                    time.sleep(1)
                    self.press_start_button()
                elif "continue" in i:
                    time.sleep(1)
                    self.press_load_transition('last_game')

        print(self.name, data)
        #the_data = json.loads(data)
        #self.finished_expression(the_data[self.robot_name][1])

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Messages from robot to tablet to interaction
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def change_pieces(self, x):
        print('app changes pieces to ', x)
        # first, start to move the pieces on the tablet

        self.screen_manager.get_screen('solve_tangram_room').change_pieces(x)
        # put dynamic here!
        # XXXXXX RINAT XXX
        # ONLY WHEN THE PIECES FINISHED MOVING, then call the interaction with the line below.
        # time.sleep(1)
        # self.interaction.components['child'].on_action(['tangram_change', x])

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Messages from tablet to interaction
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def changed_pieces(self, x):
        # the robot finished changing the pieces
        print("tangram_mindset_app:changed_pieces",x)
        self.interaction.components['child'].on_action(['tangram_change', x])
        print("finished changed_pieces")

    def press_connect_button(self, ip_addr):
        # To-Do: save previous ip input
        print ip_addr

        with open('last_ip'+'.pkl', 'wb') as f:
            pickle.dump(ip_addr, f, pickle.HIGHEST_PROTOCOL)
        print('Finished saving ip')

        self.init_communication(ip_addr)

    def press_start_button (self):
        # child pressed the start button
        if (self.filled_all_data):
            self.interaction.components['child'].on_action(["press_start_button"])
        else:
            print ("please fill all the data")


    def press_robot_init (self):
        # put tega to sleep
        action_script = ["behavior_robot_init"]
        self.interaction.components['robot'].express(action_script)

    def press_load_transition(self, stage):
        if (self.filled_all_data):
            print("loading new transition file")

            with open('last_saved_state' + '.pkl', 'rb') as f:
                self.state = pickle.load(f)

            # self.gender = self.state['gender']
            # print('gender: ', self.gender)
            #
            #
            #
            # print('world: ', self.study_world)
            # state['world'] = self.study_world
            #
            # print('condition: ', self.condition)
            # state['condition'] = self.condition

            self.tangrams_solved = self.state['tnagram_solved']
            print('tangrams solved: ', self.tangrams_solved)
            # game_facilitator

            self.interaction.components['game'].game_facilitator.selection_gen.player = self.state['player']
            print('player: ', self.interaction.components['game'].game_facilitator.selection_gen.player)

            self.interaction.components['game'].game_facilitator.selection_gen.is_last_challenge = self.state['is_last_challenge']
            print(
            'is_last_challenge: ', self.interaction.components['game'].game_facilitator.selection_gen.is_last_challenge)

            self.interaction.components['game'].game_facilitator.selection_gen.challenge_counter = self.state['challenge_counter']
            print(
            'challenge_counter: ', self.interaction.components['game'].game_facilitator.selection_gen.challenge_counter)

            self.interaction.components['game'].game_facilitator.selection_gen.path_indexes = self.state['path_indexes']
            print('path_indexes: ', self.interaction.components['game'].game_facilitator.selection_gen.path_indexes)

            self.interaction.components['game'].game_facilitator.selection_gen.seen_puzzles = self.state['seen_puzzles']
            print('seen_puzzles: ', self.interaction.components['game'].game_facilitator.selection_gen.seen_puzzles)

            self.interaction.components['game'].game_facilitator.game_counter = self.state['game_counter']
            print('game_counter: ', self.interaction.components['game'].game_facilitator.game_counter)
            game_counter = self.interaction.components['game'].game_facilitator.game_counter

            self.interaction.components['game'].game_facilitator.current_player = self.state['current_player']
            print('current_player: ', self.interaction.components['game'].game_facilitator.current_player)

            # agent
            self.interaction.components['robot'].agent.current_round = self.state['current_round']
            print('current_round: ', self.interaction.components['robot'].agent.current_round)
            current_round = int(np.floor(self.state['current_interaction'] / 2))
            self.interaction.components['robot'].agent.current_round = current_round
            print('fixed current_round: ', current_round)

            # interaction
            self.interaction.current_interaction = self.state['current_interaction'] - 1
            print('current_interaction: ', self.interaction.current_interaction)

            TangramGame.cog_tangram_selection = self.state['cog_tangram_selection']
            print ('cog_tangram_selection: ', TangramGame.cog_tangram_selection)

            #games_played = int(stage.replace('game',''))-1

            # increase challenge_counter
            # if games_played > 6:
            #     self.interaction.components['game'].game_facilitator.selection_gen.challenge_counter += 1
            #     self.interaction.components['game'].game_facilitator.selection_gen.challenge_index += 1
            #
            # for i in range(games_played):
            #     self.interaction.components['game'].game_facilitator.update_game_result('S')
            #     print(self.interaction.components['game'].game_facilitator.selection_gen.current_level)
            #     self.tangrams_solved += choice([1,0])
            #
            # if games_played < 4:
            #     games_played += 1
            #
            # self.tangrams_solved = max(games_played/2, self.tangrams_solved)

            # filename = './tablet_app/worlds_sequences/sequence_' + self.study_world + '_' + stage + '.json'
            # filename = './tablet_app/worlds_sequences/sequence_w1_'+'counter_' + str(game_counter) + '.json'
            # self.interaction.load_sequence(filename=filename)
            self.interaction.next_interaction()
            #self.press_start_button()

    def press_yes_button(self):
        # child pressed the yes button
        if not self.yes_clicked_flag:
            self.interaction.components['child'].on_action(["press_yes_button"])
            self.yes_clicked_flag = True

    def press_treasure(self, treasure, dt=0):
        # child selected treasure (1/2/3)
        # print("press_treasure", treasure)
        #self.screen_manager.current_screen.show_selection(treasure)
        self.interaction.components['child'].on_action(['press_treasure', treasure])

    def tangram_move(self, x):
        # child moved a tangram piece (json of all the pieces)
        print(self.name, 'tangram_mindset_app: tangram_move', x)
        self.interaction.components['child'].on_action(['tangram_change', x])

    def tangram_turn (self, x):
        # child turned a tangram piece (json of all the pieces)
        print(self.name, 'tangram_mindset_app: tangram_turn', x)
        self.interaction.components['child'].on_action(['tangram_change', x])

    def check_solution(self, solution_json):
        # this function should not really be here
        print("tangram_mindset_app: check_solution", solution_json)
        return self.interaction.components['game'].game_facilitator.check_solution(solution_json)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Messages from interaction to tablet
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def first_screen(self):
        self.screen_manager.get_screen('first_screen_room').init_first_screen_room(the_app=self)
        self.screen_manager.current = 'first_screen_room'
        self.android_set_hide_menu()


    def party_screen(self):
        self.screen_manager.get_screen('party_screen_room').init_party(self, self.tangrams_solved)
        self.screen_manager.current = 'party_screen_room'
        self.android_set_hide_menu()


    def selection_screen(self, x):
        # Rinat: x is a list of tangrams from maor
        # you need to present all options with the tangram pieces

        # Maor: save game state for recovery
        print('Saving game state')
        # the
        state = {}

        # print('gender: ', self.gender)
        # state['gender'] = self.gender
        #
        # print('world: ', self.study_world)
        # state['world'] = self.study_world
        #
        # print('condition: ', self.condition)
        # state['condition'] = self.condition

        print('tangrams solved: ',self.tangrams_solved)
        state['tnagram_solved'] = self.tangrams_solved
        # game_facilitator
        print('player: ', self.interaction.components['game'].game_facilitator.selection_gen.player)
        state['player'] = self.interaction.components['game'].game_facilitator.selection_gen.player

        print('is_last_challenge: ', self.interaction.components['game'].game_facilitator.selection_gen.is_last_challenge)
        state['is_last_challenge'] = self.interaction.components['game'].game_facilitator.selection_gen.is_last_challenge

        print('challenge_counter: ', self.interaction.components['game'].game_facilitator.selection_gen.challenge_counter)
        state['challenge_counter'] = self.interaction.components['game'].game_facilitator.selection_gen.challenge_counter

        print('path_indexes: ', self.interaction.components['game'].game_facilitator.selection_gen.path_indexes)
        state['path_indexes'] = self.interaction.components['game'].game_facilitator.selection_gen.path_indexes

        print('seen_puzzles: ', self.interaction.components['game'].game_facilitator.selection_gen.seen_puzzles)
        state['seen_puzzles'] = self.interaction.components['game'].game_facilitator.selection_gen.seen_puzzles

        print('game_counter: ', self.interaction.components['game'].game_facilitator.game_counter)
        state['game_counter'] = self.interaction.components['game'].game_facilitator.game_counter

        print('current_player: ', self.interaction.components['game'].game_facilitator.current_player)
        state['current_player'] = self.interaction.components['game'].game_facilitator.current_player

        # agent
        print('current_round: ', self.interaction.components['robot'].agent.current_round)
        state['current_round'] = self.interaction.components['robot'].agent.current_round

        # interaction
        print('current_interaction: ', self.interaction.current_interaction)
        state['current_interaction'] = self.interaction.current_interaction

        print ('cog_tangram_selection: ', TangramGame.cog_tangram_selection)
        state['cog_tangram_selection'] = TangramGame.cog_tangram_selection

        with open('last_saved_state'+'.pkl', 'wb') as f:
            pickle.dump(state, f, pickle.HIGHEST_PROTOCOL)
        print('Finished saving game state')
        # Maor: end of save game state

        print('x=',x)
        TangramGame.SCALE = round(Window.size[0] / 75)
        self.screen_manager.get_screen('selection_screen_room').init_selection_options(x=x,the_app=self)
        self.screen_manager.current = 'selection_screen_room'
        self.android_set_hide_menu()

    def select_treasure(self,treasure):
        # robot selected treasure
        print ("select_treasure",treasure)
        print()
        self.screen_manager.current_screen.show_selection(treasure)
        Clock.schedule_once(lambda dt: self.press_treasure(treasure),1)

    def tangram_screen(self, x):
        # Rinat: x is a single tangram from maor
        # you need to present it and allow game
        print("tangram_screen",x)
        TangramGame.SCALE = round(Window.size[0] / 25)
        self.screen_manager.get_screen('solve_tangram_room').init_task(x, the_app=self)
        self.screen_manager.current = 'solve_tangram_room'
        self.android_set_hide_menu()

    def robot_express(self, action, expression):
        # robot is saying action
        print ('robot_express. action:', action, ', expression:', expression)
        self.current_action = action

        self.sound_filenames = []
        try:
            for name in expression[1:]:
                if name.lower() == name:
                    print('filename: ', name)
                    try_sound = name +'.wav'
                    #I am already doing this step of adding gender/world in robot.py
                    #try_sound_gender = name + '_' + self.gender + '.wav'
                    #try_sound_world = name + "_" + self.study_world + '.wav'
                    #try_sound_world_gender = name + "_" + self.study_world + '_' + self.gender + '.wav'
                    if (try_sound in self.sounds.keys()):
                        self.sound_filenames.append (try_sound)
                    #elif (try_sound_gender in self.sounds.keys()):
                    #    self.sound_filenames.append (try_sound_gender)
                    #elif (try_sound_world in self.sounds.keys()):
                    #    self.sound_filenames.append (try_sound_world)
                    #elif (try_sound_world_gender in self.sounds.keys()):
                    #    self.sound_filenames.append (try_sound_world_gender)
                    else:
                        print ("could not find filename", name)
                        self.finish_robot_express(0)
                    print ('sound_filenames = ', self.sound_filenames)

            if len(self.sound_filenames)>0:
                self.current_sound = 0
                self.play_next_sound()
            else:
                print("robot express: no sound to play")
                self.finish_robot_express()

        except:
            print ("unexpected error in robot_express:", sys.exc_info())

#Text to speech:
        # attempt tts
        #if self.text_handler.say(self.current_sound):
        #    self.finish_robot_express(0)

    def play_next_sound(self, *args):
        print("play_next_sound")
        sound_filename = self.sound_filenames[self.current_sound]
        sound = self.sounds[sound_filename]
        if self.current_sound + 1 < len(self.sound_filenames):
            sound.bind (on_stop = self.play_next_sound) #there are more than one sound file to be played
            self.current_sound += 1
        else:
            sound.bind(on_stop = self.finish_robot_express) #there is only one sound file to be played
        try:
            sound.play()
        except:
            print('problem playing sound:', sound_filename)
            print ("unexpected error:", sys.exc_info())
            self.finish_robot_express(0)

    def finish_robot_express (self, *args):
        #robot finished to talk
        self.playing = False
        print ('finish_robot_express', self, self.current_action)
        self.interaction.components['robot'].finished_expression(self.current_action)

    def yes(self):
        # yes price appear on the screen
        print ('yes in app')
        self.screen_manager.current_screen.ids['yes_button'].opacity = 1


    def solved(self):
        print ("trangram_mindset_app: solved")
        self.tangrams_solved += 1
        self.screen_manager.get_screen('solve_tangram_room').solved()

    def robot_solve(self, x):
        # robot is providing a solution sequence x, and solve_tangram_room animates this solution
        print ("tangram_mindset_app: robot_solve")

    def finish(self):
        # when time is up
        self.screen_manager.get_screen('solve_tangram_room').finish()

    # ~~~~~~ child-proofing ~~~~~~

    def disable_tablet(self):
        self.tablet_disabled = True
        self.screen_manager.current_screen.disable_widgets()

    def enable_tablet(self):
        self.tablet_disabled = False
        self.screen_manager.current_screen.enable_widgets()

    def update_condition(self, condition):
        self.filled_condition = True
        self.condition = condition
        self.update_filled()
        self.text_handler = TextHandler(condition)
        self.text_handler.load_text(filename=ROBOT_TEXT)
        self.interaction.components['robot'].agent.update_condition(condition)

    def update_gender(self, gender):
        self.filled_gender = True
        self.update_filled()
        self.gender = gender
        if 'MIT' in STUDY_SITE:
            self.subject_gender = ""
            self.interaction.components['robot'].gender = ""
        elif STUDY_SITE == 'TAU':
            self.subject_gender = gender
            self.interaction.components['robot'].gender = gender

    def update_world(self, world):
        self.filled_world  = True
        self.update_filled()

        if 'MIT' in STUDY_SITE:
            self.study_world = world
            self.interaction.components['game'].game_facilitator.selection_gen.load_dif_levels(world=world)
            self.interaction.components['robot'].agent.update_world(world)
            self.interaction.components['robot'].study_world = world
            self.interaction.load_sequence(
                filename='./tablet_app/worlds_sequences/sequence_' + self.study_world + '.json')
            self.interaction.next_interaction()
        elif STUDY_SITE == 'TAU':
            self.study_world = world
            self.interaction.components['game'].game_facilitator.selection_gen.load_dif_levels(world=world)
            self.interaction.components['robot'].agent.update_world(world)
            self.interaction.components['robot'].study_world = world
            self.interaction.load_sequence(filename='./tablet_app/worlds_sequences/sequence_' + self.study_world + '.json')
            self.interaction.next_interaction()

    def update_filled(self):
        self.filled_all_data = (self.filled_subject_id and self.filled_world and self.filled_gender and self.filled_condition)
        if self.filled_all_data:
            self.screen_manager.get_screen('zero_screen_room').ids['start_button'].background_color = (0.2, 0.5, 0.2, 1)
            self.screen_manager.get_screen('zero_screen_room').ids['goto_last_game_button'].background_color = (0.2, 0.5, 0.2, 1)
            # self.screen_manager.get_screen('zero_screen_room').ids['goto_game4_button'].background_color = (0.2, 0.5, 0.2, 1)
            # self.screen_manager.get_screen('zero_screen_room').ids['goto_game6_button'].background_color = (0.2, 0.5, 0.2, 1)
            # self.screen_manager.get_screen('zero_screen_room').ids['goto_game8_button'].background_color = (0.2, 0.5, 0.2, 1)
            # self.screen_manager.get_screen('zero_screen_room').ids['goto_game10_button'].background_color = (0.2, 0.5, 0.2, 1)
            print ("all is filled")

            #self.screen_manager.get_screen('zero_screen_room').ids['start_button'].text = "OK"

    def press_stop_button(self):
        print('stop button pressed')
        #if self.screen_manager.current == "solve_tangram_room":
        self.interaction.components['hourglass'].stop()
        #    self.interaction.current_interaction -= 1
        self.interaction.end_interaction()

    def difficulty_selected(self):
        difficulty = self.screen_manager.get_screen('zero_screen_room').ids['difficulty_spinner'].text
        self.interaction.components['game'].game_facilitator.selection_gen.load_dif_levels(difficulty)

    def condition_selected(self):
        #NOW MOVED TO ADD AND NAMED condition_selection
        print("condition_selected")
        condition = self.screen_manager.get_screen('zero_screen_room').ids['condition_spinner'].text
        #self.the_app.update_condition(condition)
        self.update_condition(condition)
        print(condition)

    def world_selected(self):
        #NOW MOVED TO ADD AND NAMED condition_selection
        print("world_selected")
        world = self.screen_manager.get_screen('zero_screen_room').ids['world_spinner'].text
        #self.the_app.update_condition(condition)
        self.update_world(world)
        print(world)

    def gender_selected(self):
        #NOW MOVED TO ADD AND NAMED condition_selection
        print("gender_selected")
        gender = self.screen_manager.get_screen('zero_screen_room').ids['gender_spinner'].text
        #self.the_app.update_condition(condition)
        self.update_gender(gender)
        print(gender)


    @run_on_ui_thread
    def android_set_hide_menu(self):
        if android_api_version.SDK_INT >= 19:
            Logger.debug('API >= 19. Set hide menu')
            view = AndroidPythonActivity.mActivity.getWindow().getDecorView()
            view.setSystemUiVisibility(
                AndroidView.SYSTEM_UI_FLAG_LAYOUT_STABLE |
                AndroidView.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION |
                AndroidView.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN |
                AndroidView.SYSTEM_UI_FLAG_HIDE_NAVIGATION |
                AndroidView.SYSTEM_UI_FLAG_FULLSCREEN |
                AndroidView.SYSTEM_UI_FLAG_IMMERSIVE_STICKY
            )

if __name__ == "__main__":
    TangramMindsetApp().run()
