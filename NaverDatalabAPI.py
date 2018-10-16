class NaverDatalabAPI:

    def Help(self):
        print('Parameters',
    '\n\n-----------------------------\n\n',
    'startDate',
    '\nType : string',
    'Requirement : Yes',
    'Explanation : 조회 기간 시작 날짜(yyyy-mm-dd 형식). 2016년 1월 1일부터 조회할 수 있습니다.\n\n',
    'endDate',
    '\nType : string',
    'Requirement : Yes',
    'Explanation : 조회 기간 종료 날짜(yyyy-mm-dd 형식)\n\n',
    'timeUnit',
    '\nType : string',
    'Requirement : Yes',
    'Explanation : 구간 단위\n- date: 일간\n- week: 주간\n- month: 월간\n\n',
    'keywords',
    '\nType : array(JSON)',
    'Requirement : Yes',
    'Explanation : 주제어와 주제어에 해당하는 검색어 묶음 쌍의 배열. 최대 5개의 쌍을 배열로 설정할 수 있습니다.\n\n',
    'groupName',
    '\nType : string',
    'Requirement : Yes',
    'Explanation : 주제어. 검색어 묶음을 대표하는 이름입니다.\n\n',
    'device',
    '\nType : string',
    'Requirement : No',
    'Explanation : 범위. 검색 환경에 따른 조건입니다.\n- 설정 안 함: 모든 환경\n- pc: PC에서 검색 추이\n- mo: 모바일에서 검색 추이\n\n',
    'gender',
    '\nType : string',
    'Requirement : No',
    'Explanation : 성별. 검색 사용자의 성별에 따른 조건입니다.\n- 설정 안 함: 모든 성별\n- m: 남성\n- f: 여성\n\n',
    'ages',
    '\nType : array(string)',
    'Requirement : No',
    'Explanation : 연령. 검색 사용자의 연령에 따른 조건입니다.\n- 설정 안 함: 모든 연령\n- 1: 0∼12세\n- 2: 13∼18세\n- 3: 19∼24세\n- 4: 25∼29세',
    '\n- 5: 30∼34세\n- 6: 35∼39세\n- 7: 40∼44세\n- 8: 45∼49세\n- 9: 50∼54세\n- 10: 55∼59세\n- 11: 60세 이상')



    def Search(self,startDate = "2016-01-01",
        endDate = "2017-12-31",
        timeUnit = "month",
        device = "",
        ages = [],
        gender="",
        groupName = ['네이버'],
        keywords = [['네이버','Naver']]):
        ''' function for handling Naver Datalab
        default : client_id = "bZWIA91H20kesR3Oru7w", client_secret = "fTsukml_0L",
        startDate = "2016-01-01", endDate = "2017-12-31", timeUnit = "month",
        device = "",ages = [],gender="",groupName = ['네이버'],keywords = [['네이버','Naver']]
        '''
        import os
        import sys
        import urllib.request

        url = "https://openapi.naver.com/v1/datalab/search";

        client_id = "bZWIA91H20kesR3Oru7w"
        client_secret = "fTsukml_0L"

        if (groupName != ['네이버'])&(keywords == [['네이버', 'Naver']]):
            keywords = [groupName]

        if len(groupName) != len(keywords):
            raise LenError('Lenth of groupName and keywords must be equal')


        keywordGroups = []
        for group in range(len(groupName)):
            kG = {"groupName": groupName[group],"keywords": keywords[group]}
            keywordGroups.append(kG)

        parameter = {"startDate":startDate,
                     "endDate":endDate,
                     "timeUnit":timeUnit,
                     "keywordGroups":keywordGroups,
                     "device":device,
                     "ages":ages,
                     "gender":gender}




        body = str(parameter).replace("'","\"").replace(" ","")



        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id",client_id)
        request.add_header("X-Naver-Client-Secret",client_secret)
        request.add_header("Content-Type","application/json")
        response = urllib.request.urlopen(request, data=body.encode("utf-8"))
        rescode = response.getcode()

        if(rescode==200):
            response_body = response.read()
        else:
            print("Error Code:" + rescode)

        self.response = response_body.decode('utf-8')
        return self.response

    def Parse(self):
        import pandas as pd

        rdata =pd.read_json(self.response)['results'][0]

        df_parse = pd.concat([pd.Series([rdata['title']]*len(rdata['data']),name='title'),
                    pd.Series([rdata['keywords']]*len(rdata['data']),name='keywords'),
                    pd.DataFrame.from_dict(rdata['data'])],axis=1)

        for i in range(len(df_parse)):
            df_parse.loc[i,'period']=int(df_parse.loc[i,'period'].replace('-',''))

        df_parse.loc[:,'period'] = pd.to_datetime(df_parse.loc[:,'period'],format='%Y%m%d')

        df_parse = df_parse.set_index('period',drop=True)

        return df_parse
