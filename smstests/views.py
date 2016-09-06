from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    rightside=[]
    result=[]
    rst_data=[]
    legtside=[]
    rst_data=[]
    passed=0
    fail=0
    noresult=0
    results_path='D:\\softwares\\Python\\sms\\params\\write\\teams_results.txt'
    with open(results_path,mode='rt') as rst:
        for line in rst.readlines():
            row=line.strip('\n').split(',')
            ln=len(row)
            if row[ln-1]=='pass':
                passed+=1
            elif row[ln-1]=='fail':
                fail+=1
            elif row[ln-1]=='no except result':
                moresult+=1
            data={
            'testId':'testid'+str(row[0]),
            'testTitle':row[1],
            'result':row[2]
            }
            rst_data.append(data)

    return render(request,'test_results.html',{'rst_data':rst_data,
                                                'pass':passed,
                                                'fail':fail,
                                                'noresult':noresult})

# Create your views here.
