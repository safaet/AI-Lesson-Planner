import os 
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
import streamlit as st 

load_dotenv()

def LLM_Setup(prompt):
    try:
        model = ChatGroq(
            # Updated to use a currently supported model
            model="mixtral-8x7b-32768",
            groq_api_key=os.getenv('key')
        )

        parser = StrOutputParser()
        output = model | parser 
        output = output.invoke(prompt)
        return output
    except Exception as e:
        st.error(f"Error generating lesson plan: {str(e)}")
        return None

st.title('AI Lesson Planner')

# Add some helpful descriptions
st.write("Create customized lesson plans with AI assistance")

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
                f"Generate a detailed lesson plan for the subject of {subject} on the topic of {topic}. "
                f"This lesson is intended for {grade} students and will last for {duration}. "
                f"The following are the learning objectives: {learning_objectives}. "
                f"Return the results as Markdown and don't return class size. "
                f"This is how the user wants the plan to be customized: {customization}. "
                f"Format the response in clean, well-structured Markdown."
            )
            llm_output = LLM_Setup(prompt)
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