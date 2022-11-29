from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)



from NLP.dialoguehandler import DialogueHandler
#d = DialogueHandler()
#while(True):
#    output = d.handle_chat(input("->"))
#    if output:
#        print("* -> " + output)