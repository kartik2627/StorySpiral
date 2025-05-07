import streamlit as st
import openai
import os

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Title
st.set_page_config(page_title="AI Story Generator with Plot Twists")
st.title("🎨 AI Story Generator with Dynamic Plot Twists")

# Sidebar - Input Parameters
st.sidebar.header("🔢 Story Parameters")
genre = st.sidebar.selectbox("Genre", ["Fantasy", "Sci-Fi", "Horror", "Romance", "Mystery"])
characters = st.sidebar.text_area("Main Characters", "Alice the explorer, Bob the wizard")
setting = st.sidebar.text_input("Setting", "Ancient ruins in a hidden jungle")
story_length = st.sidebar.selectbox("Story Length", ["Short", "Medium", "Long"])
num_twists = st.sidebar.slider("Number of Plot Twists", 1, 3, 2)
generate_button = st.sidebar.button("📚 Generate Story")

# Function to generate the story using GPT
@st.cache_data(show_spinner=True)
def generate_story(genre, characters, setting, story_length, num_twists):
    prompt = f"""
    You are a master storyteller.
    Write a {story_length.lower()} {genre} story.
    Characters: {characters}
    Setting: {setting}
    The story must include {num_twists} unexpected plot twist(s).
    Make the story engaging and immersive.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a creative story writer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.8,
        max_tokens=1500
    )

    return response['choices'][0]['message']['content']

# Function to generate image from DALL-E
def generate_image(prompt):
    dalle_response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="512x512"
    )
    return dalle_response['data'][0]['url']

# Main App Logic
if generate_button:
    with st.spinner("Generating story and image..."):
        story = generate_story(genre, characters, setting, story_length, num_twists)
        image_url = generate_image(f"A scene from a {genre} story set in {setting}")

    st.header("📚 Generated Story")
    st.write(story)

    st.header("🌍 Generated Illustration")
    st.image(image_url, caption="AI-generated scene using DALL·E", use_column_width=True)

    st.success("Story and image generated successfully!")

# Footer
st.markdown("---")
st.markdown("Made with ❤️ using GPT-4 and DALL·E")
