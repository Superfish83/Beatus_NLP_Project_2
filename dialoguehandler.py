import torch
from transformers import PreTrainedTokenizerFast
from transformers import BartForConditionalGeneration
from textrank import *

class DialogueHandler:

    def __init__(self):
        self.tokenizer = PreTrainedTokenizerFast.from_pretrained('digit82/kobart-summarization')
        self.model = BartForConditionalGeneration.from_pretrained('digit82/kobart-summarization')

        self.saved_explanation = []
        self.is_explaining = False

    def tr_keyword(self):
        tr = TextRank(window=5, coef=1)
        stopword = set([('있', 'VV'), ('하', 'VV'), ('되', 'VV'), ('없', 'VV') ])
        tr.load(ListTaggerReader(self.saved_explanation), lambda w: w not in stopword and (w[1] in ('NNG', 'NNP', 'VV', 'VA')))
        #print('Build...')
        tr.build()
        kw = tr.extract(0.1)

        s = ""
        for k in sorted(kw, key=kw.get, reverse=True)[:5]:
            for k_ in k:
                s += k_[0] + ', '
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


    def handle_chat(self, inp):
        output = ''

        if inp == '설명 시작':
            self.is_explaining = True
            output += '좋아, 설명해 봐!'
        elif inp == '설명 끝':
            self.is_explaining = False
            
            output += '오~ 설명 잘 들었어\n'

            output += '키워드로는\n'

            output += self.tr_keyword()

            output += '\n이 있겠네~\n이제 네가 설명해준 내용을 요약해 볼게!\n'

            output += '"' + self.abs_sum() + '"'

            self.saved_explanation = []
        elif self.is_explaining:
            self.saved_explanation.append(inp)

        return output


if __name__ == '__main__':
    d = DialogueHandler()

    while(True):
        output = d.handle_chat(input("->"))
        if output:
            print("* -> " + output)