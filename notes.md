# Development Notes

## Resources
- [Markdown Syntax](https://www.markdownguide.org/basic-syntax/)
- [MongoDB in Pythong](https://www.mongodb.com/resources/languages/python)
- [Retrieval Augmented Generation Article](https://scalexi.medium.com/implementing-a-retrieval-augmented-generation-rag-system-with-openais-api-using-langchain-ab39b60b4d9f)
- [How to uoload to Google Cloud](https://stackoverflow.com/questions/37003862/how-to-upload-a-file-to-google-cloud-storage-on-python-3)
- [Using embeddings to help search](https://cookbook.openai.com/examples/question_answering_using_embeddings)
- [Ideas for the app builder](https://zapier.com/blog/best-no-code-app-builder/#bubble)
---
## Thoughts / Ideas
- Need to figure out way to store the session history and then use it for future responses.
- Also will need to have a file which contains key information about the user:
  - Biographical info (name, nickname, family and status)
  - Hobbies and Interests
  - Location and current situation
- Ability for caretaker to send notes/alerts
- Ability for caretaker to share stuatus
- Ability for caretaker to see history in raw and synthesized manner
  - This could also give an update for the day.
- Have form factor be a picture frame or seomthing like that.
- Need to have Google Cloud as endpoint to store information
- Need to look at easy to build mobile app development tools
- Should we convert the responses to vectors to make it easier to ingest

---
## TODOs
- Incorporate MongoDB to store the chat history. 
- Review concept of RAG with the system
- Store chat history so it can be remembered in perpetuity
- Think about way to compress chat history
- Look more at the personal history file
- Create AWS function and folder to emulate cloud storage
- More modularization and configuration should all be in config files
- Think about outlining system architecture