from django.test import TestCase

# Create your tests here.
from myapp.views import do_algoritm
from myapp.models import FileData
from PIL import Image, ImageChops

def get_histogram_tested():
	hlist = []
	counter = 0
	while(True):
		try:
			im = Image.open(f"myapp/analysisfolder/tested_histogram/_TimeUsedforUrl_{counter}.png")
			counter += 1	
			hlist += [im]
		except:
			break
	return hlist

def get_histogram_generated():
	counter = 0
	hlist = []
	while(True):
		try:
			im = Image.open(f"myapp/analysisfolder/Luk_Virksomhed/Histogram/Alle_Bruger/URL_Tidsforbrug/_TimeUsedforUrl_{counter}.png")
			counter += 1
			hlist += [im]
		except:
			break
	return hlist

class HistogramTestCase(TestCase):
	def test_analysis_histogram_count(self):  # it must start with test
          """test that two nums add together"""
          myinput = {}
          myinput["csvSelected"] = 'myapp/analysisfolder/EasyData/EasyData_100.csv'


          do_algoritm(myinput, 'csvselect')
          tested_histograms = get_histogram_tested()
          generated_histograms = get_histogram_generated()
          print("len(tested_histograms):",len(tested_histograms))
          print("len(generated_histograms)",len(generated_histograms))
          self.assertEqual(len(tested_histograms), len(generated_histograms))

          # a = ImageChops.difference(hlist[0], image2)

          # self.asserEqual(, )
	def test_analysis_histogram(self):	
		tested_histograms = get_histogram_tested()
		generated_histograms = get_histogram_generated()
		for i in range(len(tested_histograms)):
			this_tested = tested_histograms[i]
			this_generated = generated_histograms[i]
			diff1 = ImageChops.difference(this_tested, this_generated)
			print("a",diff1.getextrema())
			expected_extrema = ((0, 0), (0, 0), (0, 0), (0, 0))
			self.assertEqual(diff1.getextrema(), expected_extrema)
