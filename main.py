import os
import random
import json
from dotenv import load_dotenv

import faiss
import numpy as np

from PyPDF2 import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer

from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI


load_dotenv()
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest",
                             generation_config={"response_mime_type": "application/json"})


def text_to_chunks(pdf_path, chunk_size=100): 
    text = ""
    reader = PdfReader(pdf_path)
    for page in reader.pages:
        text += page.extract_text() if page.extract_text() else ''

    text_chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    return text_chunks

def index_chunks(chunks): 
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(chunks).toarray()
    index = faiss.IndexFlatL2(vectors.shape[1])
    index.add(vectors)
    return index, vectorizer

def query_chunks(index, vectorizer, query, k=5): 

    query_vector = vectorizer.transform([query]).toarray()
    distances, indices = index.search(query_vector, k)

    return indices[0]

def generate_explanation(question, options, correct_answer): 

    prompt = PromptTemplate(
        input_variables=["question", "correct_answer"],
        template="Provide an explanation for the following question and answer:\n\nQuestion: {question}\nCorrect Answer: {correct_answer}\nOptions: {options}\n\nExplanation:"
    )
    chain = prompt | llm

    return chain.invoke({"question": question, "options": options, "correct_answer": correct_answer}).content

def generate_question_and_answer(content): 

    response_schemas = [
        ResponseSchema(name="question", description="The multiple choice question"),
        ResponseSchema(name="option_a", description="Option A for the question"),
        ResponseSchema(name="option_b", description="Option B for the question"),
        ResponseSchema(name="option_c", description="Option C for the question"),
        ResponseSchema(name="option_d", description="Option D for the question"),
        ResponseSchema(name="correct_answer", description="The correct answer for the question which should be one of 'Option A', 'Option B', 'Option C', or 'Option D'."),
    ]

    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)

    prompt = PromptTemplate(
        input_variables=["content"],
        template="""
            Generate a multiple-choice question based on the following content.

            Content: {content}

            {format_instructions}
            """,

        partial_variables={"format_instructions": output_parser.get_format_instructions()}
    )

    chain = prompt | llm

    result = chain.invoke(content)
    result = output_parser.parse(result.content)

    question = result.get("question")
    correct_option = result.get("correct_answer")


    options = ["Option A", "Option B", "Option C", "Option D"]
    answers = [result.get("option_a"),
               result.get("option_b"),
               result.get("option_c"),
               result.get("option_d")]
    
    pre_answers = ["A. ", "B. ", "C. ", "D. "]
    options_answers = zip(options, answers)
    correct_answer = [answer for option, answer in options_answers if option.strip() == correct_option.strip()][0]

    random.shuffle(options)
    explanation = generate_explanation(question, answers, correct_answer)
    question = question + '\n' + " ".join([pre + answer for pre, answer in zip(pre_answers, answers)])
    
    return question, options, correct_answer, correct_option, explanation

def generate_question(content): 
    question, options, correct_answer, correct_option, explanation = generate_question_and_answer(content)
    
    return question, options, correct_answer, correct_option, explanation

def check_answer(user_answer, correct_answer, explanation, score, count):

    if user_answer == correct_answer:
        score += 1
        result = "Correct!"
    else: 
        result = "Incorrect."

    explanation_text = f"Your answer: {user_answer} -- Correct answer: {correct_answer} -- Explanation: {explanation}"
    count += 1

    return result, explanation_text, score, count

def start_quiz():
    num_questions = 7
    file = "./data/file.pdf"

    text_chunks = text_to_chunks(file)
    index, vectorizer = index_chunks(text_chunks)
    chunk_indices = list(range(len(text_chunks)))
    random.shuffle(chunk_indices)

    used_indices = []
    first_index = chunk_indices.pop(0)
    used_indices.append(first_index)
    
    question, options, correct_answer, correct_option, explanation = generate_question(text_chunks[first_index])

    return "", question, options, correct_answer, correct_option, explanation, 0, 0, "", "", options, index, vectorizer, text_chunks, used_indices, num_questions, "Score: 0"

def submit_answer(user_answer, correct_answer, correct_option, explanation, score, count, index, vectorizer, text_chunks, used_indices, total_questions=7): 

    result, explanation_text, score, count = check_answer(user_answer, correct_option, explanation, score, count)
    score_text = f"Score: {score}/{total_questions}"

    if count >= total_questions: 
        grade = f"Your final score is {score} out of {total_questions}."
        return "", "", "", "", "", result, explanation_text, score, count, grade, [], index, vectorizer, text_chunks, used_indices, total_questions, score_text
    
    chunk_indices = list(set(range(len(text_chunks))) - set(used_indices))
    if not chunk_indices: 
        return "No more questions available", [], "", "", used_indices, None, None, None
    
    next_index = random.choice(chunk_indices)
    used_indices.append(next_index)
    question, options, correct_answer, correct_option, explanation = generate_question(text_chunks[next_index])

    return (
        question, options, correct_answer, correct_option, explanation, result, explanation_text, score, count, "", options, index, vectorizer, text_chunks, used_indices, total_questions, score_text
    )