# coding: utf-8

import ui
import sound
from time import sleep
import threading

# main timer object, tracks the current round time
# runs in a seperate thread to avoid collision with the UI thread
class Timer(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		# initialize all params
		self.started = False
		self.work_time = 45
		self.rest_time = 5
		self.rounds = 8
		self.timer_value = 10; # setup time
		self.pause_event = threading.Event()

	def run(self):
		self.started = True
		
		# get the values entered into the UI
		s = v['work_slider']
		self.work_time = int(s.value*10)*5
		s = v['rest_slider']
		self.rest_time = int(s.value*10)*5
		s = v['rounds_slider']
		self.rounds = int(s.value*10)
		
		# get handle to timer and round number texts
		t = v['timer']
		r = v['rounds']

		# first do our setup time
		while self.timer_value > 0:
			if self.pause_event.is_set():
				sleep(1)
				
			while not self.pause_event.isSet() and self.timer_value > 0:
				t.text = str(self.timer_value)
				if self.timer_value < 4:
					sound.play_effect('game:Beep', 0.5)
				self.timer_value -= 1
				sleep(1)
		sound.play_effect('game:Ding_2', 0.5)
		
		# now each round
		while self.rounds > 0:
			r.text = "Rounds: " + str(self.rounds)
			self.rounds -= 1
			t.text = "Work"
			sleep(1)
			self.timer_value = self.work_time-1
			while self.timer_value > 0:
				if self.pause_event.isSet():
					sleep(1)
					
				while not self.pause_event.isSet() and self.timer_value > 0:
					t.text = str(self.timer_value)
					if self.timer_value < 4:
						sound.play_effect('game:Beep')
					self.timer_value -= 1
					sleep(1)
			sound.play_effect('game:Ding_2')
			
			t.text = "Rest"
			sleep(1)
			self.timer_value = self.rest_time-1
			while self.timer_value > 0:
				if self.pause_event.isSet():
					sleep(1)
					
				while not self.pause_event.isSet() and self.timer_value > 0:
					t.text = str(self.timer_value)
					if self.timer_value < 4:
						sound.play_effect('game:Beep')
					self.timer_value -= 1
					sleep(1)
			sound.play_effect('game:Ding_2')
		sound.play_effect('game:Ding_2')
		t.text = "Done!"
				
# allow popups while running
@ui.in_background

# executed when the work interval slider changes
def work_slider_moved(sender):
	# update the text above
	t = sender.superview['work_label']
	t.text = "Work Interval: " + str(int(sender.value*10)*5)

# executed when the rest interval slider changes
def rest_slider_moved(sender):
	# update the text above
	t = sender.superview['rest_label']
	t.text = "Rest Interval: " + str(int(sender.value*10)*5)

# executed when the rounds slider changes
def rounds_slider_moved(sender):
	# update the text above
	t = sender.superview['rounds_label']
	t.text = "Rounds: " + str(int(sender.value*10))
	t = sender.superview['rounds']
	t.text = "Rounds: " + str(int(sender.value*10))

# executed on start button press
def start_button_tapped(sender):
	# pass along a handle to the UI and start the timer
	if not MyTimer.started :
		MyTimer.start()
	else:
		MyTimer.pause_event.clear()

# executed on pause button press
def pause_button_tapped(sender):
	if MyTimer.started:
		MyTimer.pause_event.set()

# Main task, just build a new timer object and load the UI
MyTimer = Timer()
v = ui.load_view('Tabata')
if ui.get_screen_size()[1] >= 768:
	# iPad
	v.present('popover')
else:
	# iPhone
	v.present(orientations=['portrait'])
