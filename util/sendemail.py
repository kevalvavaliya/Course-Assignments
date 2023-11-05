import requests
import json
import os

class Email:

    @classmethod
    def sendEmailToAllStudents(cls,student_list,assignment,teacherName):
        emailList = []
        recipentVar={}
        for s in student_list:
            emailList.append(s.email)
            recipentVar[s.email]={"name":s.name}

        # print(json.dumps(recipentVar))
        return requests.post(
        f"https://api.mailgun.net/v3/{os.getenv('MAILGUN_DOMAIN')}/messages",
        auth=("api", os.getenv("MAILGUN_API_KEY")),
        data={"from": "keval@info.bauddhikgeeks.tech",
              "to": emailList,
              "subject": f"New Assignment {assignment.title} has been Assigned",
              "text": f" Hello %recipient.name% you have got assignment from {teacherName} \n\n Description of assignment :{assignment.desc} \n\n Thanks",
              "recipient-variables": json.dumps(recipentVar)
              })
