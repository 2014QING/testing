#coding:utf-8
import os


class ReadParams(object):
    #txt_path为文件路径+文件名称，如txt_path='D:\\softwares\\PythonScripts\\sms\\params\\edit_level1_params.txt'
    def read_params(self,txt_path):
        l3=[]
        #先判断文件是否存在，存在读取文件内容,读取的内容字符串化
        #encoding='utf-8'
        if os.path.isfile(txt_path):
            print("File already exists!")
            #with open(txt_path,encoding='utf-8',mode='rt') as f:
            with open(txt_path,mode='rt') as f:
                for line in f:
                    l1=str(line.strip('\n'))
                    l2=l1.split(',')
                    l3.append(l2)
            f.close()
            #去掉第一行标题
            params=l3[1:]
            return params
        else:
            print("File is not exists!")

if __name__=='__main__':
    print('what~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    readParams=ReadParams()
    params=readParams.read_params('D:\\softwares\\Python\\sms\\params\\add_teams_params.txt')
    print(params)
