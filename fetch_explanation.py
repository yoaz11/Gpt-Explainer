import openai
import asyncio
import json


async def fetch_explanation(slide_text, index):
    """
    Sends a slide's text to the OpenAI API to get an explanation.

    Args:
        slide_text (str): The text content of a slide.
        index (int): The index of the slide.

    Returns:
        dict: A dictionary containing the slide index and the explanation.
    """
    prompt = f"Explain the following slide content in detail:\n\n{slide_text}"
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return {"index": index, "explanation": response.choices[0].message["content"]}
    except Exception as e:
        return {"index": index, "explanation": f"Exception: {str(e)}"}

async def get_explanations(slides_texts):
    """
    Processes all slides' texts to fetch explanations concurrently.

    Args:
        slides_texts (list): A list of texts from each slide.

    Returns:
        list: A list of dictionaries containing explanations for each slide.
    """
    tasks = [fetch_explanation(text, idx) for idx, text in enumerate(slides_texts)]
    explanations = await asyncio.gather(*tasks)
    return explanations

def save_explanations(explanations, output_path):
    """
    Saves the explanations to a JSON file.

    Args:
        explanations (list): A list of explanations for each slide.
        output_path (str): The path to the output JSON file.
    """
    with open(output_path, "w") as f:
        json.dump(explanations, f, indent=4)
