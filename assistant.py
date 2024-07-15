import base64
from threading import Lock, thread

import cv2
from cv2 import VideoCapture, imencode
from dotenv import load_dotenv
from langchain.prompts import ChatPromptsTemplate, MessagePlaceholder
from langchain.schema.messages import SystemMessage
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.hostory import RunnableWithMessageHistory
from langchain_google_genai import ChatGoogleGenerativeAI
from openai import audio
from pyaudio import PyAudio, paInt16
from speech_recognition import Microphone, Recognizer, UnknownValueError

load_dotenv()

class WebcamStream:
    def __init__(self):
        self.stream = VideoCapture(index = 0)
        _, self.frame = self.stream.read()
        self.running = False
        self.lock = Lock()
    
    def start(self):
        if self.running:
            return self
        
        self.running = True
        self.thread = Thread(target=self.update, args=())