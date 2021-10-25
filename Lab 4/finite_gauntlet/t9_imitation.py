from collections import Counter
import re
import itertools 

all_words=Counter()
n2l={1:'\'', 2:'abc',3:'def',4:'ghi',5:'jkl',6:'mno',7:'pqrs',8:'tuv',9:'wxyz'}


with open('./dict/words.txt','r') as di:  # UNIX 250k unique word list 
     all_words.update({line.strip() for line in di if len(line) < 6}) 

with open('./dict/x_train.txt','r') as fin:  
    for line in fin:
         all_words.update([word.lower() for word in re.findall(r'\b\w+\b',line)])

def combos(nums):
    t=[n2l[i] for i in nums]
    return tuple(''.join(t) for t in itertools.product(*(t)))

def t9(nums):
    combo=combos(nums)
    c1=combos([nums[0]])
    first_cut=(word for word in all_words if word.startswith(c1))
    return (word for word in first_cut if word.startswith(combo))

def try_it(nums):
    s=set(t9(nums))
    result = []
    for i, word in enumerate(
          [w for w in sorted(all_words,key=all_words.get, reverse=True) if w in s],1):
        if i<=5:
            result.append(word)
    return result