from subprocess import run
run("pip install -r data/requirements.txt")
inst="Your are HEX, {name}'s personal AI assistant. Be calm,gentle,informative and friendly. Answer precisely and directly. Stay on the main topic only. Do not ask questions, just proide straightforward answer in plain text. STRICTLY - No use of any kind of formatting, latex text, respond only in plain text."
with open("data/api.key","w") as f:
	f.write(input("Enter your groq API key: "))
with open("data/instructions.txt","w") as f:
	f.write(inst.format(name=input("Enter your name: ")))
