# QA Bot

Table of Contents
===

[TOC]

Startup
===

All source code can be found on [GitHub](https://github.com/shihxuancheng/qa_bot)

1. Use [back_end/run.py](https://github.com/shihxuancheng/qa_bot/blob/master/back_end/run.py) to launch backend app
2. [front_end/detect_intnt.py](https://github.com/shihxuancheng/qa_bot/blob/master/front_end/detect_intent_texts.py) is a demo code demostrate that how to detect intents by  python api 


Intent-Based NLU
===
### Google Dialogflow
[![image alt](https://miro.medium.com/max/1838/1*ZtwmXH1dvBKeYQj3M8kErw.png)](https://dialogflow.com/)

#### Example of Restful API for Fulfillment

==Request==
```json
    POST body:
    {
      "responseId": "ea3d77e8-ae27-41a4-9e1d-174bd461b68c",
      "session": "projects/your-agents-project-id/agent/sessions/88d13aa8-2999-4f71-b233-39cbf3a824a0",
      "queryResult": {
        "queryText": "user's original query to your agent",
        "parameters": {
          "param": "param value"
        },
        "allRequiredParamsPresent": true,
        "fulfillmentText": "Text defined in Dialogflow's console for the intent that was matched",
        "fulfillmentMessages": [
          {
            "text": {
              "text": [
                "Text defined in Dialogflow's console for the intent that was matched"
              ]
            }
          }
        ],
        "outputContexts": [
          {
            "name": "projects/your-agents-project-id/agent/sessions/88d13aa8-2999-4f71-b233-39cbf3a824a0/contexts/generic",
            "lifespanCount": 5,
            "parameters": {
              "param": "param value"
            }
          }
        ],
        "intent": {
          "name": "projects/your-agents-project-id/agent/intents/29bcd7f8-f717-4261-a8fd-2d3e451b8af8",
          "displayName": "Matched Intent Name"
        },
        "intentDetectionConfidence": 1,
        "diagnosticInfo": {},
        "languageCode": "en"
      },
      "originalDetectIntentRequest": {}
    }
```

==Response==
```json
  {
      "fulfillmentText": "This is a text response",
      "fulfillmentMessages": [
        {
          "card": {
            "title": "card title",
            "subtitle": "card text",
            "imageUri": "https://assistant.google.com/static/images/molecule/Molecule-Formation-stop.png",
            "buttons": [
              {
                "text": "button text",
                "postback": "https://assistant.google.com/"
              }
            ]
          }
        }
      ],
      "source": "example.com",
      "payload": {
        "google": {
          "expectUserResponse": true,
          "richResponse": {
            "items": [
              {
                "simpleResponse": {
                  "textToSpeech": "this is a simple response"
                }
              }
            ]
          }
        },
        "facebook": {
          "text": "Hello, Facebook!"
        },
        "slack": {
          "text": "This is a text response for Slack."
        }
      },
      "outputContexts": [
        {
          "name": "projects/${PROJECT_ID}/agent/sessions/${SESSION_ID}/contexts/context name",
          "lifespanCount": 5,
          "parameters": {
            "param": "param value"
          }
        }
      ],
      "followupEventInput": {
        "name": "event name",
        "languageCode": "en-US",
        "parameters": {
          "param": "param value"
        }
      }
    }
```

#### Reference

- [DialogFlow Offical Site](https://dialogflow.com/)
- [DialogFlow client api for Python](https://github.com/shihxuancheng/dialogflow-python-client-v2)
- [DialogFlow v2 rest api reference](https://cloud.google.com/dialogflow/docs/reference/rest/v2-overview)
- [Voice App 開發實務：使用Diagflow+firebase開發Google home App (google assistant action)](https://ithelp.ithome.com.tw/users/20046160/ironman/1808)
---
### Microsoft (bot service + LUIS)
[![image alt](https://2.bp.blogspot.com/-V3CtS3b1HAc/WWzaWvwJzVI/AAAAAAAABUc/0Od0YddweRUVbOt5OyRbd-6AhJJUwGQ1ACLcBGAs/s1600/Title.png)](https://www.luis.ai/home)

### Microsoft QnA Maker

#### Example of Restful API

==Request==
```json
{
    "question": "Is the QnA Maker Service free?",
    "top": 3
}
```

==Response==
```json
{
  "answers": [
    {
      "questions": [
        "How do I embed the QnA Maker service in my website?"
      ],
      "answer": "Follow these steps to embed the QnA Maker service as a web-chat control in your website:\n\n\n1.  Create your FAQ bot by following the instructions [here](https://docs.microsoft.com/azure/cognitive-services/qnamaker/tutorials/create-qna-bot).\n2.  Enable the web chat by following the steps [here](https://docs.microsoft.com/azure/bot-service/bot-service-channel-connect-webchat)",
      "score": 70.95,
      "id": 16,
      "source": "https://docs.microsoft.com/azure/cognitive-services/qnamaker/faqs",
      "metadata": []
    },
    {
      "questions": [
        "Do I need to use Bot Framework in order to use QnA Maker?"
      ],
      "answer": "No, you do not need to use the Bot Framework with QnA Maker. However, QnA Maker is offered as one of several templates in Azure Bot Service. Bot Service enables rapid intelligent bot development through Microsoft Bot Framework, and it runs in a server-less environment.",
      "score": 46.94,
      "id": 14,
      "source": "https://docs.microsoft.com/azure/cognitive-services/qnamaker/faqs",
      "metadata": []
    },
    {
      "questions": [
        "How can I create a bot with QnA Maker?"
      ],
      "answer": "Follow the instructions in [this](https://docs.microsoft.com/azure/cognitive-services/qnamaker/tutorials/create-qna-bot)documentation to create your Bot with Azure Bot Service.",
      "score": 43.25,
      "id": 15,
      "source": "https://docs.microsoft.com/azure/cognitive-services/qnamaker/faqs",
      "metadata": []
    }
  ]
}
```
#### Reference
- [利用 MS Bot framework 與 Cognitive Service 建構自用智慧小秘書 系列](https://ithelp.ithome.com.tw/users/20091494/ironman/1411?page=1)
- [使用 Microsoft Conversational AI Tools - 打造新时代的UI界面 系列](https://ithelp.ithome.com.tw/users/20083151/ironman/2101)
- [Bot Framework SDF for Python](https://github.com/microsoft/botbuilder-python)
- [QnA Maker](https://www.qnamaker.ai/)
- [LUIS](https://www.luis.ai)

Demo
===

## Agent1 - Wanhai_QABot

### qa_bot

[![](https://github.com/shihxuancheng/qa_bot/blob/master/resources/assets/qa_bot_dialogflow.png?raw=true)](https://www.draw.io/?lightbox=1&highlight=0000ff&nav=1&page-id=c7558073-3199-34d8-9f00-42111426c3f3&title=qa_bot%20dialog%20flow.drawio#Uhttps%3A%2F%2Fraw.githubusercontent.com%2Fshihxuancheng%2Fqa_bot%2Fmaster%2Fresources%2Fassets%2Fqa_bot%2520dialog%2520flow.drawio)

## Agen2 - Wanhai_ServiceBot

### system_pic

[![](https://github.com/shihxuancheng/qa_bot/blob/master/resources/assets/system_pic_dialogflow.png?raw=true)](https://www.draw.io/?lightbox=1&target=blank&highlight=0000ff&nav=1&page-id=s6GVqAID3o5IfIvOThLx&title=qa_bot%20dialog%20flow.drawio#Uhttps%3A%2F%2Fraw.githubusercontent.com%2Fshihxuancheng%2Fqa_bot%2Fmaster%2Fresources%2Fassets%2Fqa_bot%2520dialog%2520flow.drawio)

---

### whl_report

[![](https://github.com/shihxuancheng/qa_bot/blob/master/resources/assets/whl_report_dialogflow.png?raw=true)](https://www.draw.io/?lightbox=1&target=blank&highlight=0000ff&nav=1&page-id=ZBpW3UwpYAJFGxqoSjzb&title=qa_bot%20dialog%20flow.drawio#Uhttps%3A%2F%2Fraw.githubusercontent.com%2Fshihxuancheng%2Fqa_bot%2Fmaster%2Fresources%2Fassets%2Fqa_bot%2520dialog%2520flow.drawio)

---

### whl_family

[![](https://github.com/shihxuancheng/qa_bot/blob/master/resources/assets/whl_family_dialogflow.png?raw=true)](https://www.draw.io/?lightbox=1&target=blank&highlight=0000ff&nav=1&page-id=bM1LIQPi1tVLYMAEycQf&title=qa_bot%20dialog%20flow.drawio#Uhttps%3A%2F%2Fraw.githubusercontent.com%2Fshihxuancheng%2Fqa_bot%2Fmaster%2Fresources%2Fassets%2Fqa_bot%2520dialog%2520flow.drawio)

Slide
---
{%slideshare https://www.slideshare.net/RichardShih4/qa-bot %}

###### tags: `AI` `ChatBot` `dialogflow`
test
