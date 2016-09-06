from django.test import TestCase
import urllib.request
import urllib.parse
import json
import unittest
from sms.commonmethods.url_methods import UrlMethods
from sms.commonmethods.read_params import *
#测试用例id和title
testId=0
testTitle=''

class TestTeams(unittest.TestCase):
    
    def setUp(self):
        self.urlmethods=UrlMethods()
        self.readparams=ReadParams()
    def tearDown(self):
        print('end')        
    def test_add_teams(self):
        global testId
        global testTitle
        wr_rs=[]
        testTitle='add teams'
        urlMehtods=self.urlmethods
        readParams=self.readparams
        #球队目前不支持创建自行车的球队
        daxiang_type={
        '篮球':'lq',
        '足球':'lq',
        '赛车':'sc',
        '综合体育':'zh',
        '橄榄球':'glq',
        '电竞':'zh',
        '棒球':'bq',
        '自行车':''
        }
        teamType={
        '俱乐部':'CLUB_TEAM',
        '国家队':'NATIONAL_TEAM'
        }
        
        add_teams_path='D:\\softwares\\Python\\sms\\params\\read\\add_teams_params.txt'
        teams_results_path='D:\\softwares\\Python\\sms\\params\\write\\teams_results.txt'
        all_params=readParams.read_params(add_teams_path)
        for pa in all_params:
            #确认新建球队的接口url
            url_type=daxiang_type[pa[0]]
            add_teams_url='http://s.sms.letv.com/team/'+url_type+'/edit'
            #mian_type对应接口中id值为teams_data_lq中gameFType值
            gameFType=self.getChildDicByKey('main_type',pa[0])[1]
            #pa[3]是发布地区信息，可能包含多个发布地区，用“/”隔开，需要判断
            allow_countries=self.getAllowCountries(pa[3])
            #赛车、综合体育、电竞无type字段，足球type=3
            #篮球、橄榄球和棒球teams_data字段一样 有联盟、分区
            #电竞、综合体育和赛车data一样
            #赛车、综合体育、电竞 通过post传递的data参数一致
            teams_data={
                'id':'',
                'gameFType':gameFType,
                'allowCountries':allow_countries,
                'name':pa[4],
                'nickname':pa[5],
                'city':pa[6],
                'octopusId':pa[9],
                'octopusName':pa[10],
                'campId':pa[11],
                'leciId':pa[12],
                'desc':pa[13]
                }

            #篮球、橄榄球、棒球 通过post传递的data参数一致
            if pa[0]=='篮球' or '橄榄球' or '棒球':
                #conference对应lianmeng的id,region对应fenqu的id，如果lianmeng和fenqu是空，这两个值则对应-1
                #pa[1]是txt文件上读取的lianmeng字段数据，pa[2]是txt文件上读取的fenqu字段数据
                lianmeng_list=self.getChildDicByKey('lianmeng',pa[1])
                fenqu_list=self.getChildDicByKey('fenqu',pa[2])
                if pa[1] =='':
                    conference=-1
                else:
                    conference=lianmeng_list[1]
                if pa[2] =='':
                    region=-1
                else:
                    region=fenqu_list[1]
                # pa[3]是发布地区信息，可能包含多个发布地区，用“/”隔开，需要判断
                # allow_countries=self.getAllowCountries(pa[3])
                teams_data['type']=url_type
                teams_data['conference']=conference
                teams_data['region']=region
                teams_data['homeGround']=pa[7]
                teams_data['teamType']=teamType[pa[8]]
            if pa[0]=='足球':
                teams_data['type']=3
                teams_data['homeGround']=pa[7]
                teams_data['teamType']=teamType[pa[8]]
            rs_code=urlMehtods.url_post_method(add_teams_url,teams_data)
            #输出结果：testId+testTitle+result
            #当code=A00000，msg='成功'时，认为结果为pass；当code不等于A000000，认为结果为fail；当code为其他，认为无结果
            testId=testId+1
            wr_rs.append(str(testId)+','+testTitle+','+self.getResults(rs_code['code'],rs_code['msg']))
            # print('################',rs_code)
            # print('################',rs_code['code'])
        print('%%%%%%%%%%%%%%%%%%%%%%',wr_rs)
        readParams.write_results(teams_results_path,wr_rs)
        

    def test_query_teams_list(self):
        testTitle='query teams'
        name='what'
        teamType=''
        gameFType=''
        country='CN'
        url_query='http://s.sms.letv.com/team/query?name='+name+'&teamType='+teamType+'&gameFType='+gameFType+'&country='+country+'&callerId=10001&size=15&page=0'
        pass

    def test_delete_teams(self):
        global testId
        wr_rs=[]
        testTitle='delete teams'
        urlMehtods=self.urlmethods
        readParams=self.readparams
        url_del='http://s.sms.letv.com/team/delete'
        name=''
        gameFType=''
        ids=[]
        delete_ids=[]
        add_teams_path='D:\\softwares\\Python\\sms\\params\\read\\add_teams_params.txt'
        teams_results_path='D:\\softwares\\Python\\sms\\params\\write\\teams_results.txt'
        all_params=readParams.read_params(add_teams_path)
        for pa in all_params:
            name=pa[4]
            gameFType=self.getChildDicByKey('main_type',pa[0])[1]
            url_query='http://s.sms.letv.com/team/query?name='+name+'&teamType=&gameFType='+str(gameFType)+'&country=CN&callerId=10001&size=15&page=0'
            query_rs=urlMehtods.url_get_method(url_query)
            for co in query_rs['data']['content']:
                ids.append(co['id'])
        print('~~~~~~~~~~~~~',ids)
        print('~~~~~~~~~~~~~!!!!!!!!!!!!!!1',len(ids))
        #去掉重复id
        for delete_id in ids:
            if delete_id not in delete_ids:
                delete_ids.append(delete_id)
        for em in delete_ids:
            param={
            'id':em
            }
            delete_rs=urlMehtods.url_post_method(url_del,param)
            testId=testId+1
            wr_rs.append(str(testId)+','+testTitle+','+self.getResults(delete_rs['code'],delete_rs['msg']))
        readParams.write_results(teams_results_path,wr_rs)



        
    def getChildDicByKey(self,key,name):
        urlMehtods=UrlMethods()
        url='http://s.sms.letv.com/dict/getChildDicByKey?key='
        key_url=url+key
        rs_ChildDicByKey=[]
        data=urlMehtods.url_get_method(key_url)['data']
        for ls in data:
            if ls['name']==name:
                rs_ChildDicByKey.append(ls['key'])
                rs_ChildDicByKey.append(ls['id'])
        return(rs_ChildDicByKey)
                
    def getAllowCountries(self,countries):
        allowCountries={
        '中国':'CN',
        '香港':'HK',
        '美国':'US'
        }
        allowCountriesList=countries.split('/')
        
        allowcountrieslist=[]
        for country in allowCountriesList:
            allowcountrieslist.append(allowCountries[country])
        #将国家用','隔开，生成字符串allowcountries
        allowcountries=','.join(allowcountrieslist)
        return allowcountries
    def getResults(self,code,msg):
        try:
            if code=='A00000' and msg=='成功':
                rs='pass'
            else:
                rs='fail'
        except Exception as e:
            rs='no except result'
        return rs

    def test_edit_teams(self):
        pass

if __name__ == '__main__':
    unittest.main()
