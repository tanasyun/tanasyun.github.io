from gtts import gTTS

myText = "それってあなたのかんそうですよね"
language ='ja'
output = gTTS(text=myText, lang=language, slow=True)
output.save("output.mp3")