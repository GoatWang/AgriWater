from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt



from linebot import LineBotApi, WebhookParser ##, WebhookHanlder
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import (
    MessageEvent, FollowEvent, PostbackEvent, UnfollowEvent,
    TextMessage, LocationMessage, 
    TextSendMessage, TemplateSendMessage,ImageSendMessage, StickerSendMessage,
    ButtonsTemplate, ConfirmTemplate, CarouselTemplate,
    PostbackTemplateAction, MessageTemplateAction, URITemplateAction,
    CarouselColumn
)
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)




import pickle
import os
import pandas as pd
import re
from datetime import datetime, timedelta
from ArgriWater import settings
# import
from pymongo import MongoClient
from bson.son import SON
from bson.objectid import ObjectId #這東西再透過ObjectID去尋找的時候會用到
dbuser = os.environ['AGRIWATER_DBUSER']
dbpassword = os.environ['AGRIWATER_DBPASSWORD']


# connection
conn = MongoClient("mongodb://" + dbuser + ":" + dbpassword + "@ds239128.mlab.com:39128/agriwater") # 如果你只想連本機端的server你可以忽略，遠端的url填入: mongodb://<user_name>:<user_password>@ds<xxxxxx>.mlab.com:<xxxxx>/<database_name>，請務必既的把腳括號的內容代換成自己的資料。
db = conn.agriwater
# collection = db.agriwater
collection = db.agriwater_first

def index(request):
    # counties = ['卑南站', '成功站', '東河站', '檢驗單位', '池上站', '知本站', '臺東站', '長濱站', '關山站', '鹿野站']
    associations = list(collection.distinct('association'))
    stations = list(collection.distinct('station'))
    # association_stations = {}
    # association_station_points = {}
    # for association in associations:
    #     stations = collection.distince('station', filter={"association":association})
    #     association_stations[association] = stations
    #     for station in stations:
    #         points = collection.distince('point', filter={"station":station})
    #         association_station_points[association+"_"+station] = points
        
    context = {
        "associations": associations,
        "stations": stations,
    }
    return render(request, 'mainapp/index.html', context)

def get_points(request, association, station):
    cursor = collection.aggregate([
                    {"$match": {"association":association}},
                    {"$match": {"station":station}},
                    {
                        "$group": { 
                            "_id": { 
                                "point_name": "$point_name", 
                                "point_number": "$point_number" 
                            } 
                        } 
                    },
                ])
    points = [c['_id'] for c in cursor]
    context = {"points": points,}
    return JsonResponse(context)


def get_all_coordinates(request):
    # with open(os.path.join(settings.MEDIA_ROOT, "agriwater", 'locations.pkl'), 'rb') as f:
    #     coordinates = pickle.load(f)
    cursor = collection.aggregate([
                    {"$group": { "_id": { 
                        "association": "$association", 
                        "station": "$station" , 
                        "point_name": "$point_name" , 
                        "point_number": "$point_number",
                        "location": "$location" } } }
                ])
    coordinates = [c['_id'] for c in cursor]
    return JsonResponse(coordinates, safe=False)

def get_point_data(request, point_number):
    cursor = collection.find({"point_number":point_number}).sort("sampling_date", -1)
    data = [c for c in cursor]
    df = pd.DataFrame(data)[["station", "point_name", "sampling_date", "temp", "ph", "ec", "result", "point_number", "association", "location"]]#[[ "point_name", "station", "sampling_date", "temp", "ph", "ec", "cd", "cr", "pb", "zn",]]
    df.columns = ["檢測站", "檢測點", "採樣日期", "溫度", "酸鹼度", "電導度", "檢測通過", "檢測點編號", "水利會", "經緯度"]#["監視點名稱", "工作站", "採樣日期", "溫度", "酸鹼值", "電導度", "鎘", "鉻", "鉛", "鋅",]
    showing_cols = ["水利會", "檢測站", "檢測點", "採樣日期", "溫度", "酸鹼度", "電導度", "檢測通過"]
    html_table = df[showing_cols].to_html(index=False, classes="table", border=0).replace(' style="text-align: right;"', "")
    
    index_cols = ["溫度", "酸鹼度", "電導度"]#["溫度", "酸鹼值", "電導度", "鋅"] # , "鎘", "鉻", "鉛"
    df = df.iloc[:5].sort_values('採樣日期', ascending=True)
    json_table = df[index_cols].to_dict(orient='list')

    limitation = {
        "溫度":{"max":35, "min":None},
        "酸鹼度":{"max":9, "min":6},
        "電導度":{"max":750, "min":None},
        # "鋅":{"max":2, "min":None},
    }
    res_context = {
        "html_table":html_table, 
        "採樣日期":df['採樣日期'].tolist(),
        "association": df['水利會'].values[0], 
        "station": df['檢測站'].values[0], 
        "point_name": df['檢測點'].values[0], 
        "limitation":limitation,
        "json_table":json_table}
    return JsonResponse(res_context)


 # Create your views here.
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)
@csrf_exempt
def callback(request):
    if request.method == 'GET':
        return JsonResponse({"status_code":200, "message":"you are in callback function!"})
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        # try:
        #     events = parser.parse(body, signature)
        # except InvalidSignatureError:
        #     return HttpResponseForbidden()
        # except LineBotApiError:
        #     return HttpResponseBadRequest()

        for event in events:
            if isinstance(event, MessageEvent):
                if isinstance(event.message, TextMessage):
                    _handle_text_message(event,request.get_host())
                if isinstance(event.message, LocationMessage):
                    _handle_location_message(event)
            # if isinstance(event, FollowEvent):
            #     _handle_follow_event(event)
            # if isinstance(event, UnfollowEvent):
            #     _handle_unfollow_event(event)
            # if isinstance(event, PostbackEvent):
            #     _handle_postback_event(event)
                
        return HttpResponse()
    # else:
    #     return HttpResponseBadRequest()


def _handle_text_msg(event):
    text = event.message.text
    messages = [TextSendMessage(text=text)]

    line_bot_api.reply_message(
        event.reply_token,
        messages
    )


def _handle_location_msg(event):
    location = event.message 
    address = location.address
    lat = location.latitude
    lng = location.longitude
    messages = []

    # lng, lat = 121.120222, 22.782330
    query = { "location" :
       { "$near" :
          {
            "$geometry" : {
               "type" : "Point" ,
               "coordinates" : [lng, lat] },
          }
       }
    }

    # query = { "location" :{ "$near" :{"$geometry" : {"type" : "Point" ,"coordinates" : [lng, lat] }}}}
    data = collection.find_one(query)
    result = "通過" if data['result'] else "未通過"
    response = ""
    response += "水利會: " + data['association']
    response += "檢測站: " + data['station']
    response += "檢測點: " + data['point_name']
    response += "溫度: %.2f"  %data['temp']
    response += "酸鹼度: %.2f"  %data['ph']
    response += "電導度: %.2f"  %data['ec']
    response += "檢測通過: " + data['result']
    
    messages = TextSendMessage(text=response)
        
    line_bot_api.reply_message(
        event.reply_token,
        messages
    )
















# df_result = pd.read_pickle(os.path.join(settings.MEDIA_ROOT,"df_result.pkl"))
# # df_result_county = pd.read_pickle(os.path.join(settings.MEDIA_ROOT,"df_result_county.pkl"))

# def get_df_result(caseid=7):
#     # files = os.listdir(os.path.join(settings.MEDIA_ROOT, "results"))
#     # file_paths = [os.path.join(settings.MEDIA_ROOT, "results", f) for f in files] 

#     # results = []
#     # for idx, fp in enumerate(file_paths):
#     #     df_result = pd.read_csv(fp)
#     #     df_result['案件全稱'] = files[idx].replace('.csv', '')
#     #     df_result['案件'] = int(re.findall("第\d+案", files[idx])[0].replace("第", "").replace("案", ""))
#     #     df_result['投票權人數'] = df_result['投票權人數'].apply(lambda x:x.replace(',', '')).astype(int)
#     #     df_result['投票數'] = df_result['投票數'].apply(lambda x:x.replace(',', '')).astype(int)
#     #     df_result['同意票數'] = df_result['同意票數'].apply(lambda x:x.replace(',', '')).astype(int)
#     #     df_result['不同意票數'] = df_result['不同意票數'].apply(lambda x:x.replace(',', '')).astype(int)
#     #     df_result['有效票數'] = df_result['有效票數'].apply(lambda x:x.replace(',', '')).astype(int)
#     #     df_result['有效同意票數對投票權人數百分比(%)'] = df_result['有效同意票數對投票權人數百分比(%)'].apply(lambda x:x.replace('%', '')).astype(float)
#     #     df_result['有效不同意票數對投票權人數百分比(%)'] = df_result['有效不同意票數對投票權人數百分比(%)'].apply(lambda x:x.replace('%', '')).astype(float)
#     #     df_result['投票率(%)'] = df_result['投票率(%)'].apply(lambda x:x.replace('%', '')).astype(float)
#     #     results.append(df_result)
#     # df_result = pd.concat(results).sort_values('案件')

#     # # df_result_county = df_result[df_result.apply(lambda x: pd.isnull(x['地區']) and x['縣市']!="全國", axis=1)].copy()
#     # # df_result_county['locate_idx'] = df_result_county['縣市']

#     # # df_county_polygon = pd.read_pickle(os.path.join(settings.MEDIA_ROOT,"df_county.pkl")).copy()
#     # # df_county_polygon['locate_idx'] = df_county_polygon['COUNTYNAME']


#     # # df_result_county = pd.merge(df_result_county, df_county_polygon, on='locate_idx')
#     # # df_result_county.to_pickle(os.path.join(settings.MEDIA_ROOT,"df_result_county.pkl"))
#     # # df_result_county = pd.read_pickle(os.path.join(settings.MEDIA_ROOT,"df_result_county.pkl"))
#     # # return df_result_county.copy()

#     # df_result_town = df_result[pd.notnull(df_result['地區'])].copy()
#     # df_result_town['locate_idx'] = df_result_town[['縣市', '地區']].apply(tuple, axis=1)
#     # df_town_polygon = pd.read_pickle(os.path.join(settings.MEDIA_ROOT,"df_town.pkl")).copy()
#     # df_town_polygon['locate_idx'] = df_town_polygon[['COUNTYNAME', 'TOWNNAME']].apply(tuple, axis=1)

#     # df_result = pd.merge(df_result_town, df_town_polygon, on='locate_idx')
#     # df_result.to_pickle(os.path.join(settings.MEDIA_ROOT,"df_result.pkl"))
#     # df_result = pd.read_pickle(os.path.join(settings.MEDIA_ROOT,"df_result.pkl"))
#     return df_result.copy()

# def election_index(request):
#     df_result = get_df_result()
#     print(df_result.columns)
#     case_choices = df_result[['案件', '案件全稱']].copy().drop_duplicates().values.tolist()
#     case_choices = sorted(case_choices, key=lambda x:x[0])

# # Index(['案件', '縣市', '地區', '同意票數', '不同意票數', '有效票數', '無效票數', '投票數', '投票權人數',
# #        '投票率(%)', '有效同意票數對投票權人數百分比(%)', '有效不同意票數對投票權人數百分比(%)',
# #        '有效同意與不同意票數對投票權人數百分比(%)差值', '案件全稱', 'locate_idx', 'TOWNID', 'TOWNCODE',
# #        'COUNTYNAME', 'TOWNNAME', 'TOWNENG', 'COUNTYID', 'COUNTYCODE',
# #        'coordinates'],

#     context = {
#         "case_choices":case_choices, 
#         }
#     return render(request, 'mainapp/election_index.html', context)

# def election_visualize(request, caseid=7):
#     df_result = get_df_result()
#     df_result = df_result[df_result['案件']==caseid]

#     # for county
#     # df_agreement_county_group = df_result.sort_values('有效同意票數對投票權人數百分比(%)', ascending=False)
#     # df_disagreement_county_group = df_result.sort_values('有效不同意票數對投票權人數百分比(%)', ascending=False)
#     # df_num_tickets_proportion = df_result.sort_values('投票率(%)', ascending=False)

#     # for town
#     df_agreement_county_group = df_result.groupby('縣市').sum().reset_index()[['縣市', '同意票數', '投票權人數']]
#     df_agreement_county_group['有效同意票數對投票權人數百分比(%)'] = df_agreement_county_group.apply(lambda x:x['同意票數']/x['投票權人數'], axis=1)
#     df_agreement_county_group = df_agreement_county_group.sort_values('有效同意票數對投票權人數百分比(%)', ascending=False)

#     df_disagreement_county_group = df_result.groupby('縣市').sum().reset_index()[['縣市', '不同意票數', '投票權人數']]
#     df_disagreement_county_group['有效不同意票數對投票權人數百分比(%)'] = df_disagreement_county_group.apply(lambda x:x['不同意票數']/x['投票權人數'], axis=1)
#     df_disagreement_county_group = df_disagreement_county_group.sort_values('有效不同意票數對投票權人數百分比(%)', ascending=False)

#     df_num_tickets_proportion = df_result.groupby('縣市').sum().reset_index()[['縣市', '投票數', '投票權人數']]
#     df_num_tickets_proportion['投票率(%)'] = df_num_tickets_proportion.apply(lambda x:x['投票數']/x['投票權人數'], axis=1)
#     df_num_tickets_proportion = df_num_tickets_proportion.sort_values('投票率(%)', ascending=False)

#     context = {
#         "table":df_result[['縣市', '地區', '有效票數', '有效同意票數對投票權人數百分比(%)', 'coordinates']].to_dict(orient='records'),
#         "num_qualified_citizens":int(df_result['投票權人數'].sum()),
#         "num_tickets":int(df_result['投票數'].sum()),
#         "num_effictive_tickets":int(df_result['有效票數'].sum()),
#         "num_agreement_tickets":int( df_result['同意票數'].sum()),
#         "num_disagreement_tickets":int( df_result['不同意票數'].sum()),
#         "agreement_proportion": ("%.2f" %((df_result['同意票數'].sum()/df_result['投票權人數'].sum())*100)) + "%",
#         "disagreement_proportion": ("%.2f" %((df_result['不同意票數'].sum()/df_result['投票權人數'].sum())*100)) + "%",
#         "agreement_counties":df_agreement_county_group['縣市'].values.tolist(),
#         "agreement_counties_proportion":df_agreement_county_group['有效同意票數對投票權人數百分比(%)'].values.tolist(),
#         "disagreement_counties":df_disagreement_county_group['縣市'].values.tolist(),
#         "disagreement_counties_proportion":df_disagreement_county_group['有效不同意票數對投票權人數百分比(%)'].values.tolist(),
#         "et_counties": df_num_tickets_proportion['縣市'].values.tolist(),
#         "et_counties_effective_tickets": df_num_tickets_proportion['投票率(%)'].values.tolist(),
#     }
#     return JsonResponse(context)

