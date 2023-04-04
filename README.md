# QR Code Coupon Generator and Sharing System

The QR Code Coupon Generating and Sharing System is a Python Flask-based application that utilizes Google Drive API. It was designed to distribute food coupons (QR codes) to people who have paid for Saraswati Puja Maha Bhog in 2023. The system generates a single QR code for a group of people (e.g., a family or a lab) who have paid together. The QR code is marked as void after it has been scanned n times, where n is the number of people in the group.

The application can generate QR codes and send them to the email addresses provided for each person. Upon scanning the QR code, the database is automatically updated, and it indicates whether the QR code is valid or void. A volunteer at the entrance of the event equipped with a smartphone can scan the QR code using any QR code scanning app. If a person tries to scan the same QR code for the (n+1)th time, it will be marked as void.

The interface provided by the application allows for easy updating of the database upon scanning of the QR code. The software is suitable for use in any event where coupons need to be distributed and managed.

Although the system has some limitations, such as taking 4-5 seconds to send each QR code and requiring a device to be present at the venue and powered on for the whole duration of the event(from sending the QR code to the end of the event), these issues can be mitigated if the venue has a strong connection to NISER-AP. In this case, the device can be located anywhere within NISER, and volunteers scanning the QR codes will only need to connect to NISER-AP to scan and update the system. These limitations are relatively minor and should not pose significant issues for the overall use of the system.

Here are instructions on how to use the system for your event.

## Step 1: Setting Up Google Drive and Google Cloud Project

1. You need to have `Python>=3.10.7` installed on your system.
2. *(Optional but Highly Recommended)* Make a virtual environment using `python -m virtualenv <virt-env name>` and activate it using `source <virt-env name>/bin/activate`(Linux) or `<virt-env name>\Scripts\activate`(Windows). If you do not have the `virtualenv` package installed, you can install it using `pip install virtualenv`. This package helps you to create a virtual environment for your project.
3. Install the required packages using `pip install -r requirements.txt`.
4. Follow [this](https://developers.google.com/workspace/guides/create-project) documentation page to create a Google Cloud Project using a suitable google account.
5. Go to your [google cloud console](https://console.cloud.google.com) and select the project you just created. On the top left corner, click on the hamburger menu and select `APIs & Services`, and then `Credentials`.
6. If you receive a warning that you haven't configured the `OAuth consent screen`, click on `Configure consent screen` and fill in the required details. Enabling it only for `Internal` Users will be enough (Users won't be all the persons receiving coupons. User will be only the computer which is used to send the QRs). You can skip the `Scopes` section for now. Finally hit the `Back to Dashboard` button.
7. Now on the `Credentials` page, click on `Create Credentials` and select `OAuth client ID`. The application type should be `Desktop app` and the name can be anything. Click on `Create`.
8. You will have a pop-up saying `OAuth client created`. Click on `Download JSON` and save the file as `credentials.json` in the same directory as `uploadandshare.py`. The JSON file will look something like this:

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

9. Go to [this](https://console.cloud.google.com/flows/enableapi?apiid=drive.googleapis.com) to enable the `Google Drive API` for your project. Make sure the correct project is selected in the top left corner.

## Step 2: The Files Required

First, make sure you have these files in your current directory:

1. **`credentials.json`**: This file is generated in the previous step.
2. **`people.csv`**: This file contains the list of people for whom you want to generate the QR codes. The file should have 3 columns, `name`, `email`, and the `count`. The `name` and `email` fields are self-explanatory. The `count` is the number of food coupons you want to give to that person. For example, if the `count` is 4, the QR code sent to that person can be scanned 4 times in the gate. An example of the `people.csv` file is given below:

   ```csv
   name,email,count
   John Smith,johnsmith@example.com,4
   Emily Davis,emilydavis@example.com,2
   Michael Johnson,michaeljohnson@example.com,1
   ```

3. **`local_settings.json`**: This file contains the settings for the project. There are three information to be provided in this file:
   * **`IP`**: The IP address of this computer in the local network. **This IP address is used by the scanning devices to locate your device in the local network.** This can be found by typing `ifconfig` in the Linux terminal (`ipconfig` in Windows). The IP address will be listed beside `IPv4 Address` in windows or `inet` in Linux. If directly connected to the intranet, it will be something like `10.0.x.x` or something like `192.168.x.x`. If you are connected to the intranet and also have hotspot enabled, you will see two IP addresses. In that case, if you want the scanning devices to be connected to the hotspot, use the IP address of the hotspot, else if you want them to connect to the intranet, use the IP address of the intranet.
   **Note:** It is **NOT** `127.0.0.1`
   * **`PORT`**: This is the port number. Can keep any port which is not being used. For example, `5000` or `8080`... ports in these ranges generally remain empty.
   * **`people`**: Although I have said that the `people.csv` file is required, you can keep any name to it, and provide the name of the file in this field. For example, if you named the file `people.csv`, this field should be `people.csv`. If you have named it `people_list.csv`, then this field should be `people_list.csv`. If you do not have the file in this very directory, just put the global path to the file in this field.
   **Note:** The file should be in the same format as the `people.csv` file mentioned above.

## Step 3: Generating the QR Codes

At this point, if the above steps are done correctly and you are connected to the same network at the same spot which will be used for scanning, just running the `generate_qrs.py` file should generate the QR codes. The QR codes have to be generated on the spot, connecting your laptop to the required network. The QR will contain the IP address of the computer, the port number, and a randomly generated string. The QR codes will be saved in the `QRs` directory. At this point, the code doesn't bother about who gets which QR code. It just generates QR codes sufficient for the number of people in the `people.csv` file. The QR codes are named as `<the_randomly_generated_string>.png`. Care has been taken to minimize the possibility of two randomly generated strings being exactly the same.

## Step 4: Uploading the QR Codes to Google Drive and share them to the concerned persons via Drive

1. Go to the function `give_permissions()` in the [`uploadandshare.py`](./uploadandshare.py) file. There draft the message to be sent to the people while sharing the QR codes with the people. The message can contain the following placeholders:
    * `{name}`: The name of the person.
    * `{count}`: The number of coupons the person is entitled to.
2. Run the `uploadandshare.py` file. If you are doing this for the first time, you will be asked to give this code permission to access your google drive. It should automatically launch the default browser and ask for permission. Here you need to select a `@niser.ac.in` account. The QR codes will be uploaded on the google drive of this account, and the emails will be sent from this account. **This is a one-time process.** As you give the permission, it will automatically generate a `token.json` file in the same directory. This file will be used to access your google drive in the future. If you feel you want to change the account, just delete the `token.json` file and run the `uploadandshare.py` file again. It will ask for permission again.
3. If already logged in, this file is supposed to take a while (about 4-5 seconds for every QR code) to run. This will upload the QR codes to Google Drive and share them with the concerned persons. The QR codes will be uploaded to a folder named `QR_Codes` in the root directory of your Google Drive. The folder will be created if it doesn't exist. (you can change the file name in the `uploadandshare.py` file line 45 as of today (03-04-2023) it might not be the same line number in the future)

## Step 5: Running the server and scanning the QR codes

1. Volunteers are supposed to connect to the same network as the computer running the server. They can either connect to the hotspot of the computer running the server, or connect to the intranet of the institute. As mentioned in *point #3 of step 2* if they had given the hotspot IP address in the `local_settings.json` file, they should connect to the hotspot, else they should connect to the intranet.
2. Do the Required changes in the [`templates/log.html`](./templates/log.html) file like the name of the event.
3. in the last line of the [`server.py`](./server.py) file, change the `debug=True` to `debug=False`. This is to prevent evil people from trying to tamper with the server.
4. Run the `server.py` file. This will start the server. The server will be running on the IP address and port number mentioned in the `local_settings.json` file. The server should be running on the same computer as the one running the `generate_qrs.py` file.
