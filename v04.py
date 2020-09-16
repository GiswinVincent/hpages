#changes
#added support for & in company name
import subprocess
import sys
if sys.version.split(' ')[0][0] =="2":
        print ("This program is designed for python 3 not python 2")

def install(package):
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
try:
        import sys
        import requests
        import time
        import re
        import clipboard
        import json
except ImportError:
        print("libraries are missing. Trying to install libraries.")
        print("Wait 2-3 minutes for installation to finish")
        print("This is a one time process\n\n")
        try:
                install("requests")
                install("clipboard")
                print("\n\nlibraries installed\n\n\n")
                #loading libraries
                import sys
                import requests
                import time
                import re
                import clipboard
                import json
        except:
                print("installation of libraaries failed")
                foo = input()


    
def parser(url):
        try:
                r = requests.get(url)
                page_source = r.text
        ####        print(url)
                return_string = ""
                try:
                    email = re.findall(r'\\\"email\\\":\\\"([\w@\.]+)',page_source)[0]
                except:
                    email=" "
                try:
                    contact = re.findall(r'\\\"contact_name\\\":\\\"([\w@\.\s]+)',page_source)[0]
                except:
                    contact=" "
                try:
                    first_name= contact.split(" ")[0]
                except:
                    first_name=" "
                try:
                    last_name= contact.split(" ")[-1]
                except:
                    last_name=" "
                try:
                    mobile = re.findall(r'\\\"mobile\\\":\\\"([\d\s]+)',page_source)[0]
                except:
                    mobile=" "
                try:
                        if len(mobile)>7 and mobile[0] == "0" and " " not in mobile : #if leading digit is 0
                                mobile=mobile[:4]+" "+mobile[4:7]+" "+mobile[7:]
                except:
                        pass
                try:
                    company_name=re.findall(r'\\\"name\\\":\\\"([&\w\.\s]+)\\\",\\\"address',page_source)[0]
                except:
                    company_name=" "
                try:
                    suburb=re.findall(r'\\\"suburb\\\":\\\"([\w\.\s]+)\\\",\\\"state',page_source)[0]
                except:
                    suburb=" "
                try:
                    postcode=re.findall(r'\\\"zip\\\":([\d]+),\\\"country',page_source)[0]
                except:
                    postcode=" "
                try:
                    state = re.findall(r'\\\"state_code\\\":\\\"([\w\.\s]+)\\\",\\\"zip',page_source)[0]
                except:
                    state=" "
                try:
                    website=re.findall(r'\\\"website\\\":\\\"([\w\.\s]+)\\\",\\\"primary_category',page_source)[0]
                except:
                    website=" "
                try:
                    email_domain=email.split("@",1)[1]
                except:
                    email_domain=""

                return_string = first_name+"\t"+last_name+"\t"+company_name+"\t"+suburb+"\t"+postcode+"\t"+state+"\t"+mobile+"\t"+email+"\t"+website+"\t"+url+"\t\t\t"+email_domain
        ##        print(return_string)
                time.sleep(.1)
                return return_string
        except:
                return

##main_link ="https://hipages.com.au/search/builders/sa/lawson"
##main_link ="https://hipages.com.au/find/builders/nsw/sydenham"
##main_link ="https://hipages.com.au/search/builders/vic/bittern"
##main_link ="https://hipages.com.au/find/builders/sa/port_kenny"
##main_link ="https://hipages.com.au/search/builders/sa/west_hindmarsh"
while True: #main loop
    while True:
        try:
            main_link=input("enter link: ")
            ##for debug ; enter 1,2 or 3 for a valid link
            if main_link == '1':
                main_link = "https://hipages.com.au/search/builders/vic/bittern"
            if main_link == '2':
                main_link = "https://hipages.com.au/find/builders/nsw/sydenham"
            if main_link == '3':
                main_link ="https://hipages.com.au/find/builders/sa/port_kenny"
                
            ##find state and suburb name form entered link
            searching_state = re.search(r"hipages.com.au\/(search|find)\/builders/([\s\S]+)\/([\s\S]+)",main_link).group(2)
            searching_suburb = re.search(r"hipages.com.au\/(search|find)\/builders/([\s\S]+)\/([\s\S]+)",main_link).group(3)
        except:
            print("link invalid, only hipages supported. recheck link \nfor eg:https://hipages.com.au/find/builders/nsw/sydenham, hipages.com.au/find/builders/sa/port_kenny\n")
        else:
            break
        
    ##generate main_link from parsed data
    main_link = "https://hipages.com.au/find/builders/{}/{}".format(searching_state,searching_suburb)
    ##print(main_link)



    r = requests.get(main_link)
    page_source = r.text  

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    ajax_code = re.search(r'\"code\":\"([\w\d]+)\",\"practiceId\":5',page_source).group(1)

    #Post to AJAX
    #https://hipages.com.au/api/directory/sites?suburb=sydenham&state=nsw&category=5&page=5&perpage=10&code=0e88ebf65712115b547bbd89bbbdf9578a8382ef7c4489f5a1dbf7b5fd74b3aed5ff143bbaf5c629d7918161ad15bc10
    page_number=1
    site_key_list = []
    repeat_count = 0
    while True:
        try:
            response = requests.get(
                "https://hipages.com.au/api/directory/sites",
                params={
                    "suburb": searching_suburb,
                    "state": searching_state,
                    "category": 5,
                    "page": page_number,
                    "perpage":10,
                    "code": ajax_code   # eg:"0e88ebf65712115b547bbd89bbbdf9578a8382ef7c4489f5a1dbf7b5fd74b3aed5ff143bbaf5c629d7918161ad15bc10"
                }
            , headers=headers)
            page_number += 1
            if len(json.loads(response.content))==0: #check if empty
                break
            for json_entry in json.loads(response.content):
                site_key = json_entry["siteKey"]
                if site_key in site_key_list:
                    repeat_count +=1
                else:
                    site_key_list.append(site_key)
            if page_number >100 or repeat_count >2:
                break
        except:
            print("Unexpected error occured")
    print("{} possible links found".format(len(site_key_list)))
    print("please wait. We are trying to open these links. It may take up to 2 minutes")
    ##print(site_key_list) # print list of all site keys

    main_list=[]
##    print("loading",end="")
    for site_key in site_key_list:
            try:
                    main_list.append(parser("https://hipages.com.au/connect/{}".format(site_key)))
##                    print(".",end="")
            except:
                    pass
    ##        print("error in {}".format(site_key))
            
    clipboard.copy('\n'.join(map(str, main_list)))
    print("\ndata copied to clipboard")
    #menu
    while True:
        try:
            print("\nEnter 1 to search with new link")
            print("Enter 2 to copy again to clipboard")
            print("Enter 3 to exit")
            user_selection=input("Selection:")
            if user_selection == "1":
                break
            elif user_selection == "2":
                clipboard.copy('\n'.join(map(str, main_list)))
                print("data copied to clipboard")
            elif user_selection == "3":
                print("exitting")
                sys.exit()
            else:
                print("invalid entry, try again")
        except:
            if user_selection == "3":
                    sys.exit()    
            print("invalid entry, try again")
