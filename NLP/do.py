#textrank.py의 함수 모두 불러오기( networkx 라이브러리가 필요함 )
from NLP.textrank import *

# 파일 열기 (나중에 경로 바꿔야 함), w는 write의 약자. w썼을 때 입력 가능.
f = open('C:/Users/홍준혁/inputtext.txt', 'w')
# 파일에 텍스트 쓰기
f.write(input())
# 파일 닫기
f.close()
#window:문맥으로 사용할 단어의 개수. 기본값 5로 주면 특정 단어의 좌우 5개씩, 총 10개 단어를 문맥으로 사용
#coef동시출현 빈도를 weight에 반영하는 비율. 기본값은 1.0로, 동시출현 빈도를 weight에 전부 반영. 0.0일 경우 빈도를 반영하지 않고 모든 간선의 weight을 1로 동일하게 간주
#threshold:말그대로 임계값. 문서 요약시 관련있는 문장으로 여길 최소 유사도값. 기본값은 0.005. 그 이하 처리 안함(얘는 textrank 파일에서 바꿀 수 있음.textrank함수에.)
tr = TextRank(window=5, coef=1)
print('Load...')
stopword = set([('있', 'VV'), ('하', 'VV'), ('되', 'VV'), ('없', 'VV') ])
tr.load(RawTaggerReader('inputtext.txt'), lambda w: w not in stopword and (w[1] in ('NNG', 'NNP', 'VV', 'VA')))
print('Build...')
tr.build()
kw = tr.extract(0.1)
for k in sorted(kw, key=kw.get, reverse=True):
    print("%s\t%g" % (k, kw[k]))

#다시 쓸 수 있도록 파일 정리 작업
f = open('C:/Users/홍준혁/inputtext.txt', 'w')
f.write("")
f.close()
