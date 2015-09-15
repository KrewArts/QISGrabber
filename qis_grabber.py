#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

"""qis_grabber: This script grabs your marks from the QIS/HIS site of the Hochschule für Telekommunikation Leipzig and displays them in stdout"""

__author__ = "Stephan Marschner"
__copyright__ = "Copyright 2015, Stephan Marschner"

__license__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "Stephan Marschner"
__email__ = "marschner.stephan@me.com"
__status__ = "alpha"


import requests, re, getpass

username = raw_input("Benutzername (e.g. 123456): ")
password = getpass.getpass("Passwort: ")
countExams = 0
countPassedExams = 0
countFailedExams = 0

# parameter for the post request
payload = {'state': 'user', 'type': '1', 'category': 'auth.login', 'startpage': 'qispos/notenspiegel/student', 'breadCrumbSource': 'qispos/notenspiegel/student', 'asdf': username, 'fdsa': password, 'submit': 'Anmelden'}

# create new .Session() object
s = requests.Session()

# requests a POST http request to login
req = s.post('https://qisweb.hispro.de/tel/rds', params = payload)

# checks if login was successful (hardcoded...)
if(req.headers['content-length'] > '2000'):
	ASIURL = s.get('https://qisweb.hispro.de/tel/rds?state=change&type=1&moduleParameter=studyPOSMenu&nextdir=change&next=menu.vm&subdir=applications&xml=menu&purge=y&navigationPosition=functions%2CstudyPOSMenu&breadcrumb=studyPOSMenu&topitem=functions&subitem=studyPOSMenu')

# gets the unique asi code for the marksview
	pattern = re.compile("amp;asi=(.*?)\"")
	asiRegex = re.search(pattern ,ASIURL.text)
	asi = asiRegex.group(1)

# requests a GET http request with the asi key
	MARKURL = s.get('https://qisweb.hispro.de/tel/rds?state=notenspiegelStudent&next=list.vm&nextdir=qispos/notenspiegel/student&createInfos=Y&struct=auswahlBaum&nodeID=auswahlBaum%7Cabschluss%3Aabschl%3DBA%2Cstgnr%3D1&expand=0&asi=' + asi)

# use regex to filter the important stuff (no., modul, semester, mark, status, ect, tries)
	patternMarks = re.compile("<.*?>\s+(\d{4})\s+<.*?>\s+<.*?>\s+(.*)\s+<.*?>\s+<.*?>\s+(.*)\s+<.*?>\s+<.*>\s+(.*?)\s+(?:<.*>\s+)?<.*?>\s+<.*?>\s+(.*)\s+<.*?>\s+<.*?>\s+(.*)\s+<.*>\s+<.*>\s+(.*)\s+<.*?>", re.MULTILINE)
	marksList = re.findall(patternMarks, MARKURL.text)

# parses the list with the found elements into a nicer form to view (not final!)
	for items in marksList:
		if(items[0] != "" and items[1] != "" and items[2] != "" and items[3] != "" and items[4] != "" and items[5] != "" and items[6] != ""):
			print("-----------")
			print('Prüfungsnummer: ' + str(items[0]))
			print('Modul: ' + items[1])
			print('Semester: ' + items[2])
			print('Note: ' + items[3])
			print('Status: ' + items[4])
			print('ECTs: ' + items[5])
			print('Versuche: ' + items[6])
# counter part for statistics
			countExams += 1
			if items[4] == "bestanden": countPassedExams += 1
			else: countFailedExams += 1
# print the statistics
	print("-----------\n|STATISTIK|\n-----------\nAnzahl aller Prüfungen: " + str(countExams))
	print("Anzahl bestandener Prüfungen: " + str(countPassedExams))
	print("Anzahl durchgefallener Prüfungen: " + str(countFailedExams))
else:
	print("WRONG USERNAME OR PASSWORD!")
