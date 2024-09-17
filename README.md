---
title: English Quiz project
emoji: 📝
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: "4.44.0"
app_file: app.py
pinned: false
---

# Interactive Quiz Application using Gemini API and Gradio

A quiz application made using Google Gemini with LangChain and Gradio for the interactive frontend. The application will read data from a provided PDF - in the demo, it quizzes on English Grammar concepts. The app then uses Gemini AI to generate quiz questions and answers relating to the contents of the PDF. 

The frontend display is built using Gradio, and updates to show the correct answers and provides generated explanations for each question. The app will provide feedback on correct/incorrect answers instantly, and return a final score once the quiz is finished.

View the live project deployed on [HuggingFace](https://huggingface.co/spaces/zealousmushroom/interactive_english_quiz), or view the [Demo Video](https://youtu.be/mCj5RhkGCkM).

## Local Deployment

To run the app locally, clone this git repo and navigate to the project folder. Once in the correct directory, run the following command to create a Python virtual environment: 

```
python -m venv venv
```

After the virtual environment is created, activate it with: 

```
source venv/bin/activate
```

Or on Windows with:

```
.\venv\scripts\Activate.ps1
```

Install the necessary libraries: 

```
pip install -r requirements.txt
```

After the setup is complete, launch the app by running the following command: 

```
python app.py
```

The Gradio frontend will launch on `localhost:7860` and can be accessed from your browser. 