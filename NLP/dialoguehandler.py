import torch
from transformers import PreTrainedTokenizerFast
from transformers import BartForConditionalGeneration
from NLP.textrank import *
import time
import random

class DialogueHandler:

    def __init__(self):
        self.tokenizer = PreTrainedTokenizerFast.from_pretrained('digit82/kobart-summarization')
        self.model = BartForConditionalGeneration.from_pretrained('digit82/kobart-summarization')

        self.saved_explanation = []
        self.is_explaining = False

        self.idle_dlgs = ['', '오...', '그렇구나~']

    def tr_keyword(self):
        tr = TextRank(window=5, coef=1)
        stopword = set([('있', 'VV'), ('하', 'VV'), ('되', 'VV'), ('없', 'VV') ])
        tr.load(ListTaggerReader(self.saved_explanation), lambda w: w not in stopword and (w[1] in ('NNG', 'NNP', 'VV', 'VA')))
        #print('Build...')
        tr.build()
        kw = tr.extract(0.1)

        s = ""
        for k in sorted(kw, key=kw.get, reverse=True)[:5]:
            s += k[0][0] + ', '
        return s[:-2]


    def abs_sum(self):
        text = ''
        for s in self.saved_explanation:
            text += s

        raw_input_ids = self.tokenizer.encode(text)
        input_ids = [self.tokenizer.bos_token_id] + raw_input_ids + [self.tokenizer.eos_token_id]

        summary_ids = self.model.generate(torch.tensor([input_ids]),  num_beams=4,  max_length=512,  eos_token_id=1)
        text = self.tokenizer.decode(summary_ids.squeeze().tolist(), skip_special_tokens=True)

        return text


    def handle_chat(self, inp, state):
        # state -> 여러 번 메시지를 보낼 때 얼마나 보냈는지 기록에 사용
        # 0: 다음 응답 기다림
        # 100번대: 입력된 말 요약 
        output = ''

        if state >= 100:
            if state == 100:
                output += '키워드로는\n'
                output += self.tr_keyword()
                output += '\n이 있겠네~'
                state += 1
            elif state == 101:
                output += '이제 네가 설명해준 내용을 요약해 볼게!'
                state += 1
            elif state == 102:
                output += '"' + self.abs_sum() + '"'
                self.saved_explanation = []
                state = 0
        
        else:
            state = 0
            if inp == '설명 시작':
                self.is_explaining = True
                output += '좋아, 설명해 봐!'
                state = 0
            elif inp == '설명 끝':
                self.is_explaining = False
                output += '설명 잘 들었어!'
                state = 100
            elif self.is_explaining:
                self.saved_explanation.append(inp)
                output += self.idle_dlgs[random.randint(0,len(self.idle_dlgs)-1)]
                state = 0
            
        
        return output, state


if __name__ == '__main__':
    d = DialogueHandler()

    while True :
        inp = input("->")
        state = 1
        while state > 0:
            print(state)
            output, state = d.handle_chat(inp, state)
            if output:
                print("* -> " + output)