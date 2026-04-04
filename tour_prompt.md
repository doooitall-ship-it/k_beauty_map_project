## 1) HTTP 요청정보 및 헤더

Request URL
https://korean.visitseoul.net/comm/curation/ajax/postList
Request Method
POST
Status Code
200 200
Remote Address
210.178.43.253:443
Referrer Policy
strict-origin-when-cross-origin

referer
https://korean.visitseoul.net/curation
sec-ch-ua
"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"
sec-ch-ua-mobile
?0
sec-ch-ua-platform
"macOS"
sec-fetch-dest
empty
sec-fetch-mode
cors
sec-fetch-site
same-origin
user-agent
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36
x-requested-with
XMLHttpRequest



## 2) Payload 정보

curPage=1&type=All&optionList=&langCodeId=ko


## 3) 응답의 일부를 Response 에서 일부를 복사해서 넣어주기 (전체는 토큰 수 제한으로어렵습니다.)

{
    "param": {
        "curPage": "1",
        "type": "All",
        "optionList": "",
        "langCodeId": "ko"
    },
    "listVO": {
        "totalCount": 2913,
        "curPage": 1,
        "curUrl": "/comm/curation/ajax/postList",
        "urlParam": "type=All&amp;optionList=&amp;langCodeId=ko",
        "totalPage": 729,
        "totalPageD": 729.0,
        "listObject": [
            {
                "ctgryNm": "서울도보해설관광",
                "tagList": "HYBE사옥,국립중앙박물관,노들섬,여의도한강공원,한강",
                "RNUM": 1,
                "postUri": "K-POP-HANGANG",
                "imageUri": "/data/MEDIA/20260305/0305143529239-4bfc034f68cb42be9ce14df148172ced.jpeg",
                "ctgrySn": 8,
                "postSj": "K-POP 성지 도보투어 1코스",
                "areaNm": null,
                "menuUri": "walking-tour",
                "postSn": 51767,
                "cid": "KON5h154u"

## 4) 해당 API가 제대로 수집되는지 csv 파일로 저장해서 확인하고, 모든 컬럼이 같은 값이거나 결측치인 컬럼은 모두 제외하고, 중복데이터 확인하고, sqlitedb 로 저장하기
