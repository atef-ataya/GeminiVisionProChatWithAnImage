import os
import streamlit as st
import google.generativeai as genai

from dotenv import load_dotenv, find_dotenv

def chat_func(prompt, img):
    model = genai.GenerativeModel('gemini-pro-vision')

    try:
        response = model.generate_content([prompt, img])
        return response.text
    except Exception as e:
        return f"An error occured: {e}. Please try again."

def convert_image_to_pil(st_image):
    import io
    from PIL import Image
    image_data = st_image.read()
    pil_image = Image.open(io.BytesIO(image_data))
    return pil_image

if __name__ == "__main__":
    load_dotenv(find_dotenv(), override=True)
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

    st.image('banner.png')
    st.title('💬 Chatbot')

    img = st.file_uploader("Upload an image", type=['png', 'jpg', 'jpeg','gif'])

    if img:
        st.image(img, caption='Chat with this image')

        prompt = st.text_area('Ask a question about your image:')

        if prompt:
            pil_image = convert_image_to_pil(img)

            with st.spinner('Analyzing your image ...'):
                answer = chat_func(prompt, pil_image)
                st.text_area('Gemini Answer: ', value=answer)


            if 'history' not in st.session_state:
                st.session_state.history = 'Chat History\n'

            value = f'**Question**: {prompt}: \n\n **Answer**: {answer}'
            st.session_state.history = f'{value} \n\n {"-" * 100} \n\n {st.session_state.history}'

            h = st.session_state.history
            st.text_area(label='Chat History:', value=h, height=800, key='history')

