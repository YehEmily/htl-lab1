"""
A Flask server that presents a minimal browsable interface for the Olin course catalog.

author: Oliver Steele <oliver.steele@olin.edu>
date  : 2017-01-18
license: MIT

contributor: Emily Yeh <emily.yeh@students.olin.edu>
date       : 2017-01-23
contributions:
(0) Made website look better (with background image made with GIMP)
(1) Added 'Return to Home' button to every page
(2) Changed instructor names format ('first last' instead of 'last, first')
(3) Added 'Back to Top' and 'Skip to Bottom' links to /area/... pages
(4) Added personal course pages for each course
(5) Added pages for instructors that list the courses they teach (with links to these courses)
"""

import os

import pandas as pd
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

courses = pd.read_csv('./data/olin-courses-16-17.csv')

@app.route('/health')
def health():
    return 'ok'

@app.route('/')
def home_page():
    return render_template('index.html', areas=set(courses.course_area), contacts=switch_names_in_set(set(courses.course_contact.dropna())))

@app.route('/area/<course_area>')
def area_page(course_area):
    return render_template('course_area.html', area=course_area, courses=courses[courses.course_area == course_area].iterrows())

@app.route('/instructor/<instructor_name>')
def instructor_page(instructor_name):
	unswitched_name = unswitch_name(instructor_name)
	return render_template('instructor_pages.html', name=switch_name(instructor_name), instructors=courses[courses.course_contact == unswitched_name].iterrows())

@app.route('/courses/<course_number>')
def course_page(course_number):
	return render_template('course_pages.html', course_number = course_number, current_course=courses[courses.course_number == course_number].iterrows())

def switch_name (contact):
	teachers = contact.split("; ")
	names = ""
	for teacher in teachers:
		parts = teacher.split(", ")
		if (len(parts) > 1):
			names += parts[1] + " " + parts[0] + "; "
		else:
			names += parts[0] + "; "
	return names[:-2]

def unswitch_name (contact):
	teachers = contact.split("; ")
	names = ""
	for teacher in teachers:
		parts = teacher.split()
		names += ", ".join(parts[::-1]) + "; "
	return names[:-2]

def switch_names_in_set (contacts_set):
	contacts = set()
	for contact in contacts_set:
		contacts.add(switch_name(contact))
	return contacts

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', debug=True, port=port)