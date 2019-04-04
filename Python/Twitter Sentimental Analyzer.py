import sys,tweepy,csv,re
from textblob import TextBlob
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QLabel

class SentimentAnalysis(QWidget):

    def __init__(self):
        super().__init__()
        self.tweets = []
        self.tweetText = []
        self.title = 'BDA Mini Project: Tweet Sentiment Analysis'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
		

		# Create Label
        self.label1 = QLabel('Search Term:', self)
        self.label1.move(20, 20)
        self.label1.resize(280,40)

        # Create textbox
        self.textbox1 = QLineEdit(self)
        self.textbox1.move(120, 20)
        self.textbox1.resize(280,40)
        
        # Create Label
        self.label2 = QLabel('No of tweets:', self)
        self.label2.move(20, 80)
        self.label2.resize(280,40)

        # Create textbox
        self.textbox2 = QLineEdit(self)
        self.textbox2.move(120, 80)
        self.textbox2.resize(280,40)

        # Create Label
        self.label3 = QLabel('-', self)
        self.label3.move(20, 200)
        self.label3.resize(700,150)
 
        # Create a button in the window
        self.button = QPushButton('Analyze!', self)
        self.button.move(200,140)
        self.button.clicked.connect(self.on_click)
        self.show()

    def DownloadData(self, searchTerm, NoOfTerms):
        # authenticating
        consumerKey = 'DZIF3QS3wf8pYC7mZr6zGdKkM'
        consumerSecret = 'fi0fR2GPZNO4ex2g83coD6kinTzu5OPBaNgGIMO5uFWOEMYqSw'
        accessToken = '448140491-9geQ6MbH0voyY9jPYp51jaTYj0m4b5L25rPLI0ly'
        accessTokenSecret = 'owBK4P7Um0szSkKVt1jR89VBcCOSHlbqaiAKRg8080jj5'
        auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
        auth.set_access_token(accessToken, accessTokenSecret)
        api = tweepy.API(auth)

        # input for term to be searched and how many tweets to search
        #searchTerm = input("Enter Keyword/Tag to search about: ")
        #NoOfTerms = int(input("Enter how many tweets to search: "))

        # searching for tweets
        self.tweets = tweepy.Cursor(api.search, q=searchTerm, lang = "en").items(NoOfTerms)

        # Open/create a file to append data to
        csvFile = open('result.csv', 'a')

        # Use csv writer
        csvWriter = csv.writer(csvFile)


        # creating some variables to store info
        polarity = 0
        positive = 0
        wpositive = 0
        spositive = 0
        negative = 0
        wnegative = 0
        snegative = 0
        neutral = 0


        # iterating through tweets fetched
        for tweet in self.tweets:
            #Append to temp so that we can store in csv later. I use encode UTF-8
            self.tweetText.append(self.cleanTweet(tweet.text).encode('utf-8'))
            # print (tweet.text.translate(non_bmp_map))    #print tweet's text
            analysis = TextBlob(tweet.text)
            # print(analysis.sentiment)  # print tweet's polarity
            polarity += analysis.sentiment.polarity  # adding up polarities to find the average later

            if (analysis.sentiment.polarity == 0):  # adding reaction of how people are reacting to find average later
                neutral += 1
            elif (analysis.sentiment.polarity > 0 and analysis.sentiment.polarity <= 0.3):
                wpositive += 1
            elif (analysis.sentiment.polarity > 0.3 and analysis.sentiment.polarity <= 0.6):
                positive += 1
            elif (analysis.sentiment.polarity > 0.6 and analysis.sentiment.polarity <= 1):
                spositive += 1
            elif (analysis.sentiment.polarity > -0.3 and analysis.sentiment.polarity <= 0):
                wnegative += 1
            elif (analysis.sentiment.polarity > -0.6 and analysis.sentiment.polarity <= -0.3):
                negative += 1
            elif (analysis.sentiment.polarity > -1 and analysis.sentiment.polarity <= -0.6):
                snegative += 1


        # Write to csv and close csv file
        csvWriter.writerow(self.tweetText)
        csvFile.close()

        # finding average of how people are reacting
        positive = self.percentage(positive, NoOfTerms)
        wpositive = self.percentage(wpositive, NoOfTerms)
        spositive = self.percentage(spositive, NoOfTerms)
        negative = self.percentage(negative, NoOfTerms)
        wnegative = self.percentage(wnegative, NoOfTerms)
        snegative = self.percentage(snegative, NoOfTerms)
        neutral = self.percentage(neutral, NoOfTerms)

        # finding average reaction
        polarity = polarity / NoOfTerms

        # printing out data
        print("How people are reacting on " + searchTerm + " by analyzing " + str(NoOfTerms) + " tweets.")
        print()
        print("General Report: ")

        if (polarity == 0):
            print("Neutral")
        elif (polarity > 0 and polarity <= 0.3):
            print("Weakly Positive")
        elif (polarity > 0.3 and polarity <= 0.6):
            print("Positive")
        elif (polarity > 0.6 and polarity <= 1):
            print("Strongly Positive")
        elif (polarity > -0.3 and polarity <= 0):
            print("Weakly Negative")
        elif (polarity > -0.6 and polarity <= -0.3):
            print("Negative")
        elif (polarity > -1 and polarity <= -0.6):
            print("Strongly Negative")
        
        result = str(positive) + ' % people thought it was positive\n' + str(wpositive) + ' % people thought it was weakly positive\n' + str(negative) + ' % people thought it was negative\n' + str(wnegative) + ' % people thought it was weakly negative\n' + str(snegative) + ' % people thought it was strongly negative\n' + str(neutral) + ' % people thought it was neutral'

        #print()
        #print("Detailed Report: ")
        #print(str(positive) + "% people thought it was positive")
        #print(str(wpositive) + "% people thought it was weakly positive")
        #print(str(spositive) + "% people thought it was strongly positive")
        #print(str(negative) + "% people thought it was negative")
        #print(str(wnegative) + "% people thought it was weakly negative")
        #print(str(snegative) + "% people thought it was strongly negative")
        #print(str(neutral) + "% people thought it was neutral")

        self.label3.setText(result)
        self.plotPieChart(positive, wpositive, spositive, negative, wnegative, snegative, neutral, searchTerm, NoOfTerms)


    def cleanTweet(self, tweet):
        # Remove Links, Special Characters etc from tweet
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", tweet).split())

    # function to calculate percentage
    def percentage(self, part, whole):
        temp = 100 * float(part) / float(whole)
        return format(temp, '.2f')

    def plotPieChart(self, positive, wpositive, spositive, negative, wnegative, snegative, neutral, searchTerm, noOfSearchTerms):
        labels = ['Positive [' + str(positive) + '%]', 'Weakly Positive [' + str(wpositive) + '%]','Strongly Positive [' + str(spositive) + '%]', 'Neutral [' + str(neutral) + '%]',
                  'Negative [' + str(negative) + '%]', 'Weakly Negative [' + str(wnegative) + '%]', 'Strongly Negative [' + str(snegative) + '%]']
        sizes = [positive, wpositive, spositive, neutral, negative, wnegative, snegative]
        colors = ['yellowgreen','lightgreen','darkgreen', 'gold', 'red','lightsalmon','darkred']
        patches, texts = plt.pie(sizes, colors=colors, startangle=90)
        plt.legend(patches, labels, loc="best")
        plt.title('How people are reacting on ' + searchTerm.capitalize() + ' by analyzing ' + str(noOfSearchTerms) + ' Tweets.')
        plt.axis('equal')
        plt.tight_layout()
        plt.show()

    def on_click(self):
        searchTerm = self.textbox1.text()
        NoOfTerms = self.textbox2.text()
        #print(type(NoOfTerms))
        NoOfTerms = int(NoOfTerms)
        #print(type(NoOfTerms))
        #print (searchTerm)
        print (NoOfTerms)
		#os.system('python3 twitter.py '+str(values))
        self.DownloadData(searchTerm, NoOfTerms)

if __name__== "__main__":
    app = QApplication(sys.argv)
    sa = SentimentAnalysis()
    #sa.DownloadData()
    sys.exit(app.exec_())