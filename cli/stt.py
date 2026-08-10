import os
import queue
import threading

import sounddevice as sd
from dotenv import load_dotenv
from deepgram import DeepgramClient
from deepgram.core.events import EventType


load_dotenv()


# ==================================================
# Audio configuration
# ==================================================

SAMPLE_RATE = 16000
CHANNELS = 1

# 100 ms of audio at 16 kHz.
BLOCK_SIZE = 1600

# Your microphone was slightly quiet.
GAIN = 1.8


# ==================================================
# Speech-to-Text
# ==================================================

class SpeechToText:

    def __init__(self):

        self.api_key = os.getenv(
            "DEEPGRAM_API_KEY"
        )

        if not self.api_key:

            raise RuntimeError(
                "DEEPGRAM_API_KEY is not configured."
            )


        self.audio_queue = queue.Queue()

        self.stop_event = (
            threading.Event()
        )

        self.final_parts = []

        self.interim_text = ""


    # ==================================================
    # Microphone callback
    # ==================================================

    def _audio_callback(
        self,
        indata,
        frames,
        time,
        status,
    ):

        if status:

            print(
                f"\nAudio status: {status}"
            )


        # Convert to float so gain can
        # be applied safely.

        audio = indata.astype(
            "float32"
        )


        # Increase microphone volume.

        audio *= GAIN


        # Prevent clipping.

        audio = audio.clip(
            -32768,
            32767,
        )


        # Convert to 16-bit PCM.

        audio = audio.astype(
            "int16"
        )


        # Put PCM bytes into queue.

        self.audio_queue.put(
            audio.tobytes()
        )


    # ==================================================
    # Send audio to Deepgram
    # ==================================================

    def _send_audio(
        self,
        connection,
    ):

        print(
            "\nAudio streaming started."
        )


        while not self.stop_event.is_set():

            try:

                audio = (
                    self.audio_queue.get(
                        timeout=0.1
                    )
                )


                if not audio:

                    continue


                connection.send_media(
                    audio
                )


            except queue.Empty:

                continue


            except Exception as error:

                print(
                    f"\nAudio streaming error: {error}"
                )

                break


    # ==================================================
    # Receive Deepgram messages
    # ==================================================

    def _handle_message(
        self,
        message,
    ):

        if message.type != "Results":

            return


        alternatives = (
            message.channel.alternatives
        )


        if not alternatives:

            return


        transcript = (
            alternatives[0].transcript
        )


        if not transcript:

            return


        # ------------------------------------------
        # Final result
        # ------------------------------------------

        if message.is_final:

            self.final_parts.append(
                transcript
            )

            self.interim_text = ""


        # ------------------------------------------
        # Interim result
        # ------------------------------------------

        else:

            self.interim_text = (
                transcript
            )


        self._display_transcript()


    # ==================================================
    # Display live transcript
    # ==================================================

    def _display_transcript(self):

        final_text = " ".join(
            self.final_parts
        )


        if self.interim_text:

            display = (
                final_text
                + " "
                + self.interim_text
            )

        else:

            display = final_text


        print(
            f"\rYou: {display}",
            end="",
            flush=True,
        )


    # ==================================================
    # Deepgram error handler
    # ==================================================

    def _handle_error(
        self,
        error,
    ):

        print()

        print(
            f"❌ Deepgram error: {error}"
        )


    # ==================================================
    # Deepgram event listener
    # ==================================================

    def _listen_for_events(
        self,
        connection,
    ):

        try:

            connection.start_listening()

        except Exception as error:

            print(
                f"\nDeepgram listener error: {error}"
            )


    # ==================================================
    # Transcribe microphone
    # ==================================================

    def transcribe(self):

        # Reset state.

        self.stop_event.clear()

        self.final_parts = []

        self.interim_text = ""


        print()

        print(
            "🎤 Listening..."
        )

        print(
            "Press ENTER to stop."
        )


        # ------------------------------------------
        # Create Deepgram client
        # ------------------------------------------

        client = DeepgramClient(
            api_key=self.api_key
        )


        # ------------------------------------------
        # Open Deepgram connection
        # ------------------------------------------

        with client.listen.v1.connect(

            model="nova-3",

            language="en-IN",

            encoding="linear16",

            sample_rate=SAMPLE_RATE,

            channels=CHANNELS,

            interim_results=True,

            smart_format=True,

            endpointing=300,

        ) as connection:


            # --------------------------------------
            # Register Deepgram events
            # --------------------------------------

            connection.on(
                EventType.MESSAGE,
                self._handle_message,
            )


            connection.on(
                EventType.ERROR,
                self._handle_error,
            )


            # --------------------------------------
            # IMPORTANT
            #
            # start_listening() is blocking.
            #
            # Therefore it MUST run in its
            # own thread.
            # --------------------------------------

            listener_thread = threading.Thread(

                target=self._listen_for_events,

                args=(connection,),

                daemon=True,
            )


            listener_thread.start()


            # --------------------------------------
            # Give the listener a moment to start.
            # --------------------------------------

            listener_thread.join(
                timeout=0.05
            )


            # --------------------------------------
            # Start audio → Deepgram thread
            # --------------------------------------

            audio_thread = threading.Thread(

                target=self._send_audio,

                args=(connection,),

                daemon=True,
            )


            audio_thread.start()


            try:

                # ----------------------------------
                # Open microphone
                # ----------------------------------

                with sd.InputStream(

                    samplerate=SAMPLE_RATE,

                    channels=CHANNELS,

                    dtype="int16",

                    blocksize=BLOCK_SIZE,

                    callback=self._audio_callback,

                ):

                    # ------------------------------
                    # Wait for user to press ENTER
                    # ------------------------------

                    input()


            finally:

                print(
                    "\nStopping..."
                )


                # ----------------------------------
                # Stop audio thread
                # ----------------------------------

                self.stop_event.set()


                audio_thread.join(
                    timeout=1
                )


                # ----------------------------------
                # Tell Deepgram the audio is done
                # ----------------------------------

                try:

                    connection.send_finalize()

                except Exception as error:

                    print(
                        f"Finalize error: {error}"
                    )


                # ----------------------------------
                # Wait briefly for final result
                # ----------------------------------

                listener_thread.join(
                    timeout=1
                )


        # ==================================================
        # Build final transcript
        # ==================================================

        final_text = " ".join(
            self.final_parts
        ).strip()


        print()

        print(
            f"Final: {final_text}"
        )


        return final_text


# ==================================================
# Standalone STT test
# ==================================================

if __name__ == "__main__":

    stt = SpeechToText()


    try:

        text = stt.transcribe()


        print()

        print(
            f"Final transcript: {text}"
        )


    except KeyboardInterrupt:

        print()

        print(
            "Stopped."
        )


    except Exception as error:

        print()

        print(
            f"❌ STT error: {error}"
        )