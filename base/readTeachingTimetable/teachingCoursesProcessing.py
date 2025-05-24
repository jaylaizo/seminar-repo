import PyPDF2
import re
from itertools import chain
import pdb

import fitz  # PyMuPDF
import re
import pdb

def readPdfFile(files):
    all_results = []

    for file in files:
        text = ""
        with fitz.open(stream=file.read(), filetype="pdf") as doc:
            for page in doc:
                text += page.get_text()

        # Extract time slots from the header
        time_slots = re.findall(r'\d{2}:\d{2} \d{2}:\d{2}', text)
        
        
        print(time_slots)
        pdb.set_trace()

        # Extract seminar blocks: 3 lines under each "Seminar"
        seminar_blocks = re.findall(r'Seminar\s+(.*?)\n(.*?)\n(.*?)(?:\n|$)', text)

        for i, block in enumerate(seminar_blocks):
            course_lines = [line.strip() for line in block]
            course_text = ' '.join(course_lines)
            course_text = re.sub(r'\s{2,}', ' ', course_text).strip()

            if i < len(time_slots):
                all_results.append({
                    'course': course_text,
                    'time': time_slots[i]
                })

    print(all_results)
    pdb.set_trace()

    return all_results



def readPdfFile2(files):
    with open('processed_Teaching_Courses.txt', mode="w") as output_file:
        for file in files:
            pdfFileObj = file
            pdfReader = PyPDF2.PdfReader(pdfFileObj)
            for page in pdfReader.pages:
                text = page.extract_text()
                output_file.write(text)
            pdfFileObj.close()  
    output_file.close()

    lines2 = ['DAR ES SALAAM UNIVERSITY COLLEGE OF EDUCATION ']
    
    lines3 = ['TEACHING TIMETABLE', 'ACADEMIC YEAR', '07:00 07:55 08:00 08:55 09:00 09:55 10:00 10:55 11:00 11:55 12:00 12:55 13:00 13:55 14:00 14:55 15:00 15:55 16:00 16:55 17:00 17:55 18:00 18:55 19:00 19:55',
        'PUBLISHED', '07:00 07:55 08:00 08:55 09:00 09:55 10:00 10:55 11:00 11:55 12:00 12:55 13:00 13:55 14:00 14:55 15:00 15:55 16:00 16:55 17:00', 
        'BY UNIVERSITY OF', 'DAR ES SALAAM, PROGRAM MAN UNIT', 'DUCE HUMANITIES', 'PAGE', 'CONTINUED']

    with open('processed_Teaching_Courses.txt', 'r') as f:
        lines = f.readlines()
        lines = [l.strip('\n') for l in lines]        
        lines = [l.upper() for l in lines if l not in lines2]
        
        lines4 = [l for l in lines if any([substring in l for substring in lines3])]
        lines = [t.strip() for t in lines if t not in lines4]

        newlines = []
        for line in lines:
            newlines.extend(re.split('LECTURE ', line)[1:])
            newlines.extend(re.split('PRACTICALS ', line)[1:])
            newlines.extend(re.split('SEMINAR ', line)[1:])
            newlines.extend(re.split('PROJECT WORK ', line)[1:])

        unwanted = ['THU', 'RSDAY', 'PRACTICAL',  'TUTORIAL', 'MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', ',','(A)', '(B)', '(C)', 'B.A']
        for word in unwanted:
            newlines = [t.split(word) for t in newlines]
            newlines = list(chain.from_iterable(newlines))




        seminar_items = [item for item in newlines if 'SEMINAR' in item]
        print(seminar_items)
        import pdb
        pdb.set_trace()
        
        
        

        newlines = [t.strip() for t in newlines if len(t) >= 5]
        #courses = [course[-6:] if course.endswith(('A', 'B')) else course[-5:] for course in newlines]

        courses = [
            course[-6:] if course.endswith(('A', 'B', 'C'))
            else course[-8:] if course[-4:].isdigit()
            else course[-5:]
            for course in newlines
        ]
        courses = [t.strip() for t in courses]
        courses = list(set(courses))
    return courses
        

def timetableProcessing(teaching_timetables, course_allocations_files, initial_draft):
    course_list = readPdfFile(teaching_timetables)
    courses_allocations = processExcelFile(course_allocations_files)

    offered_courses = [[course, students] for course, students in set(courses_allocations.items())]
    semesterCourses = [course[0] for course in offered_courses]

    offered_courses = [ '-'.join([course, students]) for course, students in courses_allocations.items()]
    newCourses = set(semesterCourses) - set(course_list)

    newCourses_final = ['-'.join([course, students]) for course, students in courses_allocations.items() if course in list(newCourses)]


    deleteCourses = []
    if initial_draft:
        deleteCourses = list(set(course_list) - set(semesterCourses))
    else:
        offered_courses = [ '-'.join([course, students]) for course, students in courses_allocations.items() if course in list(newCourses)]
        offered_courses.extend(list(course_list))
    total_courses = len(set(offered_courses))
    return newCourses_final, deleteCourses, offered_courses, total_courses, set(course_list)