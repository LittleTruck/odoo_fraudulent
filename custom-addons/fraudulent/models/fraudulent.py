# -*- coding: utf-8 -*- 

import pandas as pd
import datetime
import numpy as np
import xgboost as xgb
import pickle
from odoo import models, fields, api

class fraudulent(models.Model):

    _name = 'fraudulent.fraudulent'
    _description = 'fraudulent'

    name = fields.Char('訂單簡述',required=False)
    detail = fields.Text('詳細資訊',size=150)
    # is_closed = fields.Boolean('是否關閉')
    # close_reason = fields.Selection(
    #     [('changed','已修改'),('cannot','無法修改'),('delay','推遲')]
    #     ,string="關閉理由"
    # )
    # user_id = fields.Many2one('res.users',string='負責人')


    #member
    member_registry_platform = fields.Char('註冊平台',required=True)
    member_name = fields.Char('使用者名',required=True)
    member_last_name = fields.Char('使用者姓',required=True)
    member_registry_email = fields.Char('註冊信箱',required=True)
    member_registry_region = fields.Char('註冊地區',required=True)
    member_registry_time = fields.Datetime('註冊時間',required=True)

    #product
    prod_tag_cd = fields.Char('訂購商品Tag',required=True)
    prod_oid = fields.Char('訂購商品編號',required=True)

    #order
    order_time = fields.Datetime('訂單成立日期',required=True)
    order_coupon = fields.Char('訂單使用的折扣券')
    product_use_date = fields.Datetime('訂購商品出發日',required=True)
    buyer_pay_currency = fields.Char('訂購人付款幣別',required=True)
    order_amount = fields.Float('訂購人付款總金額',required=True)
    product_quantity = fields.Integer('訂購商品張數',required=True)
    buyer_nationality = fields.Char('訂購人國籍',required=True)
    cart_id = fields.Char('購物車編號',required=True)
    order_comment = fields.Boolean('是否填寫評論',required=True)
    order_remark = fields.Boolean('訂單備註',required=True)

    buyer_id = fields.Char('會員代號',required=True)

    # model not necessary
    # buyer_email = fields.Char('訂購人email')
    # buyer_name = fields.Char('訂購人姓名')
    buyer_phone = fields.Char('訂購人電話')
    buyer_phone_plus = fields.Char('訂購人電話國碼')
    order_id = fields.Char('訂單編號',required=True)
    product_name = fields.Char('訂購商品名稱',required=True)

    predict_result = fields.Char('盜刷預測結果',readonly=True)


    is_fraudulent = fields.Selection(selection=[
    ('unconfirmed', '未確認'),
    ('yes', '是'),
    ('no', '否'),
    ],string='實際是否為盜刷')

    api_call = fields.Boolean('API呼叫',readonly=True,default=False)
    api_call_time = fields.Datetime('API呼叫時間',readonly=True)

    # _sql_constraints = [
    #                  ('order_id_unique', 
    #                   'unique(order_id)',
    #                   'Choose another value - it has to be unique!')
    # ]

    def batch_predict_order(self):
        for fraudulent in self:
            member = pd.DataFrame(
                [
                    [
                        str(fraudulent.member_registry_platform),
                        str(fraudulent.member_name),
                        str(fraudulent.member_last_name ),
                        str(fraudulent.member_registry_email ),
                        str(fraudulent.member_registry_region ),
                        str(fraudulent.buyer_id )
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
                        str(fraudulent.prod_tag_cd ),
                        str(fraudulent.prod_oid )
                    ]
                ],
                columns=
                    [
                        'tag_cd',
                        'prod_oid'
                    ]
            )
            data = pd.DataFrame(
                [
                    [
                        str(fraudulent.order_time),
                        str(fraudulent.order_coupon ),
                        str(fraudulent.product_use_date),
                        str(fraudulent.buyer_pay_currency),
                        fraudulent.order_amount,
                        fraudulent.product_quantity,
                        str(fraudulent.buyer_nationality),
                        str(fraudulent.cart_id),

                        str(fraudulent.buyer_id ),
                        str(fraudulent.buyer_phone ),
                        str(fraudulent.buyer_phone_plus),
                        str(fraudulent.order_id),
                        str(fraudulent.product_name),

                        str(fraudulent.member_registry_time ),

                        str(fraudulent.prod_oid ),

                        str(fraudulent.order_comment ),
                        str(fraudulent.order_remark )
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

                        '訂購商品編號',
                        
                        '是否填寫評論',
                        '訂單備註'
                    ]
            )

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
            fraudulent.predict_result=str(ypred).strip('[]')

            # bst = xgb.Booster.dump_model("xgboost")
            ## 預測
            # xgboost_ypred = bst.predict(dtest)

def weekday(x):
    return str(datetime.datetime(int(x.split("-")[0]),int(x.split("-")[1]),int(x.split("-")[2].split(" ")[0])).weekday())

def whether_is_weekend(x):
    return 1 if x =='0' or x=='6' or x=='5' else 0


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
        for idx,data in enumerate(product['tag_cd'].apply(lambda x:x.split(","))):
            if i in data:
                tmp[idx] = 1
        tag_dict[i] = tmp

    tag_dataframe = pd.DataFrame(tag_dict)
    ##
    product = pd.concat([product,tag_dataframe],axis=1)
    product['訂購商品編號'] = product['prod_oid']
  
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
                                      '訂購人電話', '訂單成立日期', '訂購商品編號',
                                      '訂購商品名稱', '訂購商品出發日', '會員代號','訂購人國籍','prod_oid','tag_cd','註冊時間'])
    
    # 處理類別型變數
    data = pd.get_dummies(data)
    
    return data



