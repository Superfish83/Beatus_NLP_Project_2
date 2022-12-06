from flask import *
app = Flask(__name__)

from NLP.dialoguehandler import DialogueHandler
dlgHandler = DialogueHandler()
botname = '어썸'

def template(title, content, auto_submit = None):
    t = f'''<!doctype html>
    
    <link rel="stylesheet" href="{ url_for('static', filename='design.css') }" media="(min-width:600px)">
    <html>
        <title>{title}</title>
        <header>
            <div id="logo">
                <a href = "/">
                    <img src="https://www.cnsa.hs.kr/images/hpw/common/logo.gif" alt="Logo" width="225" height="55" href="./index.html">
                </a>
            </div>

            <div id="top_menu">
                <h2> AwSUM </h2>
                <h4> KoBART와 TextRank를 이용한 학습용 챗봇 </h4>
            </div>
        </header>
        
        <article id="content" style="
    overflow-y: scroll;
    height: calc(100vh - 240px);
">
            {content}
        </article>
        
        <footer style="
    position: fixed;
    bottom: 0;
">
            <p>2022 Beatus</p>
            <p>AI Team | 2학년 김연준, 홍준혁</p>
            <p>Web Team | 1학년 조인성</p>
        </footer>
        <script>document.querySelector("article").scroll(0,99999999)</script>
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
            <form class = "input" name = "getUserText" action="/chat/" method="POST" style="
    position: fixed;
    bottom: 90px;
    width: 96%;
    height: 30px;
    padding: .5% 1%;
    display: flex;
">
                <input type="textarea" name="usertext" placeholder="채팅 입력" style="
    flex: 1; autofocus/">
                <input type="hidden" name="current_username" value={username}>
                <input type="hidden" name="dlg_state" value={dlg_state}>
                <input type="submit" value="입력">
            </form>'''
    else: # 챗봇이 계속 말할 때 (입력받는 것 없이 form 제출)
        form = f'''
            <form class = "input" name = "getUserText" action="/chat/" method="POST" style="
    position: fixed;
    bottom: 90px;
    width: 96%;
    height: 30px;
    padding: .5% 1%;
    display: flex;
">
                <input type="textarea" name="usertext" placeholder="채팅 입력" style="
    flex: 1;" readonly/>
                <input type="hidden" name="current_username" value={username}>
                <input type="hidden" name="dlg_state" value={dlg_state}>
            </form>
            '''
    return form

def getTextTemplate(name, text):
    if text == '':
        return ''

    if name != botname: #사용자의 입력
        return f'''
            <div>
                <p class="chattext-user">{text}</p>
            </div>
        '''
    else: #봇의 입력
        return f'''
            <div>
                <p class="chat-username">{name}</p>
                <p class="chattext-bot">{text}</p>
            </div>
        '''


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
        <ul>
            <h3><a href="/related-work/">텍스트 요약 원리</a></h3>
            <h3><a href="https://github.com/Superfish83/Beatus_NLP_Project_2">GitHub</a></h3>
        </ul>
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

            if username == botname:
                return '다른 이름을 설정하세요!'

            #채팅 내역
            chat_history[username] = getTextTemplate(botname, f'''안녕, {username}!
            "설명 시작"을 입력하고 나에게 설명하려는 내용을 입력한 뒤
            "설명 끝"을 입력하면 요약해 줄게.''')
            chatting += chat_history[username]
            
            #채팅 입력 form
            chatting += getTextForm(username, 1)

        # 채팅을 입력했을 때 -> dlgHandler를 통해 응답 받은 후 출력
        elif 'usertext' in request.form.keys():
            username = request.form['current_username']
            usertext = request.form['usertext']
            dlg_state = int(request.form['dlg_state'])
            output, new_state = dlgHandler.handle_chat(usertext, dlg_state)

            # 채팅 내역
            chat_history[username] += getTextTemplate(username, usertext)
            chat_history[username] += getTextTemplate(botname, output)
            chatting += chat_history[username]

            # 채팅 입력 form
            chatting += getTextForm(username, new_state)

            # 대화 state 값이 100 이상일 때 채팅 입력 form 자동 제출
            if new_state >= 100:
                autoSubmitForm = 'getUserText'

        t = '<div class="chat">'
        t += template('Chat Page', chatting, auto_submit = autoSubmitForm) + '</div>'
        return t

    elif request.method == 'GET':
        return 'ERROR'

@app.route('/related-work/')
def related_work():
    return render_template('related_work.html')

if __name__ == '__main__':
    app.run(debug=True)
