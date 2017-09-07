# both python3 and python 2 compatible
# __author__ : Kutay YILMAZ
# __email__  : ktyylmz035@gmail.com

from random import shuffle

number_of_pairs = 10000

# people, m:men, w:women
m = list(range(number_of_pairs))
w = list(range(number_of_pairs,number_of_pairs*2))

# preferences of men and women [....,#3,#2,#1 ascenting ? (descenting at the same time :D)]
m_p = dict()
w_p = dict()

for i in range(number_of_pairs):
	#random prefs
	prefs = list(range(number_of_pairs,number_of_pairs*2))
	shuffle(prefs)
	m_p[i] = prefs

for i in range(number_of_pairs,number_of_pairs*2):
	#random prefs
	prefs = list(range(number_of_pairs))
	shuffle(prefs)
	
	prefs_shuffled = [0] * number_of_pairs

	for index,rank in enumerate(prefs):
		prefs_shuffled[rank] = index
	
	w_p[i] = prefs_shuffled[::-1]

# engagements
eng = dict((woman,None) for woman in w)

while m:
	# choosing an arbitrary man
	man = m.pop()
	# choosing the woman who is our man's first choice and not proposed by our man yet
	woman = m_p[man].pop()
	# if she doesn't have a partner then engage them
	if eng[woman]==None:
		eng[woman] = man
	else:
		other_man = eng[woman]
		like_list = w_p[woman]
		# find the man that our woman prefers
		if like_list[other_man] > like_list[man]:
			# if woman doesn't prefer our man, add him to free array
			m.append(man)
		else:
			# engage our man with the woman and set other_man free
			eng[woman] = man
			m.append(other_man)

#for woman,man in eng.items():
#	print("%s engages with %s <3" %(woman,man))

 
