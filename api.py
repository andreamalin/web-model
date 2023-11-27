import requests
import json 
api_url = "https://deaflens-xa3v62ac2q-uc.a.run.app/v1"

sign_language_ids = {
    "LENSEGUA": "651b5d410ae23c0573d7953e",
    "ASL": "651b5d660ae23c0573d7953f"
}

def get_cdn_signed_url():    
    headers = {
        'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6ImFkNWM1ZTlmNTdjOWI2NDYzYzg1ODQ1YTA4OTlhOWQ0MTI5MmM4YzMiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vZGVhZmxlbnMiLCJhdWQiOiJkZWFmbGVucyIsImF1dGhfdGltZSI6MTY5NTk2MjY3OSwidXNlcl9pZCI6Im9xd1RFTXgweGZRb2l6UjJPU0dGQVpqUzBtdDEiLCJzdWIiOiJvcXdURU14MHhmUW9pelIyT1NHRkFaalMwbXQxIiwiaWF0IjoxNjk1OTYyNjc5LCJleHAiOjE2OTU5NjYyNzksImVtYWlsIjoia2VuaWZveDBAZ21pbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZW1haWwiOlsia2VuaWZveDBAZ21pbC5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJwYXNzd29yZCJ9fQ.P83AxaRcTJk1oHFHO3jAf9XwXGWhjxFsx5ufbrlluyf41BN-NFT7LOfs-HsLP7w84TgxLzbYA3An7GNNRkbEKaay2kmi8XCdVtZIgsqRsUerkwSzKlM7mPjmd55_50ReIDKUoaGOH5kflsnsfnnEvh8Z2kADptFEJqjDiHWLNkbtXVbboFQ20gdFs7953Z69CSuJvL3Ov4ci55pAUbW8vv_u4qyB1i_uszJWCfsN84FIxcDIkCeRS_Ifqcxadf68ZLwzjln8iRH59uqAOH685sJwT7ZOVnaj_dKCu2mrkLbv7x7oHgwFldndf5zI5JnlcjU5ca-v_vCykVBX1gEkFg'
    }
    data = {'apiUsername': "W4B.n-sdsh",
            'apiPassword': '7AuY-YmfBv-624MKj2sQ',
            "languageId": sign_language_ids["LENSEGUA"],
            'isVideo': True}
 
    # sending post request and saving response as response object
    r = requests.post(url=f'{api_url}/resources/signedUrl', data=data, headers=headers)
    
    # extracting response text
    pastebin_url = r.text
    data = json.loads(pastebin_url)
    print("The pastebin URL is:%s" % data)

    
    # Open the MP4 file and send it to the signed URL
    with open('output.mp4', 'rb') as file:
        response = requests.put(data['signedUrl'], data=file)

    if response.status_code == 200:
        print("File uploaded successfully.")
    else:
        print("Error uploading file. Status code:", response.status_code)

def get_uploaded_video():
    video_id = "653b0856c72e8ab69cc1c20b"
    response = requests.get(f'https://deaflens-xa3v62ac2q-uc.a.run.app/v1/landmark/{sign_language_ids["LENSEGUA"]}/{video_id}_landmark.mp4')

    if response.status_code == 200:
        output_file = 'mediapipe_video.mp4'
        with open(output_file, 'wb') as file:
            file.write(response.content)
        print("File downloaded successfully.")
    else:
        print("Error no existing file. Status code:", response.status_code)


get_cdn_signed_url()
# get_uploaded_video()