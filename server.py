"""
A Flask server that presents a minimal browsable interface for the Olin course catalog.

author: Oliver Steele <oliver.steele@olin.edu>
date  : 2017-01-18
license: MIT
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
    return render_template('index.html', areas=set(courses.course_area), contacts=set(courses.course_contact.dropna()))

@app.route('/area/<course_area>')
def area_page(course_area):
    return render_template('course_area.html', area=course_area, courses=courses[courses.course_area == course_area].iterrows())

@app.route('/instructor/<instructor_name>')
def instructor_page(instructor_name):
	return render_template('instructor_pages.html', name=instructor_name, instructors=courses[courses.course_contact == instructor_name].iterrows())

@app.route('/courses/<course_number>')
def course_page(course_number):
	return render_template('course_pages.html', current_course=courses[courses.course_number == course_number].iterrows())

if __name__ == '__main__':
    app.run(debug=True)

# Add area descriptions to the Course Area pages.
# Bring these in from a CSV or other data file, and get the values to the template file.