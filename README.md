## Project
### Stock Prediction using Financial News Sentiment Analysis and Time Series Forecasting

## Project Proposal:
https://codelabs-preview.appspot.com/?file_id=1TyFR1jlvE59nKuilDi-f81CGV9NqJZscQYVdNB1wxhE#0

## Project Report:
https://codelabs-preview.appspot.com/?file_id=1mx82bA7TVTtCWliCPi2ZfzDeMAPvKqDgOvrzML4R3DE#0

## Web Application:
https://stock-prediction-analysis.herokuapp.com/

## Project Structure
```
Project
├── README.md
├── Config file
├── Company Keywords
│   └── keywords to categorize the articles
├── Data: Scripts to scrape the data and api to get stock data
│   └── StockAPI_Alphavantage.py
│   └── WSJScrapper_Headline.py
│   └── WSJScrapper_Content.py
│   └── sentiment_analysis.py
│   └── test_data.csv
├── Dockerfile: instruction for docker image construction.
├── requirements.txt: dependencies.
├── GlueScripts: Scripts for AWS Gule 
│   └── Pyspark scripts for each pipeline
├── webapp: code for flask webapp
│   └── templates: html and css templates for web app
│   └── app.py
│   └── Procfile
│   └── runtime.txt
│   └── License
├── Readme.MD
```



## Getting Started

#### Prerequisites
1. Python3.5+
2. Docker
3. Flask
4. AWS
5. Heroku


#### Configuring the AWS CLI
You need to retrieve AWS credentials that allow your AWS CLI to access AWS resources.

1. Sign into the AWS console. This simply requires that you sign in with the email and password you used to create your account. If you already have an AWS account, be sure to log in as the root user.
2. Choose your account name in the navigation bar at the top right, and then choose My Security Credentials.
3. Expand the Access keys (access key ID and secret access key) section.
4. Press Create New Access Key.
5. Press Download Key File to download a CSV file that contains your new AccessKeyId and SecretKey. Keep this file somewhere where you can find it easily
6. Get AWS Key and create a config file
7. Go to https://www.alphavantage.co and get API key to retrive the stock data and paste it in a config file.

#### Steps to get Data
1. git clone the repo https://github.com/jayeshpatil130/CSYE7245_BDIA/tree/master/Final_Project
2. In data folder we have file to run the api and Scrapper function this are aslo sechduled with AWS Lambda in AWS console to run daily
3. This will get us the data in S3 bucket.
4. Now we will have a Data in S3 bucket now run AWS gule scripts or open the glue job from AWS console to perform and classify the data and to create a etl workflow which will update our redshift datawarehouse.

#### Aws Comprehend:
1. In this repo we have python script for sentiment_analaysis we need to run that in order to get sentiment score of the scrapped data which will trigger the aws gule workflow to run the gule jobs which add the data in redshift data warehouse.

#### AWS Forecast Setup:
1. Sign in to the AWS Management Console and open the Amazon Forecast console.
2. On the Amazon Forecast home page, choose Create dataset group.
3. On the Create dataset group page, for Dataset group details, provide the Dataset group name and Forecasting domain – From the drop-down menu, choose Custom.
4. On the Create target time series dataset page, for Dataset details, provide the following information:
5. Dataset name – Enter a name for your dataset.
6. Frequency of your data – In our case, it was daily.
7. On the Import target time series data page, for Dataset import job details, provide the following information:
8. Dataset import job name – Enter a name for your dataset.
9. Timestamp format – We chose  (yyyy-MM-dd). The format must be consistent with the input time series data.
10. IAM role – Keep the default Enter a custom IAM role ARN.
11. Data Location - se the following format to enter the location of your .csv file on Amazon S3:
s3://<name of your S3 bucket>/<folder path>/<filename.csv>
12. Import Dataset we created, Train the Predictor by choosing the algorithm(ARIMA in our case) and generate the forecast.
  
#### Deploying the webapp on heroku:
1. Download heroku toolbelt from  https://toolbelt.heroku.com/
2. Creating requirements.txt in which the dependencies for the package are listed on each line in the same folder as app.py. We can list the following:
Flask,
gunicorn
3. Creating runtime.txt which tells Heroku which Python version to use. We have used python-3.5.1
4. Create a Procfile. It is a text file in the root directory of the application that defines process types and explicitly declares what command should be executed to start our app. It can contain:
web: gunicorn app:app --log-file=-
5. We need to create a GitHub repository with app.py and these essential files along with.gitignore(Although it is not necessary it is recommended to include it)
6. Now our Flask app folder contains the this file structure
```
 ├── .gitignore
 ├── Procfile
 ├── app.py
 ├── requirements.txt
 │── runtime.txt
 ```
7. Go on Heroku website and after logging in click on New → Create New App.
Enter ”App name” and select the region and click on Create App and in the Deploy tab, select GitHub in Deployment method then Select the repository name and click Connect
8. Select Enable Automatic Deploys so that whenever we push changes to our GitHub it reflects on our app and Click Deploy Branch  which will deploy the current state of the branch.
If everything is successful it shows an Open App button. We can now open the app deployed on Heroku


#### Docker setup for app:
1. git clone the repo https://github.com/jayeshpatil130/CSYE7245_BDIA/tree/master/Final_Project
2. docker build -t stock_app:1.0 . -- this references the Dockerfile at . (current directory) to build our Docker image & tags the docker image with stock_app:1.0
3. Run docker images & find the image id of the newly built Docker image, OR run docker images | grep stock_app:1.0 | awk '{print $3}'
4. docker run -it --rm -p 5000:5000 {image_id} stock_app:1.0 -- this refers to the image we built to run a Docker container.

### Tests:
1. Heroku- Once App is deployed, you can spin the app from your browser, to see if its working or not.
2. Docker- You test it on 0.0.0.0:5000 or using docker-machine ip (eg : http://192.168.99.100:5000/)


## Authors
<b>[Sharvari Karnik](https://www.linkedin.com/in/sharvarikarnik25/)</b> 

<b>[Kunal Jaiswal](https://www.linkedin.com/in/kunaljaiswal4393/)</b> 

<b>[Jayesh Patil](https://www.linkedin.com/in/jayeshpatil130/)</b> 

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
