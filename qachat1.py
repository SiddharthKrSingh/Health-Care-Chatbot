import streamlit as st
import panel as pn
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])


def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response


class QnAChat(pn.Column):
   

    def __init__(self):
        self.chat_history = []

        self.input_box = pn.widgets.TextInput(name="Input:")
        self.submit_button = pn.widgets.Button(name="SUBMIT")

        self.response_area = pn.Column(name="The Response is")
        self.chat_log = pn.Column(name="The Chat History is")

        self.submit_button.param.watch(self.handle_submit, "clicks")

        super().__init__(
            self.input_box, self.submit_button, self.response_area, self.chat_log
        )

    def handle_submit(self, event):
        if self.input_box.value:
            response = get_gemini_response(self.input_box.value)
            self.chat_history.append(("You", self.input_box.value))

            for chunk in response:
                self.response_area.append(chunk.text)
                self.chat_history.append(("Bot", chunk.text))

            self.input_box.value = ""  

            
            self.chat_log.clear()
            for role, text in self.chat_history:
                self.chat_log.append(f"{role}: {text}")



qa_chat = QnAChat()


pn.serve(qa_chat)
