import cherrypy
import urllib2
import urllib
import time
from subprocess import Popen, PIPE
import random
import os


class TTS():

	def convert_text_to_sound(self, text, file_name):
		with open(file_name, 'w') as f:
			sound_data = self.text_to_sound(text)
			f.write(sound_data)



class GoogleTranslate(TTS):

	EXTENSION = "mp3"

	def text_to_sound(self, text):
		opener = urllib2.build_opener()
		opener.addheaders = [('User-agent', 'Mozilla/5.0')]
		param_string = urllib.urlencode({
			"ie": "UTF-8",
			"tl": "en",
			"q": text.encode('utf-8'),
			})
		url = "http://translate.google.com/translate_tts?" + param_string
		response = opener.open(url)
		return response.read()



class Espeak(TTS):

	EXTENSION = "wav"

	def text_to_sound(self, text):
		espeak = Popen(["espeak", "--stdin", "--stdout"],
			stdin=PIPE,
			stdout=PIPE)
		(stdout, stderr) = espeak.communicate(input = text)
		return stdout



class SpeechServer(object):

	sounds_subdir = "sounds"
	text_subdir = "text"
	text_filename = "murmurs.txt"
	play_mp3_cmd = "mpg123"
	play_wav_cmd = "play"


	def __init__(self, tts_class):
		self.tts_class = tts_class


    	def index(self, text):
		self._create_directories()
		cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'
		with open(self._transcript_path(), "a") as transcript:
			utf_text = text.encode('utf-8')
			tts = self.tts_class()
			filename = self._make_file_path()
			transcript.write("%s %s\n" % (filename, utf_text))
			tts.convert_text_to_sound(text, filename)
			self._play(filename)

	def ping(self):
		return "pong"

	def _make_file_path(self):
		rand = random.randint(0,1000)
		t = time.strftime("%Y_%m_%d_%H_%m_%S", time.localtime())
		filename ="%s__%03d.%s" % (t, rand, self.tts_class.EXTENSION)
		return os.path.join(self.sounds_subdir, filename)


	def _transcript_path(self):
		return os.path.join(self.text_subdir, self.text_filename)


	def _play(self, filename):
		if filename.endswith("wav"):
			play_cmd = self.play_wav_cmd
		else:
			play_cmd = self.play_mp3_cmd
		os.system("%s %s </dev/null" % (play_cmd, filename))

	def _create_directories(self):
		for directory in [self.sounds_subdir, self.text_subdir]:
			if not os.path.exists(directory):
				os.mkdir(directory)


    	index.exposed = True
    	ping.exposed = True



if __name__ == "__main__":
	cherrypy.config.update({
		'server.socket_host': '0.0.0.0',
		'server.socket_port': 8000,
		})
	#tts_class = Espeak
	tts_class = GoogleTranslate
	server = SpeechServer(tts_class)
	if cherrypy.__version__.startswith("2"):
		cherrypy.root = server
		cherrypy.server.start()
	else:
		cherrypy.quickstart(server)
