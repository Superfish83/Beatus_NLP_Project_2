from flask import *
app = Flask(__name__)

from NLP.dialoguehandler import DialogueHandler
dlgHandler = DialogueHandler()

def template(title, content, auto_submit = None):
    t = f'''<!doctype html>
    <link rel="stylesheet" href="{ url_for('static', filename='design.css') }" media="(min-width:600px)">
    <html>
        <title>{title}</title>
        <header>
            <div id="logo">
                <a href = "/">
                    <img src="https://www.cnsa.hs.kr/images/hpw/common/logo.gif" alt="Logo" width="225" height="60" href="./index.html">
                </a>
            </div>

            <div id="top_menu">
                <h2> 2022 Beatus 인공지능팀 프로젝트</h2>
                <h4> KoBART와 TextRank를 이용한 학습용 챗봇 </h4>
            </div>
        </header>
        
        <article id="content" style="background-color: #9EC3E3">
        <div>{content}</div>
        </article>
        
        <footer>
            <p>Made by 김연준, 홍준혁</p>
        </footer>
    '''

    if auto_submit:
        t += f'''
            <script>
                document.{auto_submit}.submit();
            </script>'''
    t += '</html>'
    return t

def getTextForm(username, dlg_state):
    form = ''
    if dlg_state < 100: # 사용자에게 채팅 입력을 받을 때
        form = f'''
            <form name = "getUserText" action="/chat/" method="POST">
                <input type="textarea" name="usertext" placeholder="채팅 입력"></textarea>
                <input type="hidden" name="current_username" value={username}>
                <input type="hidden" name="dlg_state" value={dlg_state}>
                <input type="submit" value="입력">
            </form>'''
    else: # 챗봇이 계속 말할 때 (입력받는 것 없이 form 제출)
        form = f'''
            <form name = "getUserText" action="/chat/" method="POST">
                <input type="textarea" name="usertext" placeholder="채팅 입력"></textarea>
                <input type="hidden" name="current_username" value={username}>
                <input type="hidden" name="dlg_state" value={dlg_state}>
            </form>
            '''
    return form

@app.route('/')
def home():
    getName = '''
        <div class = "input-box">
            <h1>당신의 이름을 입력하세요.</h1>
            <form action="/chat/" method="POST">
                <input type="text" name="username" placeholder="이름 입력">
                <input type="submit" value="완료">
            </form>
        </div>
    '''
    return template('Main Page', getName)

# user마다 채팅 기록을 저장하는 딕셔너리 (전역 변수)
chat_history = {}

@app.route('/chat/', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        global chat_history
        chatting = ''
        autoSubmitForm = None

        # index에서 처음 넘어왔을 때 -> 전역 변수 user_dict에 username 등록 
        if 'username' in request.form.keys():
            username = request.form['username']

            #채팅 입력 form
            chatting = getTextForm(username, 1)

            #채팅 내역
            chat_history[username] = f'''
                <p>[BeatusChatBot] Hello, {username}!</p> 
            '''
            chatting += chat_history[username]

        # 채팅을 입력했을 때 -> dlgHandler를 통해 응답 받은 후 출력
        elif 'usertext' in request.form.keys():
            username = request.form['current_username']
            usertext = request.form['usertext']
            dlg_state = int(request.form['dlg_state'])
            output, new_state = dlgHandler.handle_chat(usertext, dlg_state)

            # 채팅 입력 form
            chatting = getTextForm(username, new_state)

            # 채팅 내역
            # css 
            if usertext != '':
                chat_history[username] += f'''
                <div style="width=100%; border: 2px solid #09c;"><p style="border:1px solid blue; background-color:yellow; border-radius:40px; width:500px;">[{username}] {usertext}</p></div>
                '''
            if output != '':
                chat_history[username] += f'''
                    <div style="width = 100%; border: 2px solid #09c; background-color: #9EC3E3;"><p style="background-color: white;">[BeatusChatBot] {output}</p></div>
                '''
            chatting += chat_history[username]

            # 대화 state 값이 100 이상일 때 채팅 입력 form 자동 제출
            if new_state >= 100:
                autoSubmitForm = 'getUserText'

        return template('Chat Page', chatting, auto_submit = autoSubmitForm)

    elif request.method == 'GET':
        return 'ERROR'

if __name__ == '__main__':
    app.run(debug=True)
