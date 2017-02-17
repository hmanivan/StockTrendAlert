import datetime

# date in the format of yyyy/mm/dd
#Assuming that ticker is 4 characters long eg. YHOO, GOOG, APPL, as presented in project specs
def checkDateRange(d):
	today=datetime.date.today()
	margin = datetime.timedelta(days = 7)
	year=int(d[0:4])
	month= int(d[5:7])
	day= int(d[8:10])
	return (today -margin <= datetime.date(year,month,day ))

def getFriendAlerts():
	friendAlerts = []
	transcationStrings = []
	filterTradeTransactionsByDate = []
	friendsList = getFriendsListForUser()

	for friend in friendsList:
		trades = getTradeTransactionsForUser(friend)
		for trade in trades:
			transcationStrings.append(trade)

	#filter Trade Transcation by those that were made only in the past week
	for transaction in transcationStrings:
		if checkDateRange(transaction):
			filterTradeTransactionsByDate.append(transaction);

	activity = []		
	#remove date crud from  filterTradeTranscationsByDate
	for transaction in filterTradeTransactionsByDate:
		activity.append(transaction[11:])

	#REPLACE BUY OR SELL WITH RESPECTIVE 1 or -1
	for index in range(len(activity)):
		activity[index]=activity[index].replace("BUY","1")
		activity[index]=activity[index].replace("SELL","-1")

	#add all unique ticker 
	ticker = set()
	for a in activity:
		ticker.add(a[-4:])
	
	#use a dictionary to represent the key value pair of (ticker, netAmount) eg (YHOO,2)
	netAmount=0
	netTicker = { }	
	for tick in ticker:
		for a in activity:
			if tick == a[-4:]:
				netAmount = netAmount + int(a[:-5])
				netTicker[tick] =netAmount
		netAmount=0

	#set up list of friend alerts "<net_friends>,<BUY|SELL>,<ticker>"
	transactionType = " " 
	alert= " "
	for tick in ticker:
		if netTicker.get(tick) != 0:
			if netTicker.get(tick) > 0:
			 	 transactionType = "BUY" 
			elif netTicker.get(tick) < 0:
				  transactionType = "SELL"
			alert = str(abs(int(netTicker.get(tick)))) + "," + transactionType + "," + tick
			friendAlerts.append(alert)

	friendAlerts.sort(reverse=True)
	return friendAlerts 

#library functions implemented for test purposes
def getFriendsListForUser():
	friendsList= ["F1" , "F2" , "F3"]
	return friendsList

def getTradeTransactionsForUser(user_id):
	trades = [];
	if user_id == "F1":
		 trades = ["2017-02-12,BUY,APPL","2017-02-14,SELL,YHOO","2017-02-11,BUY,GOOG"]
	elif user_id == "F2":
		trades = ["2017-02-12,BUY,APPL","2017-02-14,BUY,YHOO","2017-02-11,SELL,GOOG"]
	elif user_id == "F3":
		trades = ["2015-02-12,BUY,APPL","2017-02-14,SELL,YHOO","2016-02-11,BUY,GOOG"] 
	return trades

#printing final result with each alert in new line
print("\n".join(getFriendAlerts()))