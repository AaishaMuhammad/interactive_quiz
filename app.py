import gradio as gr
from main import start_quiz, submit_answer

# Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("### Quiz Application")
    gr.Markdown("Take an interactive quiz on English grammar concepts. There are 7 multiple-choice answers in total.")

    num_questions = gr.State(7)
    start_btn = gr.Button("Start Quiz")

    question_state = gr.State("")
    options_state = gr.State(["Option A", "Option B", "Option C", "Option D"])
    correct_answer_state = gr.State("")
    correct_option_state = gr.State("")
    explanation_state = gr.State("")
    score_state = gr.State(0)
    count_state = gr.State(0)
    total_questions_state = gr.State(7)
    book_content_state = gr.State("")
    index_state = gr.State(None)
    vectorizer_state = gr.State(None)
    text_chunks_state = gr.State(None)
    used_indices_state = gr.State([])

    question_label = gr.Label()
    answer_radio = gr.Radio(choices=[], label="Select an answer")
    submit_btn = gr.Button("Submit")
    result_label = gr.Label()
    explanation_label = gr.Label()
    final_grade_label = gr.Label()
    score_label = gr.Label(label="Score: 0")
    
    # Allow the radio buttons of the answers to be shown from the first question onwards
    start_btn.click(lambda q, o: (gr.update(value=q), gr.update(choices=o)),
                inputs=[question_label, options_state], outputs=[question_label, answer_radio])
    

    start_btn.click(
    start_quiz,
    inputs=[],
    outputs=[
        book_content_state,
        question_label,
        answer_radio,  
        correct_answer_state,
        correct_option_state,
        explanation_state,
        score_state,
        count_state,
        result_label,
        final_grade_label,
        options_state,  
        index_state,
        vectorizer_state,
        text_chunks_state,
        used_indices_state,
        total_questions_state,
        score_label
    ]
)
    
    submit_btn.click(
    submit_answer,
    inputs=[
        answer_radio,
        correct_answer_state,
        correct_option_state,
        explanation_state,
        score_state,
        count_state,
        index_state,
        vectorizer_state,
        text_chunks_state,
        used_indices_state,
        total_questions_state
    ],
    outputs=[
        question_label,
        answer_radio,
        correct_answer_state,
        correct_option_state,
        explanation_state,
        result_label,
        explanation_label,
        score_state,
        count_state,
        final_grade_label,
        options_state,  
        index_state,
        vectorizer_state,
        text_chunks_state,
        used_indices_state,
        total_questions_state,
        score_label
    ]
)
    submit_btn.click(lambda q, o: (gr.update(value=q), gr.update(choices=o)), inputs=[question_label, options_state], outputs=[question_label, answer_radio])

    
    demo.launch(share=True)