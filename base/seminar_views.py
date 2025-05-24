from django.views import View 
from django.shortcuts import render
from django.http import HttpResponse
from.readTeachingTimetable.teachingCoursesProcessing import readPdfFile
from.readTeachingTimetable.examsdata import readPdfFile as readExamPdfFile


class TeachingTimetableView(View):
    upload_template= 'upload_pdf.html'
    
    def get(self, request):
        # Render the upload form when accessed via GET
        return render(request, self.upload_template)
    
    
    def post(self,request):
        files= request.FILES.getlist('pdf_files')
        if files:
            seminars= readPdfFile(files)
            
            #seminars=readExamPdfFile(files)
            
            
            print(seminars)
            import pdb
            pdb.set_trace()
            
            
            
            return render(request,{'exracted_seminars':seminars})
        return HttpResponse('no files uploaded ')           