from kivy.lang.builder import Builder
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen,ScreenManager
from kivy.core.window import Window
from kivy.metrics import dp
from kivymd.uix.button import MDIconButton
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from kivy.graphics.texture import Texture
from kivy.properties import StringProperty, NumericProperty
import connection as conn
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivymd.uix.menu import MDDropdownMenu
import pyaudio
import wave
import threading
import subprocess


import time, cv2 as cv
import os
from kivy.config import Config
Config.set('graphics', 'maxfps', 0)



Window.size = (300, 500)


screen_helper="""
ScreenManager:
    LoginPage:
    MainPage:
<SearchWidget@Screen>:
    MDTextField:
        hint_text: "Enter username"
        helper_text: "Forgot Username"
        helper_text_mode: "on_focus"
        pos_hint: {"x": 0.05, "y": 0.85}
        size_hint_x: 0.9

<CameraClick>:
    orientation: 'vertical'
    Camera:
        id: camera
        resolution: (640, 480)
    BoxLayout:
        orientation: "horizontal"
        MDFloatingActionButton:
            icon: "camera"
            on_press: root.capture()
        MDFloatingActionButton:
            icon: "incognito"

<LoginPage>:
    name: "login_page"
    MDCard:
        size_hint: None, None
        size: 300, 400
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        elevation: 10
        padding: 25
        spacing: 25
        orientation: 'vertical'

        MDLabel:
            id: welcome_label
            text: "WELCOME"
            font_size: 40
            halign: 'center'
            size_hint_y: None
            height: self.texture_size[1]
            padding_y: 15

        MDTextFieldRound:
            id: user
            hint_text: "username"
            icon_right: "account"
            size_hint_x: None
            width: 200
            font_size: 18
            pos_hint: {"center_x": 0.5}

        MDTextFieldRound:
            id: password
            hint_text: "password"
            icon_right: "eye-off"
            size_hint_x: None
            width: 200
            font_size: 18
            pos_hint: {"center_x": 0.5}
            password: True

        MDRoundFlatButton:
            text: "LOG IN"
            font_size: 12
            pos_hint: {"center_x": 0.5}
            on_press: root.verify_credentials()

        MDRoundFlatButton:
            text: "CLEAR"
            font_size: 12
            pos_hint: {"center_x": 0.5}
            on_press: app.clear()

        Widget:
            size_hint_y: None
            height: 10

<MainPage>:
    name: "main_page"
    BoxLayout:
        orientation: "vertical"
        md_bg_color: app.theme_cls.primary_color
        MDToolbar:
            title: "P R E S E N D"
            elevation: 20
        MDBottomNavigation:
            MDBottomNavigationItem:
                name: "home"
                icon: "home"
                BoxLayout:
                    orientation: "horizontal"
                    Button:
                    Button:
            MDBottomNavigationItem:
                name: "explore"
                icon: "search-web"
                SearchWidget:
            MDBottomNavigationItem:
                name: "record"
                icon: "plus"
                CameraClick:
                Slider:
                    orientation: "vertical"
                    min: 0
                    max: 2
                    step: 1
                    value: 1
                    pos_hint: {"center_x": 0.1, "center_y": 0.6}
                    size_hint: 0.5, 0.5

            MDBottomNavigationItem:
                name: "notification"
                icon: "bell"
                BoxLayout:
                    orientation: "horizontal"
                    Button:
                    Button:
                    Button:
                    Button:
            MDBottomNavigationItem:
                name: "profile"
                icon: "face-profile"
                BoxLayout:
                    orientation: "vertical"
                    FloatLayout:
                        canvas:
                            Color:
                                rgb: 1, 1, 1
                            Ellipse:
                                pos: self.width/2.7, self.height*2.7
                                size: 75, 75
                                source: "galaxy/images/bg1.jpg"
                                angle_start: 0
                                angle_end: 360
                        # MDIconButton:
                        #     id: settings
                        #     icon: "account-settings"
                        #     pos_hint: {"center_x": 0.93, "center_y": 0.8}
                        #     on_press: root.drop()

                    BoxLayout:
                        orientation: "horizontal"
                        MDLabel:
                            text: "Recordings"
                        MDLabel:
                            text: "Followers"
                        MDLabel:
                            text: "Following"
                    # BoxLayout:
                    #     orientation: "horizontal"
                    #     MDLabel:
                    #         text: root.my_recordings
                    #     MDLabel:
                    #         text: root.my_followers
                    #     MDLabel:
                    #         text: root.my_following

                    Button:
                    Button:

"""
class MainPage(Screen):
    pass
    # def on_kv_post(self, base_widget):
    #     settings = self.ids.settings
    #     self.dropdown = MDDropdownMenu(settings=settings, items=[{"viewclass": "MDMenuItem", "text": "Settings"}, {"viewclass": "MDMenuItem", "text": "Logout"}], width_mult=4)

    # def drop(self):
    #     self.dropdown.open()
class LoginPage(Screen):
    def verify_credentials(self):
        #check if loggedIn is yes from database
        if self.ids["user"].text == "user" and self.ids["password"].text == "pass":
            self.manager.current = "main_page"

class CameraClick(BoxLayout):
    def capture(self):
        '''
        Function to capture the images and give them the names
        according to their captured time and date.
        '''
        camera = self.ids['camera']
        timestr = time.strftime("%Y%m%d_%H%M%S")
        camera.export_to_png("IMG_{}.png".format(timestr))

class Users():
    mycursor = conn.db.cursor()
    # mycursor.execute("SELECT * FROM users WHERE username = %s", loggedInUser)

    def recording_count(self):
        pass
        # return result

    def followers(self):
        pass
    def following(self):
        pass

class VideoRecorder():
	# Video class based on openCV
	def __init__(self):

		self.open = True
		self.device_index = 0
		self.fps = 6               # fps should be the minimum constant rate at which the camera can
		self.fourcc = "mp4v"       # capture images (with no decrease in speed over time; testing is required)
		self.frameSize = (640,480) # video formats and sizes also depend and vary according to the camera used
		self.video_filename = "temp_video.mp4"
		self.video_cap = cv.VideoCapture(self.device_index, cv.CAP_DSHOW)
		self.video_writer = cv.VideoWriter_fourcc(*self.fourcc)
		self.video_out = cv.VideoWriter(self.video_filename, self.video_writer, self.fps, self.frameSize)
		self.frame_counts = 1
		self.start_time = time.time()

	# Video starts being recorded
	def record(self):
		while self.open:
			ret, video_frame = self.video_cap.read()
			if ret:

					self.video_out.write(video_frame)
					self.frame_counts += 1
					time.sleep(0.16)

					cv.imshow('video_frame', video_frame)
					cv.waitKey(1)
			else:
				break

				# 0.16 delay -> 6 fps


	# Finishes the video recording therefore the thread too
	def stop(self):

		if self.open:

			self.open=False
			self.video_out.release()
			self.video_cap.release()
			cv.destroyAllWindows()


	# Launches the video recording function using a thread
	def start(self):
		video_thread = threading.Thread(target=self.record)
		video_thread.start()


class AudioRecorder():
    # Audio class based on pyAudio and Wave
    def __init__(self):

        self.open = True
        self.rate = 44100
        self.frames_per_buffer = 1024
        self.channels = 2
        self.format = pyaudio.paInt16
        self.audio_filename = "temp_audio.wav"
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=self.format,
                                      channels=self.channels,
                                      rate=self.rate,
                                      input=True,
                                      frames_per_buffer = self.frames_per_buffer)
        self.audio_frames = []


    # Audio starts being recorded
    def record(self):

        self.stream.start_stream()
        while(self.open == True):
            data = self.stream.read(self.frames_per_buffer)
            self.audio_frames.append(data)
            if self.open==False:
                break


    # Finishes the audio recording therefore the thread too
    def stop(self):

        if self.open==True:
            self.open = False
            self.stream.stop_stream()
            self.stream.close()
            self.audio.terminate()

            waveFile = wave.open(self.audio_filename, 'wb')
            waveFile.setnchannels(self.channels)
            waveFile.setsampwidth(self.audio.get_sample_size(self.format))
            waveFile.setframerate(self.rate)
            waveFile.writeframes(b''.join(self.audio_frames))
            waveFile.close()

    # Launches the audio recording function using a thread
    def start(self):
        audio_thread = threading.Thread(target=self.record)
        audio_thread.start()


def start_AVrecording(filename):

	global video_thread
	global audio_thread

	video_thread = VideoRecorder()
	audio_thread = AudioRecorder()

	audio_thread.start()
	video_thread.start()

	return filename




def start_video_recording(filename):

	global video_thread

	video_thread = VideoRecorder()
	video_thread.start()

	return filename


def start_audio_recording(filename):

	global audio_thread

	audio_thread = AudioRecorder()
	audio_thread.start()

	return filename




def stop_AVrecording(filename):

	audio_thread.stop()
	frame_counts = video_thread.frame_counts
	elapsed_time = time.time() - video_thread.start_time
	recorded_fps = frame_counts / elapsed_time
	print( "total frames " + str(frame_counts))
	print( "elapsed time " + str(elapsed_time))
	print( "recorded fps " + str(recorded_fps))
	video_thread.stop()

	# Makes sure the threads have finished
	while threading.active_count() > 1:
		time.sleep(1)


#	 Merging audio and video signal

	if abs(recorded_fps - 6) >= 0.01:    # If the fps rate was higher/lower than expected, re-encode it to the expected

		cmd = "ffmpeg -r " + str(recorded_fps) + " -i temp_video.mp4 -pix_fmt yuv420p -r 6 temp_video2.mp4"
		subprocess.call(cmd, shell=True)

		cmd = "ffmpeg -ac 2 -channel_layout stereo -i temp_audio.wav -i temp_video2.mp4 -pix_fmt yuv420p " + filename + ".mp4"
		subprocess.call(cmd, shell=True)

	else:

		cmd = "ffmpeg -ac 2 -channel_layout stereo -i temp_audio.wav -i temp_video.mp4 -pix_fmt yuv420p " + filename + ".mp4"
		subprocess.call(cmd, shell=True)


# Required and wanted processing of final files
def file_manager(filename):

	local_path = os.getcwd()

	if os.path.exists(str(local_path) + "/temp_audio.wav"):
		os.remove(str(local_path) + "/temp_audio.wav")

	if os.path.exists(str(local_path) + "/temp_video.mp4"):
		os.remove(str(local_path) + "/temp_video.mp4")

	if os.path.exists(str(local_path) + "/temp_video2.mp4"):
		os.remove(str(local_path) + "/temp_video2.mp4")

	if os.path.exists(str(local_path) + "/" + filename + ".mp4"):
		os.remove(str(local_path) + "/" + filename + ".mp4")


class PresendApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Red"
        screen = Builder.load_string(screen_helper)
        return screen

    def logger(self):
	    self.root.ids.welcome_label.text = f'Sup {self.root.ids.user.text}!'

    def clear(self):
	    self.root.ids.welcome_label.text = "WELCOME"
	    self.root.ids.user.text = ""
	    self.root.ids.password.text = ""


    #def submit:
        #saves info to user
#The variable __name__ for the file/module that is run will be always __main__(i.e., main.py)
#But the __name__ variable for all other modules that are being imported will be set to their module's name.

if __name__ == "__main__":
    PresendApp().run()