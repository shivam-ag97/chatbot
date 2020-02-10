from flask import Flask,jsonify,request,render_template, url_for, session, redirect
from flask_restful import Api, Resource
from pymongo import MongoClient
import os


app = Flask(__name__)
api = Api(app)
app.secret_key = 'qweasb@#12344'
client = MongoClient('mongodb+srv://shivam:shivam@cluster0-3mbds.mongodb.net/test?retryWrites=true&w=majority')
db = client.get_database('chatbot')
users = db.users


@app.route('/')
def index():
	if 'username' in session:
		# user=session['user_name']
		# user={'username' : user}
		# return render_template('chatbot.html',user=user)
		return 'Hi! You are logged in as ' + session['user_name']
	return render_template('index.html')


def get_history():
	his=db.history.find({'user_id':session['user_id']})
	# history =[]
	# for hs in his:
		# return jsonify(('{0} , {1}'.format(hs[0],hs['Bot'])))
	retData = []
	for hs in his:
		retData.append((' User: {0} , Bot: {1}'.format(hs['user'],hs['bot'])))
	# return jsonify('{0} , {1}'.format(his[0]['user'],his[0]['Bot']))
	return retData
	# his[0]['user']


@app.route('/history',methods=['GET'])
def history():
	return render_template('his.html', history=get_history())

@app.route('/login',methods=['POST','GET'])
def login():
	login_user = users.find_one({'user_id' : request.form['userid']})

	if login_user:
		p=request.form['pass']
		if p == login_user['pw']: 
			session['user_id']=request.form['userid']
			# history=db.history
			# chathis = history.find({'user_id': login_user['user_id']})
			user = login_user['user_name']
			user = {'username': user}
			# output = []
			# for i in chathis:
			# 	output.append({'bot' : chathis['']})
			return render_template('chatbot.html',user=user, history=get_history())
		return "Invalid userID or password"
	return "Invalid Credentials"



@app.route("/get")
#function for the bot response
def get_bot_response():
    userText = request.args.get('msg')
    chats = db.chat
    history = db.history
    questions=chats.find({})

    minDist=4;
    rpl="Please be more specific!"
    for q in questions:
    	t = editDistDP(q['msg'],userText,len(q['msg']),len(userText))
    	if(t<minDist):
    		minDist=t
    		rpl=q['rpl']


    # for q in ques


    # reply = chats.find_one({'msg' : userText})
    # if reply:
    # 	rpl = reply['rpl']
    # else:
    # 	rpl = "Sorry,Idk"

    history.insert({'user_id':session['user_id'],
    				'user' : userText,
    				'bot' : rpl
    				})
    return rpl


	

@app.route('/register',methods=['POST','GET'])
def register():
	if request.method == 'POST':
		existing_user = users.find_one({'user_id' : request.form['userid']})

		if existing_user is None:
			users.insert({'user_id' : request.form['userid'],'pw' : request.form['pass'],'user_name' : request.form['username']})
			session['user_name'] = request.form['username']
			return redirect(url_for('index'))

		return " User already registered! "
	return render_template('register.html')




# A Dynamic Programming based Python program for edit 
# distance problem 
def editDistDP(str1, str2, m, n): 
	dp = [[0 for x in range(n + 1)] for x in range(m + 1)]  
	for i in range(m + 1): 
		for j in range(n + 1):
			if i == 0: 
				dp[i][j] = j # Min. operations = j 
			elif j == 0: 
				dp[i][j] = i # Min. operations = i 

			elif str1[i-1] == str2[j-1]: 
				dp[i][j] = dp[i-1][j-1] 

			else: 
				dp[i][j] = 1 + min(dp[i][j-1],	 # Insert 
								dp[i-1][j],	 # Remove 
								dp[i-1][j-1]) # Replace 
	return dp[m][n] 



if __name__=="__main__":
	app.run(debug=True)