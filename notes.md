# Development Notes
## Roadmap

1. ~~**Data Structure** | Ensure that exchanges and conversations are being properly recorded and updated.~~
   2. *I think this is complete for now.*
3. ~~**Support FAQ integration** | Support the integration of FAQs into questions.~~
3. **Messaging** | Finalize caretaker -> patient messaging on the device.
4. **Messaging** | Create patient -> caretaker messaging.
5. **Talking Icon** | Create screen icon to alert when the device is listening or speaking.
6. **Calendar** | Add in ability to have user specific calendar. Build out with potential integration to Google Calendar.
5. **Hueristic Layer** | Add hueristic layer to support specific requests.
   6. *Calendar reminders* | Create alerts if there is a calendar reminder coming up.
   7. *Clear Handover* | Add message to user when handing over to Chat GPT
   8. *More structure* | Adjust Chat GPT response so that it is very precise and limit hallucinations.
   9. *Graphics* | Create grpahical analysis of sentiment and performance for the conversation usage tab

## Backlog 
- **Screen Integration** | Create more ability to use the devices screen.
- **Update triggers** | Adjust triggers so that you can say Judy and the command in one sentence. Also want to see if there's a way to keep the conversation going back and forth.
---
## Thoughts / Ideas
- **Device**
  - Periodically check in on the user and ask how they are feeling.
  - Check for activity and prompt user to do something.
  - Have screen and show images when not in use.
  - Integrate even more detail about user and interests into the prompt to ChatGPT.
  - Examine accuracy of different models of ChatGPT.
  - Integrate multiple layers for the query:
    - 1.) Check to see if there is an action to be taken.
    - 2.) See if there is a specific question being asked about current events. (Could tie into pushing information about interests.)
    - 3.) Then default to the device standard informed by bio information.
- **Cloud**
  - Go through the exchanges and group into conversations
  - Create a sentiment (1 - Bad, 5 - Good) for each conversation and create a summary.
  - Pull information from interests and share with user (also could be in device)
- **Application**
  - Ability for caretaker to send notes/alerts
  - Ability for caretaker to share status
  - Caretaker can see summary of conversations and activity
  - Integration with Google Maps API to provide an obfuscated location
  - Allow upload of images to the device.
  - Provide general update for the day on how the user is doing.
- **Unsorted**
  - Need to look at easy to build mobile app development tools
  - Should we convert the responses to vectors to make it easier to ingest
  - Should run two queries against GPT. The first should be to look through the query and see if there are specific actions to be taken. This can be done by adding a list of commands and asking if any of them fit that pattern.
  - Per article, does it make more sense to send things in YAML vs JASON or text?
---
## Resources
- [Markdown Syntax](https://www.markdownguide.org/basic-syntax/)
- [MongoDB in Pythong](https://www.mongodb.com/resources/languages/python)
- [Retrieval Augmented Generation Article](https://scalexi.medium.com/implementing-a-retrieval-augmented-generation-rag-system-with-openais-api-using-langchain-ab39b60b4d9f)
- [How to uoload to Google Cloud](https://stackoverflow.com/questions/37003862/how-to-upload-a-file-to-google-cloud-storage-on-python-3)
- [Using embeddings to help search](https://cookbook.openai.com/examples/question_answering_using_embeddings)
- [Ideas for the app builder](https://zapier.com/blog/best-no-code-app-builder/#bubble)
- [Venture Beat AI Article](https://venturebeat.com/ai/from-gen-ai-1-5-to-2-0-moving-from-rag-to-agent-systems/)