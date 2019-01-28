import json
import urllib.request

from flask import Flask, render_template
from flask import request

app = Flask(__name__)

@app.route('/')
def main():
    inst1 = request.args.get('inst1', None)
    inst2 = request.args.get('inst2', None)
    major = request.args.get('major', 0)

    inst_names = []
    

    if inst1 is not None and inst2 is not None:
        matches = get_similar_courses(inst1, inst2, major)
        inst_names.append(getSchoolName(inst1))
        inst_names.append(getSchoolName(inst2))
    else:
        matches = []
        inst_names.append('') 
        inst_names.append('')


    return render_template('index.html', similar_course_info=matches, inst1 = inst_names[0], inst2 = inst_names[1])

@app.route('/<path:path>')
def static_file(path):
    return app.send_static_file(path)

def getDataSet(school_id, discipline_id) :
        url_pattern = 'https://www.c-id.net/api/v1/course/by-school?draw=1&columns[0][data]=cid_abbreviation&columns[0][name]=&columns[0][searchable]=true&columns[0][orderable]=true&columns[0][search][value]=&columns[0][search][regex]=false&columns[1][data]=cid_name&columns[1][name]=&columns[1][searchable]=true&columns[1][orderable]=true&columns[1][search][value]=&columns[1][search][regex]=false&columns[2][data]=course_num&columns[2][name]=&columns[2][searchable]=true&columns[2][orderable]=true&columns[2][search][value]=&columns[2][search][regex]=false&columns[3][data]=course_name&columns[3][name]=&columns[3][searchable]=true&columns[3][orderable]=true&columns[3][search][value]=&columns[3][search][regex]=false&columns[4][data]=cor_effective_date&columns[4][name]=&columns[4][searchable]=true&columns[4][orderable]=true&columns[4][search][value]=&columns[4][search][regex]=false&order[0][column]=0&order[0][dir]=asc&start=0&length=1000&search=&group_by=articulation&count=1000&page=1&sort_direction=asc&sort_field=cid_abbreviation&school_id={}&school_type_id=1&discipline_id={}&approved_from_month=&approved_from_day=&approved_from_year=&approved_to_month=&approved_to_day=&approved_to_year=&_=1547919457909'
        url = url_pattern.format(school_id, discipline_id)
        contents = urllib.request.urlopen(url).read()
        return json.loads(contents)['data']

def getSchoolName(school_id) :
    dataset = getDataSet(school_id, 0)
    return dataset[0]['school_name']

def get_course_ids(data): #extracts all C-ID tagged data from JSON into set
        course_ids = set()
        for course in data:
            course_ids.add(course['cid_number'])
        return course_ids

def array_to_object(data): #college data is tagged with course C-ID 
        obj = {}
        for course in data:
            obj[course['cid_number']] = course
        return obj

def get_similar_courses(inst1, inst2, major):
 
    data1 = getDataSet(inst1, major) 
    data2 = getDataSet(inst2, major)

    college1_course_ids = get_course_ids(data1)
    college2_course_ids = get_course_ids(data2)

    common_courses = college1_course_ids.intersection(college2_course_ids) #obtains courses with same C-ID 
    sorted_common_courses = sorted(common_courses)

    c_1 = array_to_object(data1)
    c_2 = array_to_object(data2)

    results = []

    for course in sorted_common_courses:
        data = {
            'c1num': c_1[course]['course_num'],
            'c1course': c_1[course]['course_name'],
            'c2num': c_2[course]['course_num'],
            'c2course': c_2[course]['course_name']
            }

        results.append(data)

    return results

def get_different_courses(inst1, inst2, major):
 
    data1 = getDataSet(inst1, major) 
    data2 = getDataSet(inst2, major)

    college1_course_ids = get_course_ids(data1)
    college2_course_ids = get_course_ids(data2)

    different_courses = college1_course_ids.symmetric_difference(college2_course_ids) #obtains courses with different C-ID 

    c_1 = array_to_object(data1)
    c_2 = array_to_object(data2)

    results = []

    for course in sorted_common_courses:
        data = {
            'c1num': c_1[course]['course_num'],
            'c1course': c_1[course]['course_name'],
            'c2num': c_2[course]['course_num'],
            'c2course': c_2[course]['course_name']
            }

        results.append(data)

    return results

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)


