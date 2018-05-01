import urllib3
import datetime
import certifi
from bs4 import BeautifulSoup

baseURL = "https://baseball.yahoo.co.jp"
http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',ca_certs=certifi.where())
team_list = ["広島", "DeNA", "巨人", "阪神", "ヤクルト", "中日",
             "西武", "日本ハム", "ロッテ", "ソフトバンク", "オリックス", "楽天"]

def get_today_score_list(favor_team):

    # closure
    def get_score():
        score = [item.text for item in score_board.findAll("td", {"class": "score_r"})]
        return "{0[0]}-{0[1]}".format(score)
    
    def get_inning():
        return score_board.find("td", {"class": "active yjMSt bt bb"}).find("a").text
    
    if favor_team not in team_list:
        msg = "そんなチームは存在せんぞ"
        return msg,
    day = datetime.date.today().strftime("%Y%m%d")
    # 試合スケージュールの取得
    sch_url = "{}/npb/schedule/?date={}".format(baseURL, day) 
    html = http.request("GET", sch_url)
    soup = BeautifulSoup(html.data, "html5lib")
    sch_list = soup.findAll("table", {"class", "teams"})

    score_list = []
    for idx, sch in enumerate(sch_list):
        cur_teams = [item.find("a").get("title") for item in sch.findAll("th", {"class": "bt bb bl"})]
        
        # 贔屓のチームならスルー
        if favor_team in cur_teams: continue
        
        score_board = sch.find("table", {"class": "score"})
        state_list = ["standby", "active", "end"] # 試合の状態 standby: 試合前, active: 試合中, end: 試合終了
        game_state = [item for item in state_list \
                      if score_board.find("td", {"class": "{0} yjMSt bt bb".format(item)})][0]
        
        # 試合前なら開始時刻,それ以外はスコアを表示
        score, cur_state = [score_board.find("em").text, "試合前"] if game_state == "standby" else \
                           [get_score(), "試合終了"] if game_state == "end" else \
                           [get_score(), get_inning()]
            
        score_list.append("{0[0]} {1} {0[1]} {2}".format(cur_teams, score, cur_state))
        
    return score_list

favor_team = "阪神"
print(get_today_score_list(favor_team))
