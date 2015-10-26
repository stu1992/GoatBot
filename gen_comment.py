import markov
import summary as s
def generate_comment(comment):
	f = open('data.txt','r')
	markov_engine = markov.Markov(f)
	st = s.SummaryTool()
	sentences_dic = st.get_senteces_ranks(comment)
	summary = st.get_summary( comment, sentences_dic)
	words = summary.split(' ')
	response = ''
	for i in range(len(words)-2):
		try:
			first = words[i]
			second = words[i+1]
			response = markov_engine.generate_markov_text(first ,second)
			break;
		except:
			print 'fail'
			pass
	if response == '':
		response = markov_engine.generate_markov_text('this' ,'is')	
	return response


