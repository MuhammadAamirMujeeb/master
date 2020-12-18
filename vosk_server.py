from logging import root
import tkinter as tk
import threading
import pyaudio
import wave
import asyncio
import websockets
import sys
from pyaudio import PyAudio, Stream, paInt16
from contextlib import asynccontextmanager, contextmanager, AsyncExitStack
from typing import AsyncGenerator, Generator
import json

@contextmanager
def _pyaudio() -> Generator[PyAudio, None, None]:
    p = PyAudio()
    try:
        yield p
    finally:
        print('Terminating PyAudio object')
        p.terminate()

@contextmanager
def _pyaudio_open_stream(p: PyAudio, *args, **kwargs) -> Generator[Stream, None, None]:
    s = p.open(*args, **kwargs)
    try:
        yield s
    finally:
        print('Closing PyAudio Stream')
        s.close()

@asynccontextmanager
async def _polite_websocket(ws: websockets.WebSocketClientProtocol) -> AsyncGenerator[websockets.WebSocketClientProtocol, None]:
    try:
        yield ws
    finally:
        print('Terminating connection')
        await ws.send('{"eof" : 1}')
        print(await ws.recv())


async def hello(uri):
    async with AsyncExitStack() as stack:
        ws = await stack.enter_async_context(websockets.connect(uri))
        print(f'Connected to {uri}')
        print('Type Ctrl-C to exit')
        ws = await stack.enter_async_context(_polite_websocket(ws))
        p = stack.enter_context(_pyaudio())
        s = stack.enter_context(_pyaudio_open_stream(p,
            format = paInt16, 
            channels = 1,
            rate = 8000,
            input = True, 
            frames_per_buffer = 8000))
        while True:
            data = s.read(8000)
            if len(data) == 0:
                break
            await ws.send(data)
            response = json.loads(await ws.recv())
            
            if 'partial' in response:
                App.message = response['partial']
            elif 'text' in response:
                App.message = response['text']
            print(App.message)

class App():
    chunk = 1024 
    sample_format = pyaudio.paInt16 
    channels = 2
    fs = 44100
    message = ""  
    
    frames = []  
    def __init__(self, master):
        self.isrecording = False
        self.button1 = tk.Button(main, text='record',command=self.startrecording)
        self.button2 = tk.Button(main, text='stop',command=self.stoprecording)
        self.text_window = tk.Label(main, text=App.message)
      
        self.button1.pack()
        self.button2.pack()
        self.text_window.pack()

    def startrecording(self):
        try:
            server = 'localhost:2700'
            loop = asyncio.get_event_loop()
            loop.run_until_complete(
                hello(f'ws://' + server))
        except (Exception, KeyboardInterrupt) as e:
            loop.stop()
            loop.run_until_complete(
                loop.shutdown_asyncgens())
            if isinstance(e, KeyboardInterrupt):
                print('Bye')
                exit(0)
            else:
                print(f'Oops! {e}')
                exit(1)

    def stoprecording(self):
        self.isrecording = False
        print('recording complete')
        self.filename=input('the filename?')
        self.filename = self.filename+".wav"
        wf = wave.open(self.filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.p.get_sample_size(self.sample_format))
        wf.setframerate(self.fs)
        wf.writeframes(b''.join(self.frames))
        wf.close()
        main.destroy()
    def record(self):
       
        while self.isrecording:
            data = self.stream.read(self.chunk)
            self.frames.append(data)
		

main = tk.Tk()
main.title('recorder')
main.geometry('200x200')
app = App(main)
main.mainloop()
