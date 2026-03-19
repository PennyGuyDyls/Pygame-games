f=open('Wordle/Assets/guesses.txt','r')
words=[]

while True:
    word=f.readline().strip()
    if word=='':
        break
    if word not in words and len(word)==5:
        words.append(word)
    else: print(word)


f.close()

f=open('Wordle/Assets/guesses.txt','w')
for i in words:
    f.write(i+'\n')

f.close()

