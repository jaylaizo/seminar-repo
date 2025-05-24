from calendar import FRIDAY, THURSDAY, TUESDAY, WEDNESDAY
import PyPDF2
from numpy import *
import re
from string import digits

def readPdfFile(myFiles):
    examInfo = {}
    for file in myFiles:
        lines = []
        pdfFileObj = file
        pdfReader = PyPDF2.PdfReader(pdfFileObj)
        for page in pdfReader.pages:
            text = page.extract_text()
            lines.append(text)
        pdfFileObj.close()  

        lines2 = ['DAR ES SALAAM UNIVERSITY COLLEGE OF EDUCATION ']
        lines3 = ['EXAMINATION TIMETABLE', 'DUCE  SCIENCE', '07:00 08:00 08:00 09:00 09:00 10:00 10:00 11:00 11:00 12:00 12:00 13:00 13:00 14:00',
            'PUBLISHED', '07:00 07:55 08:00 08:55 09:00 09:55 10:00 10:55 11:00 11:55 12:00 12:55 13:00 13:55 14:00 14:55 15:00 15:55 16:00 16:55 17:00', 
            'BY UNIVERSITY OF', 'DAR ES SALAAM, PROGRAM MAN UNIT', 'DUCE HUMANITIES', 'PAGE', 'CONTINUED']

        lines = ','.join(lines)
        lines = lines.split('\n')  
        lines = [l.upper() for l in lines if l not in lines2]
        lines4 = [l for l in lines if any([substring in l for substring in lines3])]
        lines = [t for t in lines if t not in lines4]

        newlines = []
        for line in lines:
            newlines.extend(re.split('EXAMINATION, ', line)[1:])

        exam_Dates = []
        for line_info in newlines:
            date_s = line_info.split(',')
            dat = date_s[1]
            dat = dat.strip()
            dat = dat.split(' ')
            dat = dat[0]
            exam_Dates.append(dat)
        exam_Dates = set(exam_Dates)

        for ex_date in exam_Dates:
            if ex_date in examInfo.keys():
                continue
            examInfo[ex_date] = []

        examStarts = []
        exam_Dates2 = []
        lines = [t for t in newlines]
        for i, info in enumerate(lines):
            date_s = info.split(',')
            dat = date_s[1]
            dat = dat.strip()
            dat = dat.split(' ')
            dat = dat[0]
            if dat not in set(exam_Dates2):
                examStarts.append((i, dat))
                exam_Dates2.append(dat)
        startIndices = [t[0] for t in examStarts]
        dates3 = [t[1] for t in examStarts]
        endIndices = [startIndices[f] for f in range(1, len(startIndices))]
        endIndices.append(len(lines))
        for start, end, dat2 in zip(startIndices, endIndices, dates3):
            exams_2 = lines[start:end]
            exam_date1 = dat2
            for inf in exams_2:
                time_inf = inf.split(',')
                time_inf = [f.strip() for f in time_inf]
                exams_time = time_inf[0]
                dateVenueExam_lists = time_inf[1:]
                dateVenueExam_lists = ','.join(dateVenueExam_lists)

                pattern = r'(\w+\s*\[\d+\]\*(?:\w+\s*\[\d+\]\*)*|\w+\s*\[\d+\]|\w+/\w+\s*\[\d+\])'
                exam_extract = re.findall(pattern, dateVenueExam_lists)
                exam_extract = ','.join(exam_extract)
                
                exam_lists = []
                exams34 = exam_extract.split(',')
                pattern2 = r'(\w+(?:/\w+)*) \[\d+\]'
                for this_exam in exams34:
                    exam = re.findall(pattern2, this_exam)                   
                    exam = ','.join(exam)
                    exam = exam.split('/')
                    exam = [
                        course[-6:] if course.endswith(('A', 'B', 'C'))
                        else course[-8:] if course[-4:].isdigit()
                        else course[-5:]
                        for course in exam
                    ]
                    exam_lists.extend(exam)
                ex = ','.join(exam_lists)

                pattern22 = re.compile(r'(\d{1,2}/\d{1,2}/\d{4})\s(.*?)' + re.escape(exam_lists[0]))
                # Search for the pattern in the input string
                match = pattern22.search(dateVenueExam_lists)
                # Extract the text between date and K
                venues = match.group(2)
                venues = venues.rstrip()
                venues = re.sub(r'\s+', ' ', venues)
                processedVenue = venues.replace(" ", "/")

                info = [ex, exams_time, processedVenue]
                info = '&'.join(info)
                # '2/14/2022':['MT660&15:30-18:30&DUCE/TPC/101']
                examInfo[exam_date1].extend([info])   
    return examInfo

def readPdfFile2(myFiles):
    examInfo = {}
    for file in myFiles:
        lines = []
        pdfFileObj = file
        pdfReader = PyPDF2.PdfReader(pdfFileObj)
        for page in pdfReader.pages:
            text = page.extract_text()
            lines.append(text)
        pdfFileObj.close()  

        lines2 = ['DAR ES SALAAM UNIVERSITY COLLEGE OF EDUCATION ']
        lines3 = ['EXAMINATION TIMETABLE', 'DUCE  SCIENCE', '07:00 08:00 08:00 09:00 09:00 10:00 10:00 11:00 11:00 12:00 12:00 13:00 13:00 14:00',
            'PUBLISHED', '07:00 07:55 08:00 08:55 09:00 09:55 10:00 10:55 11:00 11:55 12:00 12:55 13:00 13:55 14:00 14:55 15:00 15:55 16:00 16:55 17:00', 
            'BY UNIVERSITY OF', 'DAR ES SALAAM, PROGRAM MAN UNIT', 'DUCE HUMANITIES', 'PAGE', 'CONTINUED']

        lines = ','.join(lines)
        lines = lines.split('\n')  
        lines = [l.upper() for l in lines if l not in lines2]
        lines4 = [l for l in lines if any([substring in l for substring in lines3])]
        lines = [t for t in lines if t not in lines4]

        newlines = []
        for line in lines:
            newlines.extend(re.split('EXAMINATION, ', line)[1:])

        exam_Dates = []
        for line_info in newlines:
            date_s = line_info.split(',')
            dat = date_s[1]
            dat = dat.strip()
            dat = dat.split(' ')
            dat = dat[0]
            exam_Dates.append(dat)
        exam_Dates = set(exam_Dates)

        for ex_date in exam_Dates:
            if ex_date in examInfo.keys():
                continue
            examInfo[ex_date] = []

        examStarts = []
        exam_Dates2 = []
        lines = [t for t in newlines]
        for i, info in enumerate(lines):
            date_s = info.split(',')
            dat = date_s[1]
            dat = dat.strip()
            dat = dat.split(' ')
            dat = dat[0]
            if dat not in set(exam_Dates2):
                examStarts.append((i, dat))
                exam_Dates2.append(dat)
        startIndices = [t[0] for t in examStarts]
        dates3 = [t[1] for t in examStarts]
        endIndices = [startIndices[f] for f in range(1, len(startIndices))]
        endIndices.append(len(lines))
        for start, end, dat2 in zip(startIndices, endIndices, dates3):
            exams_2 = lines[start:end]
            exam_date1 = dat2

            for inf in exams_2:
                time_inf = inf.split(',')
                time_inf = [f.strip() for f in time_inf]
                exams_time = time_inf[0]
                dateVenueExam_lists = time_inf[1:]
                dateVenueExam_lists = ','.join(dateVenueExam_lists)

                date_match = re.search(r'\d{1,2}/\d{1,2}/\d{4}', dateVenueExam_lists)
                date_extract = date_match.group(0)

                pattern = r'(\w+\s*\[\d+\]\*(?:\w+\s*\[\d+\]\*)*|\w+\s*\[\d+\]|\w+/\w+\s*\[\d+\])'
                exam_extract = re.findall(pattern, dateVenueExam_lists)


                exam_extract = ','.join(exam_extract)
                start_index = dateVenueExam_lists.index(date_extract) + len(date_extract)
                end_index = dateVenueExam_lists.index(exam_extract)

                exams34 = exam_extract.split(',')            
                pattern2 = r'(\w+(?:/\w+)*) \[\d+\]'
                exam = re.findall(pattern2, exams34[0])
                exam = ','.join(exam)
                if exam.endswith(('A', 'B', 'C')) and len(exam) > 6:
                    end_index = end_index + (len(exam) - 6)
                if exam[-4:].isdigit() and len(exam) > 8:
                    end_index = end_index + (len(exam) - 8)
                if exam[-3:].isdigit() and len(exam) > 5:
                    end_index = end_index + (len(exam) - 5)
                venues = dateVenueExam_lists[start_index:end_index].strip()
                venues = venues.replace(" ", "/")
                venues = venues.split('*')
                
                processedVenue = []
                for vn in venues:
                    vn = vn.lstrip(digits)
                    vn = vn.lstrip("/")
                    processedVenue.append(vn)
                processedVenue = ','.join(processedVenue)

                exam_lists = []
                exams34 = exam_extract.split(',')
                pattern2 = r'(\w+(?:/\w+)*) \[\d+\]'
                for this_exam in exams34:
                    exam = re.findall(pattern2, this_exam)                   
                    exam = ','.join(exam)
                    exam = exam.split('/')
                    exam = [
                        course[-6:] if course.endswith(('A', 'B', 'C'))
                        else course[-8:] if course[-4:].isdigit()
                        else course[-5:]
                        for course in exam
                    ]
                    exam_lists.extend(exam)
                ex = ','.join(exam_lists)

                info = [ex, exams_time, processedVenue]
                info = '&'.join(info)
                # '2/14/2022':['MT660&15:30-18:30&DUCE/TPC/101']
                examInfo[exam_date1].extend([info])
    return examInfo
    

