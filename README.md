# Setting Up from Scratch

1. You need to have `Python>=3.10.7` installed on your system.
2. *(Optional but Highly Recommended)* Make a virtual environment using `python -m virtualenv venv` and activate it using `source venv/bin/activate`(Linux) or `venv\Scripts\activate`(Windows). If you do not have the `virtualenv` package installed, you can install it using `pip install virtualenv`. This package helps you to create a virtual environment for your project.
3. Install the required packages using `pip install -r requirements.txt`.
4. Follow [this](https://developers.google.com/workspace/guides/create-project) documentation page to create a Google Cloud Project using a suitable google account.
5. Go to your [google cloud console](https://console.cloud.google.com) and select the project you just created. On the top left corner, click on the hamburger menu and select `APIs & Services` and then `Credentials`.
6. If you recieve a warning that you haven't configured `OAuth consent screen`, click on `Configure consent screen` and fill in the required details. Enabling it only for `Internal` Users will be enough (Users won't be all the persons recieving coupons. User will be only the computer which is used to send the QRs). You can skip the `Scopes` section for now. Finally hit the `Back to Dashboard` button.
7. Now in the `Credentials` page, click on `Create Credentials` and select `OAuth client ID`. Application type should be `Desktop app` and name can be anything. Click on `Create`.
8. You will have a pop up saying `OAuth client created`. Click on `Download JSON` and save the file as `credentials.json` in the same directory as `uploadandshare.py`. The json file will look something like this:

	```json
	{
	"installed": {
		"client_id": "somerandomstringdefinitelynotthis.apps.googleusercontent.com",
		"project_id": "saraswati-puja-somenumber",
		"auth_uri": "https://accounts.google.com/o/oauth2/auth",
		"token_uri": "https://oauth2.googleapis.com/token",
		"auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
		"client_secret": "someotherrandomstring",
		"redirect_uris": ["http://localhost"]
	}
	}

	```
9.  Go to [this](https://console.cloud.google.com/flows/enableapi?apiid=drive.googleapis.com) to enable the `Google Drive API` for your project.

# Usage

Asuming that setup is complete following the steps above in the [`Setting Up from Scratch`](#setting-up-from-scratch) section.

## Step 1: Generating the QR Codes

Incomplete...