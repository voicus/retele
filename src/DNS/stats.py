import matplotlib.pyplot as plt

keywords = ['google', 'facebook', 'amazon', 'yahoo', 'xiaomi', 'youtube', 'mozilla']
mp = {x:0 for x in keywords}
with open("tmp.txt") as f:
    for line in f:
        for x in keywords:
            if x in line:
                mp[x] = mp[x] + 1
      

print(mp)          
plt.figure()
plt.hist(mp.keys(), weights=mp.values())
plt.show()
