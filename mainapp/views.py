from django.shortcuts import render
from django.http import HttpResponse, JsonResponse


from ArgriWater import settings
import os
import pandas as pd
import re
# Create your views here.
# line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
# parser = WebhookParser(settings.LINE_CHANNEL_SECRET)
# @csrf_exempt
# def callback(request):
#     if request.method == 'GET':
#         return JsonResponse({"status_code":200, "message":"you are in callback function!"})
#     if request.method == 'POST':
#         signature = request.META['HTTP_X_LINE_SIGNATURE']
#         body = request.body.decode('utf-8')

#         try:
#             events = parser.parse(body, signature)
#         except InvalidSignatureError:
#             return HttpResponseForbidden()
#         except LineBotApiError:
#             return HttpResponseBadRequest()

#         for event in events:
#             if isinstance(event, MessageEvent):
#                 if isinstance(event.message, TextMessage):
#                     _handle_text_message(event,request.get_host())
#                 if isinstance(event.message, LocationMessage):
#                     _handle_location_message(event)
#             if isinstance(event, FollowEvent):
#                 _handle_follow_event(event)
#             if isinstance(event, UnfollowEvent):
#                 _handle_unfollow_event(event)
#             if isinstance(event, PostbackEvent):
#                 _handle_postback_event(event)
                
#         return HttpResponse()
#     else:
#         return HttpResponseBadRequest()


def index(request):
    return HttpResponse("Hello, world. You're at the index.")


df_result = pd.read_pickle(os.path.join(settings.MEDIA_ROOT,"df_result.pkl"))
# df_result_county = pd.read_pickle(os.path.join(settings.MEDIA_ROOT,"df_result_county.pkl"))

def get_df_result(caseid=7):
    # files = os.listdir(os.path.join(settings.MEDIA_ROOT, "results"))
    # file_paths = [os.path.join(settings.MEDIA_ROOT, "results", f) for f in files] 

    # results = []
    # for idx, fp in enumerate(file_paths):
    #     df_result = pd.read_csv(fp)
    #     df_result['案件全稱'] = files[idx].replace('.csv', '')
    #     df_result['案件'] = int(re.findall("第\d+案", files[idx])[0].replace("第", "").replace("案", ""))
    #     df_result['投票權人數'] = df_result['投票權人數'].apply(lambda x:x.replace(',', '')).astype(int)
    #     df_result['投票數'] = df_result['投票數'].apply(lambda x:x.replace(',', '')).astype(int)
    #     df_result['同意票數'] = df_result['同意票數'].apply(lambda x:x.replace(',', '')).astype(int)
    #     df_result['不同意票數'] = df_result['不同意票數'].apply(lambda x:x.replace(',', '')).astype(int)
    #     df_result['有效票數'] = df_result['有效票數'].apply(lambda x:x.replace(',', '')).astype(int)
    #     df_result['有效同意票數對投票權人數百分比(%)'] = df_result['有效同意票數對投票權人數百分比(%)'].apply(lambda x:x.replace('%', '')).astype(float)
    #     df_result['有效不同意票數對投票權人數百分比(%)'] = df_result['有效不同意票數對投票權人數百分比(%)'].apply(lambda x:x.replace('%', '')).astype(float)
    #     df_result['投票率(%)'] = df_result['投票率(%)'].apply(lambda x:x.replace('%', '')).astype(float)
    #     results.append(df_result)
    # df_result = pd.concat(results).sort_values('案件')

    # # df_result_county = df_result[df_result.apply(lambda x: pd.isnull(x['地區']) and x['縣市']!="全國", axis=1)].copy()
    # # df_result_county['locate_idx'] = df_result_county['縣市']

    # # df_county_polygon = pd.read_pickle(os.path.join(settings.MEDIA_ROOT,"df_county.pkl")).copy()
    # # df_county_polygon['locate_idx'] = df_county_polygon['COUNTYNAME']


    # # df_result_county = pd.merge(df_result_county, df_county_polygon, on='locate_idx')
    # # df_result_county.to_pickle(os.path.join(settings.MEDIA_ROOT,"df_result_county.pkl"))
    # # df_result_county = pd.read_pickle(os.path.join(settings.MEDIA_ROOT,"df_result_county.pkl"))
    # # return df_result_county.copy()

    # df_result_town = df_result[pd.notnull(df_result['地區'])].copy()
    # df_result_town['locate_idx'] = df_result_town[['縣市', '地區']].apply(tuple, axis=1)
    # df_town_polygon = pd.read_pickle(os.path.join(settings.MEDIA_ROOT,"df_town.pkl")).copy()
    # df_town_polygon['locate_idx'] = df_town_polygon[['COUNTYNAME', 'TOWNNAME']].apply(tuple, axis=1)

    # df_result = pd.merge(df_result_town, df_town_polygon, on='locate_idx')
    # df_result.to_pickle(os.path.join(settings.MEDIA_ROOT,"df_result.pkl"))
    # df_result = pd.read_pickle(os.path.join(settings.MEDIA_ROOT,"df_result.pkl"))
    return df_result.copy()

def election_index(request):
    df_result = get_df_result()
    print(df_result.columns)
    case_choices = df_result[['案件', '案件全稱']].copy().drop_duplicates().values.tolist()
    case_choices = sorted(case_choices, key=lambda x:x[0])

# Index(['案件', '縣市', '地區', '同意票數', '不同意票數', '有效票數', '無效票數', '投票數', '投票權人數',
#        '投票率(%)', '有效同意票數對投票權人數百分比(%)', '有效不同意票數對投票權人數百分比(%)',
#        '有效同意與不同意票數對投票權人數百分比(%)差值', '案件全稱', 'locate_idx', 'TOWNID', 'TOWNCODE',
#        'COUNTYNAME', 'TOWNNAME', 'TOWNENG', 'COUNTYID', 'COUNTYCODE',
#        'coordinates'],

    context = {
        "case_choices":case_choices, 
        }
    return render(request, 'mainapp/election_index.html', context)

def election_visualize(request, caseid=7):
    df_result = get_df_result()
    df_result = df_result[df_result['案件']==caseid]

    # for county
    # df_agreement_county_group = df_result.sort_values('有效同意票數對投票權人數百分比(%)', ascending=False)
    # df_disagreement_county_group = df_result.sort_values('有效不同意票數對投票權人數百分比(%)', ascending=False)
    # df_num_tickets_proportion = df_result.sort_values('投票率(%)', ascending=False)

    # for town
    df_agreement_county_group = df_result.groupby('縣市').sum().reset_index()[['縣市', '同意票數', '投票權人數']]
    df_agreement_county_group['有效同意票數對投票權人數百分比(%)'] = df_agreement_county_group.apply(lambda x:x['同意票數']/x['投票權人數'], axis=1)
    df_agreement_county_group = df_agreement_county_group.sort_values('有效同意票數對投票權人數百分比(%)', ascending=False)

    df_disagreement_county_group = df_result.groupby('縣市').sum().reset_index()[['縣市', '不同意票數', '投票權人數']]
    df_disagreement_county_group['有效不同意票數對投票權人數百分比(%)'] = df_disagreement_county_group.apply(lambda x:x['不同意票數']/x['投票權人數'], axis=1)
    df_disagreement_county_group = df_disagreement_county_group.sort_values('有效不同意票數對投票權人數百分比(%)', ascending=False)

    df_num_tickets_proportion = df_result.groupby('縣市').sum().reset_index()[['縣市', '投票數', '投票權人數']]
    df_num_tickets_proportion['投票率(%)'] = df_num_tickets_proportion.apply(lambda x:x['投票數']/x['投票權人數'], axis=1)
    df_num_tickets_proportion = df_num_tickets_proportion.sort_values('投票率(%)', ascending=False)

    context = {
        "table":df_result[['縣市', '地區', '有效票數', '有效同意票數對投票權人數百分比(%)', 'coordinates']].to_dict(orient='records'),
        "num_qualified_citizens":int(df_result['投票權人數'].sum()),
        "num_tickets":int(df_result['投票數'].sum()),
        "num_effictive_tickets":int(df_result['有效票數'].sum()),
        "num_agreement_tickets":int( df_result['同意票數'].sum()),
        "num_disagreement_tickets":int( df_result['不同意票數'].sum()),
        "agreement_proportion": ("%.2f" %((df_result['同意票數'].sum()/df_result['投票權人數'].sum())*100)) + "%",
        "disagreement_proportion": ("%.2f" %((df_result['不同意票數'].sum()/df_result['投票權人數'].sum())*100)) + "%",
        "agreement_counties":df_agreement_county_group['縣市'].values.tolist(),
        "agreement_counties_proportion":df_agreement_county_group['有效同意票數對投票權人數百分比(%)'].values.tolist(),
        "disagreement_counties":df_disagreement_county_group['縣市'].values.tolist(),
        "disagreement_counties_proportion":df_disagreement_county_group['有效不同意票數對投票權人數百分比(%)'].values.tolist(),
        "et_counties": df_num_tickets_proportion['縣市'].values.tolist(),
        "et_counties_effective_tickets": df_num_tickets_proportion['投票率(%)'].values.tolist(),
    }
    return JsonResponse(context)

