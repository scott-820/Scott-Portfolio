class Magic8:

    ANSWERS = [
        "It is decidedly so.",
        "Don't count on it.",
        "It is certain.",
        "My reply is no.",
        "My sources say no.",
        "Yes, definitely.",
        "Outlook not so good.",
        "You may rely on it.",
        "Very doubtful.",
        "As I see it, yes.",
        "Signs point to yes.",
        "I should hope not.",
        "Most likely.",
        "No - and don't take any wooden Bitcoin.",
        "Outlook is promising.",
    ]

    def __init__(self):
        pass

    def getAnswer(self):
        from random import randint
        n = randint(0,len(Magic8.ANSWERS)-1)
        return Magic8.ANSWERS[n]

    def speakAnswer(self, answer):      # Don't use this method if executing in Codespaces
        import pyttsx3                  # Works fine in stand-alone VS Code on Windows
        engine = pyttsx3.init()
        engine.say(f"The Magic 8 Oracle says:")
        engine.runAndWait()
        engine.say(answer)
        engine.runAndWait()


def main():
    question = input('Ask your "yes/no" question: ')
    m8 = Magic8()
    ans = m8.getAnswer()
    print(f'\nThe Magic8 Oracle says: "{ans}"\n')
    #m8.speakAnswer(ans)                # Doesn't seem to work in Codespaces...

if __name__ == "__main__":
    main()
