import pyttsx3


def speak(text: str) -> None:

    if not text or not text.strip():
        return


    engine = pyttsx3.init()


    try:

        engine.setProperty(
            "rate",
            175,
        )

        engine.setProperty(
            "volume",
            1.0,
        )


        engine.say(
            text
        )


        engine.runAndWait()


    finally:

        engine.stop()