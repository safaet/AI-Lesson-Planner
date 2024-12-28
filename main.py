import os 
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
import streamlit as st 
from PIL import Image  # Add this import
import openai  # Add this import

load_dotenv()


st.set_page_config(
    page_title="AI Lesson Planner",
    page_icon="📚",
    # layout="wide"
)


header = st.container()

# Add logo and title in a side-by-side layout
with header:
    col1, col2 = st.columns([1, 4])
    
    with col1:
        # Replace 'logo.png' with your logo file name
        logo = Image.open('logo.jpg')
        st.image(logo, width=100)  # Adjust width as needed
    
    with col2:
        st.title('AI Lesson Planner')
        st.write("Create customized lesson plans with AI assistance")


# def LLM_Setup(prompt):
#     try:
#         model = ChatGroq(
#             # Updated to use a currently supported model
#             model="mixtral-8x7b-32768",
#             groq_api_key=os.getenv('key')
#         )

#         parser = StrOutputParser()
#         output = model | parser 
#         output = output.invoke(prompt)
#         return output
#     except Exception as e:
#         st.error(f"Error generating lesson plan: {str(e)}")
#         return None


def generate_lesson_plan(prompt):
    try:
        openai.api_key = os.getenv('OPENAI_API_KEY')
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful AI for generating lesson plans."},
                {"role": "user", "content": prompt}
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        st.error(f"Error generating lesson plan: {str(e)}")
        return None

# Form inputs with descriptions
subject = st.text_input(
    label='Subject',
    placeholder='e.g., Science, Math, English'
)
topic = st.text_input(
    label='Topic',
    placeholder='e.g., Solar System, Fractions, Poetry'
)
grade = st.text_input(
    label='Grade',
    placeholder='e.g., 5, 9, 12'
)
duration = st.text_input(
    label='Duration',
    placeholder='e.g., one hour, 45 minutes'
)
learning_objectives = st.text_area(
    label='Learning Objectives',
    placeholder='What should students learn from this lesson?'
)
customization = st.text_area(
    label='Customization',
    placeholder='Any specific requirements or preferences for the lesson?'
)

if st.button('Generate Lesson Plan'):
    if not subject or not topic or not grade or not duration or not learning_objectives:
        st.warning('Please fill out all required fields before generating the lesson plan.')
    else:
        with st.spinner('Generating your lesson plan...'):
            prompt = (
                f"Create a detailed lesson plan for students studying {subject} on the topic '{topic}'. "
                f"The lesson is targeted at grade {grade} students and should span {duration}. "
                f"The learning objectives for this lesson are: {learning_objectives}. "
                f"Customize the plan based on the following requirements: {customization}. "
                f"Provide the lesson plan formatted in clean, structured Markdown, displayed in a table format. "
                f"Ensure the entire response is in Bengali language. Avoid including class size in the response."
            )

            # llm_output = LLM_Setup(prompt)
            llm_output = generate_lesson_plan(prompt)
            if llm_output:
                st.success('Lesson plan generated successfully!')
                st.markdown(llm_output)

# Optional: Add a footer with usage instructions
st.markdown("""
---
### How to use:
1. Fill in all the required fields
2. Click 'Generate Lesson Plan'
3. Wait for the AI to create your customized lesson plan
""")