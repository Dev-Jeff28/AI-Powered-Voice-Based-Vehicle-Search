from api import send_message
from stt import SpeechToText
from tts import speak


def main():

    print()
    print("=" * 55)
    print("              🚗 VEHICLE ASSISTANT")
    print("=" * 55)
    print()


    # ------------------------------------------
    # Conversation session
    # ------------------------------------------

    session_id = None


    # ------------------------------------------
    # Speech-to-Text
    # ------------------------------------------

    stt = SpeechToText()


    # ------------------------------------------
    # Conversation loop
    # ------------------------------------------

    while True:

        print()
        print(
            "Press ENTER to speak."
        )

        print(
            "Type 'q' + ENTER to quit."
        )


        command = input()


        # --------------------------------------
        # Quit
        # --------------------------------------

        if command.lower() in {
            "q",
            "quit",
            "exit",
        }:

            print()
            print(
                "Goodbye!"
            )

            break


        # --------------------------------------
        # Speech → Text
        # --------------------------------------

        try:

            user_text = (
                stt.transcribe()
            )

        except KeyboardInterrupt:

            print()
            print(
                "Stopped."
            )

            break


        except Exception as error:

            print()
            print(
                f"❌ STT error: {error}"
            )

            continue


        # --------------------------------------
        # No speech
        # --------------------------------------

        if not user_text:

            print()
            print(
                "No speech detected."
            )

            continue


        print()
        print(
            f"You: {user_text}"
        )


        # --------------------------------------
        # Text → Backend
        # --------------------------------------

        print()
        print(
            "🤖 Thinking..."
        )


        try:

            response = send_message(

                query=user_text,

                session_id=session_id,

            )


        except Exception as error:

            print()
            print(
                f"❌ Backend error: {error}"
            )

            continue


        # --------------------------------------
        # Validate backend response
        # --------------------------------------

        if not isinstance(
            response,
            dict,
        ):

            print()
            print(
                "❌ Invalid backend response."
            )

            continue


        if "session_id" not in response:

            print()
            print(
                "❌ Backend response is missing "
                "session_id."
            )

            continue


        if "assistant_response" not in response:

            print()
            print(
                "❌ Backend response is missing "
                "assistant_response."
            )

            continue


        # --------------------------------------
        # Update conversation session
        # --------------------------------------

        session_id = (
            response["session_id"]
        )


        # --------------------------------------
        # Assistant response
        # --------------------------------------

        assistant_text = (
            response["assistant_response"]
        )


        print()
        print(
            f"Assistant: {assistant_text}"
        )


        # --------------------------------------
        # Text → Speech
        # --------------------------------------

        try:

            print()
            print(
                "🔊 Speaking..."
            )


            speak(
                assistant_text
            )


            print(
                "✓ Finished speaking."
            )


        except Exception as error:

            print()
            print(
                f"❌ TTS error: {error}"
            )


# ------------------------------------------
# Entry point
# ------------------------------------------

if __name__ == "__main__":

    main()