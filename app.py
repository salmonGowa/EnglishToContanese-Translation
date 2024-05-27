
from flask import Flask, render_template, request, jsonify
from googletrans import Translator

#importing random to enable the random selection of categories in the exercise
import random

app = Flask(__name__)

# Dictionary of Cantonese words and their English translations
word_dict = {
    '你好': 'Hello',
    '謝謝': 'Thank you',
    '早晨': 'Morning',
    '晚安': 'Good night',
    # Add more words here
}

# Route for the home page
@app.route('/')
def home():
    return render_template('index.html')

# Route for handling the game logic
@app.route('/play', methods=['POST'])
def play():
    # Get a random word from the word_dict
    cantonese_word = random.choice(list(word_dict.keys()))
    english_translation = word_dict[cantonese_word]

    # Render the play template with the word to guess
    return render_template('play.html', cantonese_word=cantonese_word)

# Route for checking the user's guess
@app.route('/check', methods=['POST'])
def check():
    # Get the user's guess from the form
    user_guess = request.form['guess']
    cantonese_word = request.form['cantonese_word']
    english_translation = word_dict[cantonese_word]

    # Check if the user's guess is correct
    if user_guess.lower() == english_translation.lower():
        result = "Correct! Well done!"
    else:
        result = "Incorrect. The correct translation is: {}".format(english_translation)

    # Render the result template
    return render_template('result.html', result=result)

@app.route('/')
def index():
    return render_template('index.html')
#route to handle tanslation
@app.route('/translate', methods=['POST'])
def translate_text():
    text_to_translate = request.form.get('text')
    target_language = 'zh-TW'  # Cantonese language code

    if not text_to_translate:
        return jsonify({'translation': 'Please provide valid input.'})

    translator = Translator()
    try:
        translation = translator.translate(text_to_translate, dest=target_language).text
    except Exception as e:
        print(f"Translation error: {e}")
        translation = "Unable to translate."

    return jsonify({'translation': translation})

if __name__ == '__main__':
    app.run(debug=True)
