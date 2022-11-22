import torch
from transformers import PreTrainedTokenizerFast
from transformers import BartForConditionalGeneration

class DialogueHandler:

    def __init__(self):
        self.tokenizer = PreTrainedTokenizerFast.from_pretrained('digit82/kobart-summarization')
        self.model = BartForConditionalGeneration.from_pretrained('digit82/kobart-summarization')

        self.saved_explanation = ''


    def handle_chat(input, is_explaining):
        output = ''

        if input == '설명 시작':
            is_explaining = True
        elif input == '설명 끝':
            is_explaing = False

        if is_explaining:
            output = '설명 중'

        return output, is_explaining