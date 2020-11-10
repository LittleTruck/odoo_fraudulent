# -*- coding: utf-8 -*-
from odoo import http,models,fields,api
from odoo.http import Response, request
from odoo.http import JsonRequest
import time 
import datetime
import json
import pandas as pd
import datetime
import numpy as np
import xgboost as xgb
import pickle


class Fraudulent(http.Controller):
    @http.route('/api/fraudulent', type="json", auth="none", methods=["POST"], csrf=False)
    # @http.route("/api/fraudulent", type='json', auth="public", csrf=False, method=["POST"],website=True, cors="*")
    def FraudulentPredict(self, request, **kw):
        # fraudulent=http.request.env['']
        # fraudulent_domain=[('is_closed','=',False)]
        # fraudulent_open=fraudulent.search(fraudulent_domain)

        # for fraudulent in kw:

        # _str = json.dumps(data)
        # kw = json.loads(data)

        # args = http.request.httprequest.args
        # jsonp = args.get('jsonp')
        # self.jsonp = jsonp
        # request = None
        # request_id = args.get('購物車編號')

        # data = self.payload
        # data = data.get('r')
        # uri,http_method,body,headers=self.get_extra_params
        # for item in data:
        #     order_id = item[0]

        input = request.jsonrequest

        order_id = input['訂單編號']

        member = pd.DataFrame(
            [
                [
                    input['註冊平台'],
                    input['使用者名'],
                    input['使用者姓'],
                    input['註冊信箱'],
                    input['註冊地區'],
                    input['會員代號']
                ]
            ],
            columns=
                [
                    '註冊平台',
                    '使用者名',
                    '使用者姓',
                    '註冊信箱',
                    '註冊地區',
                    '會員代號'
                ]
        )

        product = pd.DataFrame(
            [
                [
                    input['訂購商品Tag'],
                    input['訂購商品編號']
                ]
            ],
            columns=
                [
                    '訂購商品Tag',
                    '訂購商品編號'
                ]
        )

        data = pd.DataFrame(
            [
                [
                    input['訂單成立日期'],
                    input['訂單使用的折扣券'],
                    input['訂購商品出發日'],
                    input['訂購人付款幣別'],
                    input['訂購人付款總金額'],
                    input['訂購商品張數'],
                    input['訂購人國籍'],
                    input['購物車編號'],

                    input['會員代號'],
                    input['訂購人電話'],
                    input['訂購人電話國碼'],
                    input['訂單編號'],
                    input['訂購商品名稱'],

                    input['註冊時間'],

                    input['訂購商品編號']
                ]
            ],
            columns=
                [
                    '訂單成立日期',
                    '訂單使用的折扣券',
                    '訂購商品出發日',
                    '訂購人付款幣別',
                    '訂購人付款總金額',
                    '訂購商品張數',
                    '訂購人國籍',
                    '購物車編號',

                    '會員代號',
                    '訂購人電話',
                    '訂購人電話國碼',
                    '訂單編號',
                    '訂購商品名稱',

                    '註冊時間',

                    '訂購商品編號'
                ]
        )

        # data = pd.DataFrame(
        #     [
        #         [
        #             input['訂單成立日期'],
        #             input['訂購人國籍'],
        #             input['訂購人付款幣別'],
        #             input['訂購人電話國碼'],
        #             input['購物車編號'],
        #             input['訂購人付款總金額'],
        #             input['訂單使用的折扣券'],
        #             input['訂單編號'],
        #             input['訂購商品編號'],
        #             input['訂購商品名稱'],
        #             input['訂購商品張數'],
        #             input['訂購商品出發日']
        #         ]
        #     ],
        #     columns=[
        #         '訂單成立日期',
        #         '訂購人國籍',
        #         '訂購人付款幣別',
        #         '訂購人電話國碼',
        #         '購物車編號',
        #         '訂購人付款總金額',
        #         '訂單使用的折扣券',
        #         '訂單編號',
        #         '訂購商品編號',
        #         '訂購商品名稱',
        #         '訂購商品張數',
        #         '訂購商品出發日'
        #     ]
        # )

        # # 處理訂單日期
        # data['訂單日期'] = data['訂單成立日期'].apply(
        #     lambda x: str(x.split("/")[2].split(" ")[0]))
        # # 處理訂單時間
        # data['訂單時間'] = data['訂單成立日期'].apply(
        #     lambda x: str(int(x.split(" ")[1].split(":")[0])))

        # # 處理訂單使用折扣券
        # data['訂單使用的折扣券'] = data['訂單使用的折扣券'].fillna(0)
        # data['訂單使用的折扣券'] = data['訂單使用的折扣券'].apply(lambda x: 0 if x == 0 else 1)

        # # 處理訂單時間高風險
        # hour_high_risk = ['19', '20']
        # hour_mid_risk = ['21', '18']
        # hour_mid_low_risk = ['8', '9']

        # data['hour_risk'] = data['訂單時間'].apply(lambda x: "high" if x in hour_high_risk
        #                                        else ("mid" if x in hour_mid_risk
        #                                              else ("mid_low" if x in hour_mid_low_risk
        #                                                    else "low")))

        # # 處理訂單使用折扣券
        # data['訂單使用的折扣券'] = data['訂單使用的折扣券'].fillna(0)
        # data['訂單使用的折扣券'] = data['訂單使用的折扣券'].apply(lambda x: 0 if x == 0 else 1)

        # # 處理訂單星期
        # data['week'] = data['訂單成立日期'].apply(lambda x: weekday(x))

        # # 處理訂購商品出發日
        # data['prodouct_week'] = data['訂購商品出發日'].apply(lambda x: weekday(x))

        # # 處理訂單假日
        # data['weekend'] = data['week'].apply(lambda x: whether_is_weekend(x))

        # # 處理訂購商品出發假日
        # data['prodouct_weekend'] = data['prodouct_week'].apply(
        #     lambda x: whether_is_weekend(x))

        # # 處理訂單總金額新台幣
        # To_NWD_rate = dict({"TWD": 1, "HKD": 3.7875, "SGD": 21.4028, "MYR": 6.9832, "KRW": 0.02468, "PHP": 0.5982, "CNY": 4.2180, "JPY": 0.2779,
        #                     "USD": 29.3461, "AUD": 21.0852, "THB": 0.9465, "EUR": 34.6794, "VND": 0.0012622, "IDR": 0.0020254, "NZD": 19.4986, "CAD": 22.0844, "GBP": 38.4138})

        # data['訂單總金額_新台幣'] = data['訂購人付款幣別'].apply(
        #     lambda x: To_NWD_rate.get(x)) * data['訂購人付款總金額']

        # # 處理訂單總金額新台幣_log 轉換
        # data['訂單總金額_新台幣_log'] = (data['訂單總金額_新台幣']+1).transform(np.log)

        # # 處理訂單平均價錢
        # data['訂單平均價格_新台幣'] = data['訂單總金額_新台幣'] / data['訂購商品張數']

        # # 處理訂單人國籍
        # high_country = ['BD', 'FR', 'CA', 'CN', "ID", 'IN', 'IT']
        # data['high_county'] = data['訂購人國籍'].apply(
        #     lambda x: 1 if x in high_country else 0)

        # # 處理訂單人幣別
        # high_coin = ['CNY', 'EUR', 'IDR', 'SGD', 'USD']
        # data['high_coin'] = data['訂購人付款幣別'].apply(
        #     lambda x: 1 if x in high_coin else 0)

        # # 處理訂購日與商品出發日相距多少天
        # data["相差多少天"] = [day.days for day in data['訂購商品出發日'].apply(lambda x:datetime.date(int(x.split('/')[0]),
        #                                                                                   int(x.split(
        #                                                                                       '/')[1]),
        #                                                                                   int(x.split('/')[2].split(' ')[0])))-data['訂單成立日期'].apply(lambda x:datetime.date(int(x.split('/')[0]),
        #                                                                                                                                                                    int(x.split(
        #                                                                                                                                                                        '/')[1]),
        #                                                                                                                                                                    int(x.split('/')[2].split(' ')[0])))]

        # # 處理消費總金額大於5000元
        # high_money_risk = data.groupby('購物車編號').sum(
        # )[data.groupby('購物車編號').sum()['訂單總金額_新台幣'] > 5000]

        # high_money_risk['high_money_risk'] = [1] * high_money_risk.shape[0]

        # high_money = high_money_risk.iloc[:, -1]

        # data = pd.merge(left=data, right=high_money, on=["購物車編號"], how="left")

        # data['high_money_risk'] = data['high_money_risk'].fillna(0)

        # # 刪除變數名稱
        # data = data.drop(axis=1, columns=['購物車編號', '訂單編號', '訂購人電話國碼', '訂單成立日期', '訂購商品編號',
        #                                   '訂購商品名稱', '訂購商品出發日', '訂購人國籍'])

        # # 處理類別型變數
        # data = pd.get_dummies(data)

        member = member_processing(member)
        product = product_processing(product)

        ## 將 product , member , data 合併
        data = pd.merge(left = data, right = member, on = ['會員代號'], how='left')
        data = pd.merge(left = data, right = product, on = ['訂購商品編號'], how='left')

        test = data_preprocessing(data)
        
        ## 將資料轉換型式
        dtest = xgb.DMatrix(data = test)

        ## 讀取 model
        xgboost_model = xgb.Booster(model_file="/home/vagrant/Desktop/test/xgboostnew")
        ypred = xgboost_model.predict(dtest)


        # data = xgb.DMatrix(data)
        # xgboost_model = xgb.Booster(
        #     model_file="/home/vagrant/Desktop/test/xgboost")
        # ypred = xgboost_model.predict(data)

        vals = {
            'member_registry_platform': input['註冊平台'],
            'member_name': input['使用者名'],
            'member_last_name': input['使用者姓'],
            'member_registry_email': input['註冊信箱'],
            'member_registry_region': input['註冊地區'],
            'member_registry_time': input['註冊時間'],

            'prod_tag_cd': input['訂購商品Tag'],
            'prod_oid': input['訂購商品編號'],

            'order_time': input['訂單成立日期'],
            'order_coupon': input['訂單使用的折扣券'],
            'product_use_date': input['訂購商品出發日'],
            'buyer_pay_currency': input['訂購人付款幣別'],
            'order_amount': input['訂購人付款總金額'],
            'product_quantity': input['訂購商品張數'],
            'buyer_nationality': input['訂購人國籍'],
            'cart_id': input['購物車編號'],

            'buyer_id': input['會員代號'],

            'buyer_phone': input['訂購人電話'],
            'buyer_phone_plus': input['訂購人電話國碼'],
            'order_id': input['訂單編號'],
            'product_name': input['訂購商品名稱'],

            'predict_result': str(ypred).strip('[]'),
            'api_call': True,
            'api_call_time':  datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        try:
            request.env['fraudulent.fraudulent'].create(vals)
        except:
            pass

        return_str = "{\"訂單編號\":\""+order_id + \
            "\",\"盜刷預測結果\":\""+str(ypred).strip('[]')+"\"}"
        return_json = json.loads(return_str)

        return return_json

        # vals = {
        #     'order_time': input['訂單成立日期'],
        #     'buyer_nationality': input['訂購人國籍'],
        #     'buyer_pay_currency': input['訂購人付款幣別'],
        #     'buyer_phone_plus': input['訂購人電話國碼'],
        #     'cart_id': input['購物車編號'],
        #     'order_amount': input['訂購人付款總金額'],
        #     'order_coupon': input['訂單使用的折扣券'],
        #     'order_id': input['訂單編號'],
        #     'product_id': input['訂購商品編號'],
        #     'product_name': input['訂購商品名稱'],
        #     'product_quantity': input['訂購商品張數'],
        #     'product_use_date': input['訂購商品出發日'],
        #     'predict_result': str(ypred).strip('[]'),
        #     'api_call': True,
        #     'api_call_time':  datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # }

        # try:
        #     request.env['fraudulent.fraudulent'].create(vals)
        # except:
        #     pass

        # return_str = "{\"訂單編號\":\""+order_id + \
        #     "\",\"盜刷預測結果\":\""+str(ypred).strip('[]')+"\"}"
        # return_json = json.loads(return_str)

        

        # return return_json


def weekday(x):
    return str(datetime.datetime(int(x.split("/")[0]), int(x.split("/")[1]), int(x.split("/")[2].split(" ")[0])).weekday())


def whether_is_weekend(x):
    return 1 if x == '0' or x == '6' or x == '5' else 0

def member_processing(member):
    ##蒐集所有註冊平台
    plat_set = {'FACEBOOK','GOOGLE','GOOGLE_MAP','KAKAO','KKDAY','LINE','NAVER','WECHAT','YAHOO_JAPAN','ability','cwtest','qctest','rsi'}
    plat_dict = dict()
    zeros = [0] * member.shape[0]

    for i in sorted(plat_set):
        tmp = zeros.copy() 
        for idx,data in enumerate(member['註冊平台'].apply(lambda x:x.split(","))):
            if i in data:
                tmp[idx] = 1
        plat_dict[i] = tmp

    plat_dataframe = pd.DataFrame(plat_dict)
    ##合併
    member = pd.concat([member, plat_dataframe],axis = 1)
    ##
    member['使用者姓名'] =( member['使用者名'].isna() | member['使用者姓'].isna())
    member['是否有註冊信箱'] = list(map(lambda x :int(x),member['註冊信箱'].isna()))
    member = member.drop(['註冊信箱','註冊平台','使用者名','使用者姓'],axis=1)
    member['註冊地區'] = member['註冊地區'].fillna("na")
    ##
    all_set = {'AE', 'AF', 'AG', 'AI', 'AL', 'AO', 'AQ', 'AR', 'AT', 'AU', 'AZ', 'BA', 'BD', 'BE', 'BF', 'BG',
               'BH', 'BM', 'BN', 'BO', 'BR', 'BS', 'BT', 'BY', 'CA', 'CD', 'CF', 'CH', 'CI', 'CL', 'CN', 'CO',
               'CR', 'CY', 'CZ', 'DE', 'DK', 'DO', 'DZ', 'EC', 'EE', 'EG', 'ES', 'FI', 'FJ', 'FR', 'GA', 'GB',
               'GE', 'GH', 'GI', 'GN', 'GR', 'GT', 'GU', 'HK', 'HN', 'HR', 'HU', 'ID', 'IE', 'IL', 'IN', 'IR',
               'IS', 'IT', 'JE', 'JM', 'JO', 'JP', 'KE', 'KH', 'KP', 'KR', 'KW', 'KZ', 'LA', 'LB', 'LI', 'LK',
               'LS', 'LT', 'LU', 'LV', 'MA', 'MC', 'MD', 'ME', 'MK', 'MM', 'MN', 'MO', 'MP', 'MT', 'MU', 'MV',
               'MX', 'MY', 'MZ', 'NG', 'NI', 'NL', 'NO', 'NP', 'NR', 'NZ', 'OM', 'PA', 'PE', 'PF', 'PG', 'PH',
               'PK', 'PL', 'PR', 'PT', 'PW', 'PY', 'QA', 'RE', 'RO', 'RS', 'RU', 'SA', 'SB', 'SC', 'SE', 'SG',
               'SI', 'SK', 'SL', 'SY', 'TG', 'TH', 'TJ', 'TL', 'TN', 'TO', 'TR', 'TT', 'TW', 'TZ', 'UA', 'US',
               'UY', 'UZ', 'VA', 'VE', 'VN', 'WS', 'YE', 'ZA', 'ZM', 'ZW'}
    ##
    place_dict = dict()
    zeros = [0] * member.shape[0]

    for i in sorted(all_set):
        tmp = zeros.copy() 
        for idx,data in enumerate(member['註冊地區']):
            if i in data:
                tmp[idx] = 1
        place_dict[i] = tmp

    place_dataframe = pd.DataFrame(place_dict)
    #
    member = pd.concat([member,place_dataframe],axis=1)
    member = member.drop(['註冊地區'],axis=1)
   
    return member

def product_processing(product):
    all_set = {'TAG_1_1', 'TAG_1_2', 'TAG_1_3', 'TAG_2_1', 'TAG_2_2', 'TAG_2_3', 'TAG_2_4', 'TAG_2_5',
               'TAG_2_6', 'TAG_3_1', 'TAG_3_2', 'TAG_3_3', 'TAG_3_4', 'TAG_3_5', 'TAG_3_6', 'TAG_3_7',
               'TAG_4_1', 'TAG_4_2', 'TAG_4_3', 'TAG_4_4', 'TAG_4_5', 'TAG_4_6', 'TAG_4_7', 'TAG_4_8',
               'TAG_5_1', 'TAG_5_2', 'TAG_5_3', 'TAG_5_4', 'TAG_5_5', 'TAG_5_6'}
    tag_dict = dict()
    zeros = [0] * product.shape[0]

    for i in sorted(all_set):
        tmp = zeros.copy() 
        for idx,data in enumerate(product['訂購商品Tag'].apply(lambda x:x.split(","))):
            if i in data:
                tmp[idx] = 1
        tag_dict[i] = tmp

    tag_dataframe = pd.DataFrame(tag_dict)
    ##
    product = pd.concat([product,tag_dataframe],axis=1)
    product['訂購商品編號'] = product['訂購商品編號']
  
    return product

def data_preprocessing(data):
    
    # 處理訂單日期
    data["訂單日期"] = data['訂單成立日期'].apply(lambda x : str(x.split("-")[2].split(" ")[0]))
    
    # 處理訂單時間
    data['訂單時間'] = data['訂單成立日期'].apply(lambda x : str(int(x.split(" ")[1].split(":")[0])))
    
    # 處理訂單時間高風險
    hour_high_risk = ['19','20']
    hour_mid_risk = ['21','18']
    hour_mid_low_risk = ['8','9']
    
    data['hour_risk'] = data['訂單時間'].apply(lambda x : "high" if x in hour_high_risk 
                                                       else ("mid" if x in hour_mid_risk 
                                                        else ("mid_low" if x in hour_mid_low_risk 
                                                       else "low")))
    
    # 處理訂單使用折扣券
    data['訂單使用的折扣券'] = data['訂單使用的折扣券'].fillna(0)
    data['訂單使用的折扣券'] = data['訂單使用的折扣券'].apply(lambda x:0 if x ==0 else 1)
    
    # 處理訂單星期
    data['week'] = data['訂單成立日期'].apply(lambda x :weekday(x))
    
    # 處理訂購商品出發日
    data['prodouct_week'] = data['訂購商品出發日'].apply(lambda x :weekday(x))
    
    # 處理訂單假日
    data['weekend'] = data['week'].apply(lambda x :whether_is_weekend(x))
    
    # 處理訂購商品出發假日
    data['prodouct_weekend'] = data['prodouct_week'].apply(lambda x :whether_is_weekend(x))
    
    # 處理訂單總金額新台幣
    To_NWD_rate = dict({"TWD":1,"HKD":3.7875,"SGD":21.4028,"MYR":6.9832,"KRW":0.02468,"PHP":0.5982,"CNY":4.2180,"JPY":0.2779,
                  "USD":29.3461,"AUD":21.0852,"THB":0.9465,"EUR":34.6794,"VND":0.0012622,"IDR":0.0020254,"NZD":19.4986,"CAD":22.0844,"GBP":38.4138})
    
    data['訂單總金額_新台幣'] = data['訂購人付款幣別'].apply(lambda x : To_NWD_rate.get(x)) * data['訂購人付款總金額']
    
    # 處理訂單總金額新台幣_log 轉換
    data['訂單總金額_新台幣_log'] = (data['訂單總金額_新台幣']+1).transform(np.log)
    
    # 處理訂單平均價錢
    data['訂單平均價格_新台幣'] = data['訂單總金額_新台幣'] / data['訂購商品張數']
    
    # 處理訂單人國籍
    high_country = ['BD','FR','CA','CN',"ID",'IN','IT']
    data['high_county'] = data['訂購人國籍'].apply(lambda x : 1 if x in high_country else 0)
    
    # 處理訂單人幣別
    high_coin = ['CNY','EUR','IDR','SGD','USD']
    data['high_coin'] = data['訂購人付款幣別'].apply(lambda x: 1 if x in high_coin else 0)
    
    # 處理訂購日與商品出發日相距多少天
    data["相差多少天"] = [day.days for day in data['訂購商品出發日'].apply(lambda x :datetime.date(int(x.split('-')[0]),
                                                     int(x.split('-')[1]),
                                                     int(x.split('-')[2].split(' ')[0])))-data['訂單成立日期'].apply(lambda x :datetime.date(int(x.split('-')[0]),
                                                     int(x.split('-')[1]),
                                                     int(x.split('-')[2].split(' ')[0])))]
    # 處理註冊日語訂購日相聚多少天
    data['註冊日與訂購相差多少天'] = [day.days for day in data['訂單成立日期'].apply(lambda x :datetime.date(int(x.split('-')[0]),
                                                     int(x.split('-')[1]),
                                                     int(x.split('-')[2].split(' ')[0])))-data['註冊時間'].apply(lambda x :datetime.date(int(x.split('-')[0]),
                                                     int(x.split('-')[1]),
                                                     int(x.split('-')[2].split(' ')[0])))]
    
    # 處理消費總金額大於5000元
    high_money_risk = data.groupby('購物車編號').sum()[data.groupby('購物車編號').sum()['訂單總金額_新台幣']>5000]

    high_money_risk['high_money_risk'] = [1] * high_money_risk.shape[0]

    high_money = high_money_risk.iloc[:,-1]
    
    data = pd.merge(left= data, right= high_money, on=["購物車編號"], how="left")
    
    data['high_money_risk'] = data['high_money_risk'].fillna(0)
    
    # 刪除變數名稱
    data = data.drop(axis=1, columns=['購物車編號', '訂單編號', '訂購人電話國碼',
                                      '訂購人電話', '訂單成立日期', 
                                      '訂購商品名稱', '訂購商品出發日','訂購人國籍','註冊時間'])
    
    # 處理類別型變數
    data = pd.get_dummies(data)
    
    
    return data


    # def index(self, **kw):
    #     return "Hello, world"

    # @http.route('/fraudulent/fraudulent/objects/', auth='public')
    # def list(self, **kw):
    #     return http.request.render('fraudulent.listing', {
    #         'root': '/fraudulent/fraudulent',
    #         'objects': http.request.env['fraudulent.fraudulent'].search([]),
    #     })

    # @http.route('/fraudulent/fraudulent/objects/<model("fraudulent.fraudulent"):obj>/', auth='public')
    # def object(self, obj, **kw):
    #     return http.request.render('fraudulent.object', {
    #         'object': obj
    #     })
