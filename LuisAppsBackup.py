import requests, json, logging, sys
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

class LUISAPI:
    def __init__(self, endpoint, authoringKey, appSecret, folder):
        self.uri = f"https://{endpoint}"        
        self.authoringKey = authoringKey
        self.appSecret = appSecret
        self.headers = {"Ocp-Apim-Subscription-Key":self.authoringKey}
        self.folder = folder
        
    # export luis app
    def ExportApps(self):
        res = self.Get(f"{self.uri}/luis/api/v2.0/apps")
        res.raise_for_status()
        result = json.dumps(res.json(), indent=4, ensure_ascii=False)
        logging.info("========== LUIS app information ==========",)
        logging.info(result)

        for app in res.json():

            try:
                appId = app["id"] 
                appName = app["name"] 
                activeVersion = app["activeVersion"]
                logging.info(f"export for id:{appId}, name:{appName}")

                res = self.Get(f"{self.uri}/luis/api/v2.0/apps/{appId}/versions/{activeVersion}/export?subscription-key={self.appSecret}")
                res.raise_for_status()
                result = json.dumps(res.json(), indent=4, ensure_ascii=False)

                file = open(f"{self.folder}/{appName}_{activeVersion}.json",'w', encoding='utf-8')
                file.write(result)
                file.close()

                logging.info(f"The {appName} saved in {self.folder}/{appName}_{activeVersion}.json successfully.")
                
            except:
                logging.error("failed!!!")

    def Get(self,uri):
        return requests.get(uri, headers=self.headers)


if __name__ == "__main__":
    
    endpoint = "westus.api.cognitive.microsoft.com" #you can change the region
    authoringKey = "{luis authoring key}"
    appSecret = "{luis app secret}" #you can use starterkey, it has limitation.
    folder = "c:\\temp"

    if len(sys.argv) == 1:
        logging.info(f"Use folder path as {folder}")
    else:
        folder = sys.argv[0]        

    luis = LUISAPI(endpoint, authoringKey, appSecret, folder)

    luis.ExportApps()


