f=open('Wordle/Assets/guesses.txt','r')
words=[]

while True:
    word=f.readline().strip().upper()
    if word=='':
        break
    words.append(word)



f.close()

f=open('Wordle/Assets/answers.txt','r')

while True:
    word=f.readline().strip().upper()
    if word=='':
        break
    if word not in words:
        words.append(word)

f.close()

words.sort()
f=open('Wordle/Assets/guesses.txt','w')

for i in words:
    f.write(i+'\n')

f.close