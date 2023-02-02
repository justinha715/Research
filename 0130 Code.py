##############################################################################
#########    다른 조건 동일하게 미세먼지 좋은날과 나쁜날 pair 만들기   ###########
#########                                                          ###########
#########       작성자: 하종현(Jonghyun Ha)                         ###########
#########      e-mail: ha200701045@gmail.com                       ###########  
##############################################################################

import pandas as pd

# Load data from Excel file
data = pd.read_excel('data.xlsx', sheet_name='2010-2019', header=0)

data = data.iloc[:, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]]

# Create a DataFrame from the data
df = pd.DataFrame(data)

# Check the number of rows in the DataFrame
num_rows = df.shape[0]
print("Number of rows in DataFrame:", num_rows)

# Check the number of columns in the DataFrame
num_cols = df.shape[1]
print("Number of columns in DataFrame:", num_cols)

# find and fill / remove the missing values with a specific value
missing_values = df.isnull().sum()
print("Number of missing values in DataFrame:",missing_values,sep='\n')

df.fillna(-9999, inplace=True)
#df = df.dropna(inplace=True)

# set up the threshold for identifying the bad days of PM10.
threshold = 80
df['bad'] = df['PM'] > threshold
df['bad'].replace({True: 1, False: 0}, inplace=True)

# set up the threshold for Temperature and Precipitation.
t=2
p=1

# result settings
result = pd.DataFrame(columns=['Date_bad','Date_good', 'PM_bad','PM_good', 'Visits_bad', 'Visits_good', 'Pre_diff', 'Temp_diff'])

################## Functions ###################################
def abs_diff(a, b):
  return abs(a - b)

#  7일전 조건 확인
def pre(index):
    pre_weekdays = df['weekdays'].iloc[index-7]
    pre_date = df['Date'].iloc[index-7]
    pre_temp = df['Temp'].iloc[index-7]
    pre_pre = df['Pre'].iloc[index-7]
    pre_pm= df['PM'].iloc[index-7]
    pre_visits= df['Visits'].iloc[index-7]           
    pre_bad=df['bad'].iloc[index-7]

    return pre_weekdays, pre_date, pre_temp, pre_pre, pre_pm, pre_visits, pre_bad

# 7일후 조건 확인
def aft(index):
    aft_weekdays = df['weekdays'].iloc[index+7]
    aft_date = df['Date'].iloc[index+7]
    aft_temp = df['Temp'].iloc[index+7]
    aft_pre = df['Pre'].iloc[index+7]
    aft_pm= df['PM'].iloc[index+7]
    aft_visits= df['Visits'].iloc[index+7]
    aft_bad=df['bad'].iloc[index+7]

    return aft_weekdays, aft_date, aft_temp, aft_pre, aft_pm, aft_visits, aft_bad


def no_missing_check(index):
    if df['Visits'].iloc[index] < 0:
        check=1
    elif df['PM'].iloc[index] < 0 :
        check=2
    elif df['Temp'].iloc[index] < -99 :
        check=3
    elif df['Pre'].iloc[index] < -99 :
        check=4
    else :
        check=0

    return check
################################################################

for index, row in df.iterrows():


## CASE 1) 7일후만 비교    
    if index <= 6 and no_missing_check(index)==0: 

        if row['bad'] ==1 and row['weekdays']==1: 

            ######################## 평일 / 7일후 조건 검색 ###################     
            aft_weekdays, aft_date,aft_temp, aft_pre, aft_pm, aft_visits, aft_bad = aft(index)

            Pre_diff = abs_diff(row['Pre'], aft_pre)
            Temp_diff = abs_diff(row['Temp'], aft_temp)
            ######################## 미세먼지 좋고 같은 평일, 조건 만족하는 경우 검색 #####
            if  aft_bad == 0 and aft_weekdays == 1 and Pre_diff <p  and Temp_diff<t :

                new_row = pd.DataFrame({
                    'Date_bad': [df['Date'].iloc[index]],
                    'Date_good': [aft_date],
                    'PM_bad': [df['PM'].iloc[index]],
                    'PM_good': [aft_pm],
                    'Visits_bad': [df['Visits'].iloc[index]],
                    'Visits_good': [aft_visits],
                    'Pre_diff': [Pre_diff],
                    'Temp_diff': [Temp_diff]
                })

                result = pd.concat([result, new_row], ignore_index=True)

        
        elif row['bad'] ==1 and row['weekdays']==0: 
            ######################## 주말 및 공휴일 / 7일후 조건 검색 ###################        
            aft_weekdays, aft_date,aft_temp, aft_pre, aft_pm, aft_visits, aft_bad = aft(index) 

            Pre_diff = abs_diff(row['Pre'], aft_pre)
            Temp_diff = abs_diff(row['Temp'], aft_temp)
            ######################## 미세먼지 좋고 같은 주말 및 공휴일, 조건 만족하는 경우 검색 #####
            if  aft_bad == 0 and aft_weekdays == 0 and Pre_diff <p  and Temp_diff<t :

                new_row = pd.DataFrame({
                    'Date_bad': [df['Date'].iloc[index]],
                    'Date_good': [aft_date],
                    'PM_bad': [df['PM'].iloc[index]],
                    'PM_good': [aft_pm],
                    'Visits_bad': [df['Visits'].iloc[index]],
                    'Visits_good': [aft_visits],
                    'Pre_diff': [Pre_diff],
                    'Temp_diff': [Temp_diff]
                })

                result = pd.concat([result, new_row], ignore_index=True)   

## CASE 2) 7일 전/후 모두 비교  
    elif 6 < index < (num_rows-7) and no_missing_check(index)==0 :

        if row['bad'] ==1 and row['weekdays']==1:
            ######################## 평일 / 7일전 ###################
            pre_weekdays, pre_date,pre_temp, pre_pre, pre_pm, pre_visits, pre_bad = pre(index)

            Pre_diff=abs_diff(row['Pre'], pre_pre)
            Temp_diff=abs_diff(row['Temp'], pre_temp)

            ######################## 미세먼지 좋고 같은 평일, 조건 만족하는 경우 검색 #####
            if  pre_bad == 0 and pre_weekdays == 1 and Pre_diff<p  and Temp_diff <t :

                new_row = pd.DataFrame({
                    'Date_bad': [df['Date'].iloc[index]],
                    'Date_good': [pre_date],
                    'PM_bad': [df['PM'].iloc[index]],
                    'PM_good': [pre_pm],
                    'Visits_bad': [df['Visits'].iloc[index]],
                    'Visits_good': [pre_visits],
                    'Pre_diff': [Pre_diff],
                    'Temp_diff': [Temp_diff]
                })

                result = pd.concat([result, new_row], ignore_index=True)
            
            ######################## 평일 / 7일후 조건 검색 ###################     
            aft_weekdays, aft_date,aft_temp, aft_pre, aft_pm, aft_visits, aft_bad = aft(index)

            Pre_diff =  abs_diff(row['Pre'], aft_pre)
            Temp_diff = abs_diff(row['Temp'], aft_temp)
            ######################## 미세먼지 좋고 같은 평일, 조건 만족하는 경우 검색 #####
            if  aft_bad == 0 and aft_weekdays == 1 and Pre_diff <p  and Temp_diff<t :

                new_row = pd.DataFrame({
                    'Date_bad': [df['Date'].iloc[index]],
                    'Date_good': [aft_date],
                    'PM_bad': [df['PM'].iloc[index]],
                    'PM_good': [aft_pm],
                    'Visits_bad': [df['Visits'].iloc[index]],
                    'Visits_good': [aft_visits],
                    'Pre_diff': [Pre_diff],
                    'Temp_diff': [Temp_diff]
                })

                result = pd.concat([result, new_row], ignore_index=True)   

        elif row['bad'] ==1 and row['weekdays']==0:

            ######################## 주말 및 공휴일 / 7일전 ###################        
            pre_weekdays, pre_date,pre_temp, pre_pre, pre_pm, pre_visits, pre_bad = pre(index)

            Pre_diff=abs_diff(row['Pre'], pre_pre)
            Temp_diff=abs_diff(row['Temp'], pre_temp)
            ######################## 미세먼지 좋고 같은 주말 및 공휴일, 조건 만족하는 경우 검색 #####
            if  pre_bad == 0 and pre_weekdays == 0 and Pre_diff<p  and Temp_diff<t :

                new_row = pd.DataFrame({
                    'Date_bad': [df['Date'].iloc[index]],
                    'Date_good': [pre_date],
                    'PM_bad': [df['PM'].iloc[index]],
                    'PM_good': [pre_pm],
                    'Visits_bad': [df['Visits'].iloc[index]],
                    'Visits_good': [pre_visits],
                    'Pre_diff': [Pre_diff],
                    'Temp_diff': [Temp_diff]
                })

                result = pd.concat([result, new_row], ignore_index=True)
 
            ######################## 주말 및 공휴일 / 7일후 조건 검색 ###################        
            aft_weekdays, aft_date,aft_temp, aft_pre, aft_pm, aft_visits, aft_bad = aft(index) 

            Pre_diff =  abs_diff(row['Pre'], aft_pre)
            Temp_diff = abs_diff(row['Temp'], aft_temp)
            ######################## 미세먼지 좋고 같은 주말 및 공휴일, 조건 만족하는 경우 검색 #####
            if  aft_bad == 0 and aft_weekdays == 0 and Pre_diff<p  and Temp_diff<t :

                new_row = pd.DataFrame({
                    'Date_bad': [df['Date'].iloc[index]],
                    'Date_good': [aft_date],
                    'PM_bad': [df['PM'].iloc[index]],
                    'PM_good': [aft_pm],
                    'Visits_bad': [df['Visits'].iloc[index]],
                    'Visits_good': [aft_visits],
                    'Pre_diff': [Pre_diff],
                    'Temp_diff': [Temp_diff]
                })

                result = pd.concat([result, new_row], ignore_index=True)   

## CASE 3) 7일 전 비교       
    elif (num_rows-7) <= index and no_missing_check(index)==0:

        if row['bad'] ==1 and row['weekdays']==1:
            ######################## 평일 / 7일전 ###################
            pre_weekdays, pre_date,pre_temp, pre_pre, pre_pm, pre_visits, pre_bad = pre(index)

            Pre_diff=abs_diff(row['Pre'], pre_pre)
            Temp_diff=abs_diff(row['Temp'], pre_temp)
            ######################## 미세먼지 좋고 같은 평일, 조건 만족하는 경우 검색 #####
            if  pre_bad == 0 and pre_weekdays == 1 and  Pre_diff<p  and Temp_diff<t :

                new_row = pd.DataFrame({
                    'Date_bad': [df['Date'].iloc[index]],
                    'Date_good': [pre_date],
                    'PM_bad': [df['PM'].iloc[index]],
                    'PM_good': [pre_pm],
                    'Visits_bad': [df['Visits'].iloc[index]],
                    'Visits_good': [pre_visits],
                    'Pre_diff': [Pre_diff],
                    'Temp_diff': [Temp_diff]
                })

                result = pd.concat([result, new_row], ignore_index=True)
 

        elif row['bad'] ==1 and row['weekdays']==0:
            ######################## 주말 및 공휴일 / 7일전 ###################        
            pre_weekdays, pre_date,pre_temp, pre_pre, pre_pm, pre_visits, pre_bad = pre(index)

            Pre_diff=abs_diff(row['Pre'], pre_pre)
            Temp_diff=abs_diff(row['Temp'], pre_temp)
            ######################## 미세먼지 좋고 같은 주말 및 공휴일, 조건 만족하는 경우 검색 #####
            if  pre_bad == 0 and pre_weekdays == 0 and Pre_diff<p  and Temp_diff<t :

                new_row = pd.DataFrame({
                    'Date_bad': [df['Date'].iloc[index]],
                    'Date_good': [pre_date],
                    'PM_bad': [df['PM'].iloc[index]],
                    'PM_good': [pre_pm],
                    'Visits_bad': [df['Visits'].iloc[index]],
                    'Visits_good': [pre_visits],
                    'Pre_diff': [Pre_diff],
                    'Temp_diff': [Temp_diff]
                })

                result = pd.concat([result, new_row], ignore_index=True)

####### Output Data : 관광객 수 차이 도출 
result.loc[:,'diff']=result['Visits_bad']-result['Visits_good']

####### 날짜 표기 단순화 
result['Date_bad'] = pd.to_datetime(result['Date_bad']).dt.date
result['Date_good'] = pd.to_datetime(result['Date_good']).dt.date

####### 결측치 포함 행 제거
mask = (result != -9999).all(axis=1)
result = result[mask]

print(result)
filename="result5.csv"
result.to_csv(filename,index=False)
  