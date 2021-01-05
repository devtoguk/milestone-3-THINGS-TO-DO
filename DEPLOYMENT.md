# Things To Do Places To Go - Deployment Information

[Live app deployed on Heroku](https://things-to-do-project.herokuapp.com/)

[Back to main README.md file](/README.md)

## Table of Contents
- [Running this project locally](#running-this-project-locally)
- [Deploying to Heroku](#deploying-to-heroku)

## Running this project locally
This app has been built using the GitPod IDE and GitHub for version control.

### The following is required:
- Github account
- Python (version 3.8)
- [MongoDB](https://account.mongodb.com/account/login) account
- [Amazon S3 Bucket](https://aws.amazon.com/s3/) account - for image storage and access
- [Heroku](https://signup.heroku.com/) account (only for deployment)

### Clone the repository
1. Login to GitHub.
2. Navigate to the projects repository “milestone-3-THINGS-TO-DO”
3. Click Clone or Download under the repository name.
4. To clone the repository using HTTPS, under “Clone with HTTPS”, click the [copy to clipboard] icon next to the URL field.
5. Open Git Bash on your local IDE.
6. Change the current working directory to the location where you want the cloned directory to be made.
7. Type ‘git clone’ and then paste the URL from the step above.
  ```
      git clone https://github.com/username/repository
  ```
8. Press Enter. Your clone will now be created.

For more information and troubleshooting on cloning a repository from GitHub click [here](https://help.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository).

### Install the Requirements
1. Go to the workspace for your local copy.
2. In a terminal window enter
  ```
    pip3 install -r requirements.txt
  ```

### Create the required MongoDB collections and index
1. Login to your MongoDB account
2. Create a cluster and then a database.
3. Create two collections in the database: users and activities.
4. Add a text index to the activities collection.
    1. From your cluster select your your database
    2. Select the activities collection
    3. In the right-hand panel choose 'Indexes' & click [Create Index] button
    4. In the fields section enter the following:
        ```
        {
        "title": "text",
        "shortDescr": "text"
        "longDescr": "text"
        "keywords": "text"
        }
        ```
    5. Click [Review], check your index then click [Confirm]

### Create AWS S3 Image Bucket
1. Login to AWS S3 and create a new S3 bucket for image storage.
2. Navigate to your AWS S3 service.
3. Select 'Buckets'.
4. Click the bucket you created.
5. Click the [Permissions] tab.
6. Ensure 'Block all public access' is set to ON, as well as the 4 sub-options below also set to ON.
7. Scroll down to 'Bucket Policy', select [Edit] and paste in the following, replacing the <> entries with your own value:
```
    {
        "Version": "2012-10-17",
        "Id": "http referer policy example",
        "Statement": [
            {
                "Sid": "Allow get requests originating from heroku app.",
                "Effect": "Allow",
                "Principal": "*",
                "Action": [
                    "s3:GetObject",
                    "s3:GetObjectVersion",
                    "s3:PutObject"
                ],
                "Resource": "arn:aws:s3:::<your_app_name>/*",
                "Condition": {
                    "StringLike": {
                        "aws:Referer": [
                            "https://<your_app_name>.herokuapp.com/*",
                            "*"
                        ]
                    }
                }
            }
        ]
    }
```
8. Scroll down to 'Cross-origin resource sharing (CORS)', select [Edit] and paste in the following:
```
    [
        {
            "AllowedHeaders": [
                "*"
            ],
            "AllowedMethods": [
                "GET",
                "HEAD",
                "POST",
                "PUT"
            ],
            "AllowedOrigins": [
                "*"
            ],
            "ExposeHeaders": []
        }
    ]
```

For more information and troubleshooting on creating an AWS S3 Bucket click [here](https://docs.aws.amazon.com/AmazonS3/latest/user-guide/create-bucket.html)

### Environment Variables
1. Add env.py to your .gitignore file
2. Create the env.py and add in the following replacing the <> entries with
your own values:
```
  import os

  os.environ.setdefault('IP', '0.0.0.0')
  os.environ.setdefault('PORT', '5000')
  os.environ.setdefault('SECRET_KEY', '<your_secret_key_here>')
  os.environ.setdefault('MONGO_URI',
    'mongodb+srv://root:<your_password>@<your_cluster_name>.qhb5p.mongodb.net/<your_dbname_here>?
    retryWrites=true&w=majority')
  os.environ.setdefault('MONGO_DBNAME', ',<your_dbname_here>')
  os.environ.setdefault('AWS_ACCESS_KEY_ID', '<your_aws_access_key_id_here>')
  os.environ.setdefault('AWS_SECRET_ACCESS_KEY', '<your_aws_secret_access_key_here>')
  os.environ.setdefault('AWS_DEFAULT_REGION', '<your_aws_region_here>')
  os.environ.setdefault('S3_BUCKET_NAME', '<your_s3_bucket_name_here>')
```

NOTE for MONGO_URI: Before entering your info for this copy your connection string from MongoDB
  - In MongoDB while on your cluster.
  - Choose 'Command Line Tools' on the cluster menu.
  - Now select [Connect Instructions] - [Connect your application]
  - Option (2) shows your connection string.

Run the App
- Open a terminal window in your IDE
- Type in:
  ```
  python3 app.py
  ```

## Deploying to Heroku
Use the steps below to deploy this app on Heroku:

### Setup Heroku
1. Create a Heroku account
2. Create a new app and select your region

### Local files required by Heroku
1. Create/update the requirements.txt file, in a terminal window type:
  ```
  pip3 freeze --local > requirements.txt
  ```
2. Create/update the Procfile, in a terminal window type:
  ```
    echo web: python run.py > Procfile
  ```

### Push files to Heroku
1. Login to Heroku, in terminal window type in the following and enter your user name and password:
  ```
    heroku login -i
  ```
2. Commit all your files.
3. Push the files to Heroku, in a terminal window type:
  ```
    git push heroku master
  ```
- If the push/build fails, investigate the errors and retry from step 2.

### Heroku Config Variables
1. Go to your Heroku account and select your app.
2. From the app menu select 'Settings'.
3. Click [Reveal Config Vars] to show the keys and the values.
4. Set the keys and values as below, replacing the <> entries with your values:

  | Key | Value |
  | --- | ---- |
  | IP | 0.0.0.0 |
  | PORT | 5000 |
  | SECRET_KEY | <your_secret_key_here> |
  | MONGO_URI | mongodb+srv://root:<your_password>@<your_cluster_name>.qhb5p.mongodb.net/<your_dbname_here>?retryWrites=true&w=majority |
  | MONGO_DBNAME | <your_dbname_here> |
  | AWS_ACCESS_KEY_ID | <your_aws_access_key_id_here> |
  | AWS_SECRET_ACCESS_KEY | <your_aws_secret_access_key_here> |
  | AWS_S3_ADDRESSING_STYLE | path |
  | AWS_DEFAULT_REGION | <your_s3_bucket_name_here> |
  | AWS_DEFAULT_REGION | <your_default_s3_bucket_region_here> |
  | AWS_S3_SIGNATURE_VERSION | s3v4 |
<br>

### Open the Heroku App
  1. At the top-right of the Heroku account window, click [Open app], the application will open in a new tab. The live URL for the app can be copied from the address bar e.g. https://things-to-do-project.herokuapp.com/
