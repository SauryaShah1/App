from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from quiz_data import quiz_data
import random

class QuizApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.max_questions_per_round = 5
        self.current_question = 0
        self.score = 0
        self.quiz_data = []
        self.selected_questions = []
        self.generate_questions()

    def generate_questions(self):
        self.quiz_data = random.sample(quiz_data, self.max_questions_per_round)
        self.selected_questions = self.quiz_data.copy()

    def build(self):
        self.layout = BoxLayout(orientation='vertical')
        self.show_question()
        return self.layout

    def show_question(self):
        if self.current_question < len(self.selected_questions):
            question = self.selected_questions[self.current_question]
            self.layout.clear_widgets()
            question_label = Label(text=question["question"], size_hint=(1, 0.3))
            self.layout.add_widget(question_label)

            choices_layout = GridLayout(cols=2, size_hint=(1, 0.5))
            for i, choice in enumerate(question["choices"]):
                button = Button(text=choice, size_hint=(0.5, None), height=100)
                button.bind(on_press=self.check_answer)
                choices_layout.add_widget(button)
            self.layout.add_widget(choices_layout)

            self.feedback_label = Label(text="", size_hint=(1, 0.1))
            self.layout.add_widget(self.feedback_label)
        else:
            self.show_result()

    def check_answer(self, instance):
        question = self.selected_questions[self.current_question]
        selected_choice = instance.text

        if selected_choice == question["answer"]:
            self.score += 1
            self.feedback_label.text = "Correct!"
        else:
            self.feedback_label.text = "Incorrect!"

        self.current_question += 1
        if self.current_question < len(self.selected_questions):
            self.show_question()
        else:
            self.show_result()

    def show_result(self):
        popup_content = BoxLayout(orientation='vertical')
        popup_content.add_widget(Label(text=f"Final Score: {self.score}/{len(self.selected_questions)}"))
        popup = Popup(title='Quiz Completed', content=popup_content, size_hint=(0.5, 0.5))
        retry_button = Button(text='Retry', size_hint=(0.5, None), height=100)
        retry_button.bind(on_press=self.retry_quiz)
        popup_content.add_widget(retry_button)
        popup.open()

    def retry_quiz(self, instance):
        self.current_question = 0
        self.score = 0
        self.generate_questions()
        self.show_question()


if __name__ == '__main__':
    QuizApp().run()
