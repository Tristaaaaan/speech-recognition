from kivy.app import App
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
import pyttsx3
import openai
import speech_recognition as sr

# Set up pyttsx3 text-to-speech engine
engine = pyttsx3.init()

# Configure OpenAI API
openai.api_key = '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'


class MetisApp(App):
    def ask_question(self, button):
        question = self.question_entry.text.strip()

        # Send the user's question to ChatGPT
        response = openai.Completion.create(
            engine='text-davinci-003',
            prompt="give the following question in the style of a quiz answer using as few words as possible " + question,
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.7
        )

        # Get the generated response
        answer = response.choices[0].text.strip()

        # Output the response in the text box
        self.answer_text.text = answer

        # Read the response out loud
        engine.say(answer)
        engine.runAndWait()

    def record_question(self, button):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            audio = r.listen(source)

        try:
            # Convert speech to text
            question = r.recognize_google(audio)
            self.question_entry.text = question
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand your speech.")
        except sr.RequestError as e:
            print("Sorry, an error occurred while processing your request: ", str(e))
        self.ask_question(None)

    def build(self):
        # Create GUI layout
        layout = BoxLayout(orientation='vertical', spacing=10)

        # Create label for Metis
        question_label = Label(text="Metis 0.1", font_size=20)
        layout.add_widget(question_label)

        # Create text entry for user's question
        self.question_entry = TextInput(height=100, size_hint_y=None)
        layout.add_widget(self.question_entry)

        # Create text box for response
        self.answer_text = TextInput(height=100, size_hint_y=None, readonly=True)
        layout.add_widget(self.answer_text)

        # Create button to ask question
        record_button = Button(text="Ask", on_release=self.record_question)
        layout.add_widget(record_button)

        # Create scroll view
        scroll_view = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
        scroll_view.add_widget(layout)

        return scroll_view


# Run the app
if __name__ == '__main__':
    MetisApp().run()