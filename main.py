try:
	from requests import post as Post,get as Get
	from pylatexenc.latex2text import LatexNodes2Text as Latex
	from pyperclip import copy as Clipboard
	from iso3166 import countries
except:
	print("Please install requirements before running the code...")
	exit()
from datetime import datetime
from json import dumps as JsonDumps
from threading import Thread
from time import sleep
from re import sub as ReSub
from random import choice
from socket import gethostname,gethostbyname
LatexToText=Latex(keep_comments=True).latex_to_text
class Colors:
	def __init__(self):
		color_code="\033[38;2;{};{};{}m"
		self.white="\033[38;2;255;255;255m"
		self.colors=dict(purple=color_code.format(150,85,255),emrald=color_code.format(0,222,152),blue=color_code.format(50,50,255),lightblue=color_code.format(0,200,255),red=color_code.format(255,35,35),yellow=color_code.format(255,200,10),magenta=color_code.format(218,69,255),slate=color_code.format(96,130,182),grey=color_code.format(113,121,126))
	def Color(self,text,color):
		return f"{self.colors.get(color,self.white)}{text}"+self.white
	def ColoredInput(self,text,output_color,input_color="white"):
		data=input(f"{self.colors.get(output_color,self.white)}{text}{self.colors.get(input_color,self.white)}")
		print(self.white,end="")
		return data
	def ColoredPrint(self,text,color,end="\n"):
		print(self.Color(text,color),end=end)
	def ColoredType(self,text,color,end="\n"):
		print(self.colors.get(color,self.white),end="")
		for i in text:
			print(i,end="",flush=True)
			sleep(0.015)
		print(self.white,end=end)
class Loader:
	def __init__(self,loader):
		self.loader=loader
		self.run=False
	def _worker(self):
		while self.run:
			for i in self.loader:
				if not self.run:
					break
				print(i+(" "*20),end="\r",flush=True)
				sleep(0.065)
	def start(self):
		self.run=True
		Thread(target=self._worker,daemon=True).start()
	def stop(self):
		self.run=False
def realtime_data():
    now=datetime.now()
    formatted_date=now.strftime("%d-%m-%Y")
    day_of_week=now.strftime("%A")
    formatted_time=now.strftime("%H:%M:%S")
    return f"Today is {formatted_date}, {day_of_week} and current time is {formatted_time}."
class HexAI:
	def __init__(self):
		self._set_country()
		try:
			with open("data/api.key") as f:
				self.headers={"Authorization": f"Bearer {f.read().strip()}","Content-Type":"application/json"}
			with open("data/instructions.txt") as f:
				self.instructions=f.read()
		except:
			print("Please run setup API key and instructions before running the code...")
			exit()
		with open("data/logo.txt","rb") as f:
			self.logo=f.read().decode()
		self.chats=[]
		self.max_chats=3
	def _set_country(self):
		IP=gethostbyname(gethostname())
		try:
			with open("data/IP.data","r") as f:
				data=f.read().strip().splitlines()
			with open("data/IP.data","w") as f:
				if len(data)!=2:
					input("making req")
					self.country=countries.get(Get("https://api.country.is/").json()["country"]).name
					f.write(f"{IP}\n{self.country}")
					return
				saved_ip,country=data[0],data[1]
				if saved_ip==IP:
					self.country=country
				else:
					input("making req")
					self.country=countries.get(Get("https://api.country.is/").json()["country"]).name
				f.write(f"{IP}\n{self.country}")
		except:
			print("Please connnect to internet to use the programme...")
			exit()
	def respond(self,q):
		messages=self.chats+[{"role":"user","content":q},{"role":"system","content":f"{self.instructions}\n\nUse this relatime information if required; {realtime_data()}"}]
		payload={"model":"openai/gpt-oss-20b","messages":messages,"temperature":0.7,"max_completion_tokens":512,"include_reasoning":False,"reasoning_effort":"low","tools":[{"type":"browser_search"},{"type":"code_interpreter"}],"search_settings":{"country":self.country,"include_images":True}}
		response=Post("https://api.groq.com/openai/v1/chat/completions",headers=self.headers,data=JsonDumps(payload),timeout=30)
		if response.status_code==401:
			print("Please run setup.py before running the code...")
			exit()
		response.raise_for_status()
		response=response.json()
		content=response["choices"][0]["message"]["content"]
		tools=[i["name"].replace("."," ").capitalize() for i in response["choices"][0]["message"].get("executed_tools",[])]
		self.chats.extend([{"role":"user","content":q},{"role":"assistant","content":content}])
		if len(self.chats)>=self.max_chats*2:
			self.chats=self.chats[2:]
		return dict(response=LatexToText(content),tools=tools,time=round(response["usage"]["total_time"]+response["usage"]["queue_time"],4),tokens=response["usage"]["total_tokens"]+response["usage"]["completion_tokens_details"]["reasoning_tokens"])
class Terminal:
	def __init__(self):
		self.Color=Colors()
		self.AI=HexAI()
		_=self.Color.Color("Hex AI: ","blue")
		self.Load=Loader([_+self.Color.Color(i,"emrald") for i in ["▁▁▁▁▁","▂▁▁▁▁","▃▂▁▁▁","▄▃▂▁▁","▅▄▃▂▁","▆▅▄▃▂","▇▆▅▄▃","█▇▆▅▄","▇█▇▆▅","▆▇█▇▆","▅▆▇█▇","▄▅▆▇█","▃▄▅▆▇","▂▃▄▅▆","▁▂▃▄▅","▁▁▂▃▄","▁▁▁▂▃","▁▁▁▁▂"]])
		self.Commands={"/cls":self.clear_terminal,"/copy":self.copy_resp,"/help":self.help_menu}
	def clear_terminal(self):
		print("\033[H\033[2J\033[3J",end="")
		self.Color.ColoredPrint(self.AI.logo,"purple")
	def copy_resp(self):
		Clipboard(self.AI.chats[-1]["content"])
		self.Color.ColoredPrint("Result was copied to clipboard.","yellow",end="\n\n")
	def help_menu(self):
		self.Color.ColoredPrint("/cls  - ","yellow",end="")
		self.Color.ColoredPrint("Clear the screen.","magenta")
		self.Color.ColoredPrint("/copy - ","yellow",end="")
		self.Color.ColoredPrint("Copy the last response to clipboard.","magenta")
		self.Color.ColoredPrint("/help - ","yellow",end="")
		self.Color.ColoredPrint("Print the help menu.","magenta",end="\n\n")
	def main(self):
		self.clear_terminal()
		while True:
			query=self.Color.ColoredInput("You: ","blue","lightblue").lower()
			clean=ReSub(r"[^a-zA-Z0-9\s]","",query.replace(" ",""))
			if clean=="":
				self.Color.ColoredPrint("Do not waste API calls...","red",end="\n\n")
				continue
			if clean=="exit":
				self.Color.ColoredPrint("Hex AI: ","blue",end="")
				self.Color.ColoredPrint(choice(["Goodbye.","See ya.","Terminated.","Quitting.","Bye."]),"emrald",end="\n\n")
				break
			if query.startswith("/"):
				self.Commands.get(query,lambda:self.Color.ColoredPrint("Invalid command... Type '/help' for more info.","red",end="\n\n"))()
				continue
			self.Load.start()
			response=self.AI.respond(query)
			self.Load.stop()
			sleep(0.3)
			print("\r"+(" "*20),end="\r")
			self.Color.ColoredPrint("Hex AI: ","blue",end="")
			self.Color.ColoredType(response["response"],"emrald",end="\n\n")
			tools=response["tools"]
			if tools:
				self.Color.ColoredPrint("Tools executed: ","slate")
				self.Color.ColoredPrint(", ".join(tools),"grey",end="\n\n")
			self.Color.ColoredPrint("Tokens used: ","slate",end="");self.Color.ColoredPrint(response["tokens"],"grey")
			self.Color.ColoredPrint("Time taken: ","slate",end="");self.Color.ColoredPrint(response["time"],"grey",end="\n\n")
def main():
	Terminal().main()
if __name__=="__main__":
	main()
