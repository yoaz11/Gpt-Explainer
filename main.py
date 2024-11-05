import os
import argparse
import asyncio
from extract_text import extract_text_from_pptx
from fetch_explanation import get_explanations, save_explanations

def main():
    """
    Main function to parse arguments and execute the script.
    """
    parser = argparse.ArgumentParser(description="Explain PowerPoint presentations using GPT-3.5")
    parser.add_argument("pptx_path", type=str, help="Path to the PowerPoint file")
    args = parser.parse_args()

    pptx_path = args.pptx_path
    if not os.path.exists(pptx_path):
        print(f"File not found: {pptx_path}")
        return

    output_path = os.path.splitext(pptx_path)[0] + ".json"

    asyncio.run(async_main(pptx_path, output_path))

async def async_main(pptx_path, output_path):
    """
    Asynchronous main function to handle the workflow of extracting text,
    fetching explanations, and saving the results.

    Args:
        pptx_path (str): The path to the PowerPoint file.
        output_path (str): The path to the output JSON file.
    """
    slides_texts = extract_text_from_pptx(pptx_path)  # No await here since it's a synchronous function
    explanations = await get_explanations(slides_texts)
    save_explanations(explanations, output_path)
    print(f"Explanations saved to {output_path}")

if __name__ == "__main__":
    main()
