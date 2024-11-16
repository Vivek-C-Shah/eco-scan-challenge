# main.py

import os
import base64
import json
from fastapi import FastAPI, UploadFile, File, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import openai
from dotenv import load_dotenv
from pydantic import BaseModel

from carbon_scores import CARBON_SCORES
from offers import OFFERS
from utils import calculate_reward_points, parse_gpt_response

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# Allow CORS for frontend to access the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze-image")
async def analyze_image(file: UploadFile = File(...)):
    try:
        # Read image file
        image_bytes = await file.read()
        # Encode image to base64
        base64_image = base64.b64encode(image_bytes).decode('utf-8')

        # Prepare the message content
        messages = [
            {
                "role": "system",
                "content": f"""You need to just answer with a JSON array of clothing items in the image. 
                The possible items are {CARBON_SCORES.keys()}.
                The JSON array should be in the following format:
                [
                    "item1",
                    "item2",
                    "item3",
                    ...
                ]
                
                You should only answer with the JSON array and nothing else.
                
                If the image contains multiple items, return a JSON array with all the items.
                
                If the image doesn't contain any clothing items, return an empty JSON array.
                
                Strictly follow the above instructions. Don't add any extra text. Do just use the possible items.
                If there are multiple number of same items then output it in an array format only:
                [
                    "item1",
                    "item1",
                    "item2",
                    ...
                ]
                """,
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "List the clothing items in this image in JSON array format."},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        },
                    },
                ],
            }
        ]

        # Call OpenAI API
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=300,
        )

        # Extract response content
        # print(f"GPT full response: {response}")
        response_content = response.choices[0].message.content
        print(f"GPT response: {response_content}")
        # Parse GPT response to get identified items
        identified_items = parse_gpt_response(response_content)

        # Get carbon scores for identified items
        carbon_scores = {item: CARBON_SCORES.get(item.lower(), 0) for item in identified_items}

        return {"identified_items": identified_items, "carbon_scores": carbon_scores}

    except Exception as e:
        print(f"Error analyzing image: {e}")
        raise HTTPException(status_code=500, detail=str(e))

class CalculateEcoScoreRequest(BaseModel):
    items: List[str]

@app.post("/calculate-eco-score")
async def calculate_eco_score(request: CalculateEcoScoreRequest):
    try:
        items = request.items
        total_carbon_score = sum(CARBON_SCORES.get(item.lower(), 0) for item in items)
        eco_reward_points = calculate_reward_points(total_carbon_score)
        return {
            "total_carbon_score": total_carbon_score,
            "eco_reward_points": eco_reward_points
        }
    except Exception as e:
        print(f"Error calculating eco-score: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/get-offers")
async def get_offers(points: int):
    try:
        available_offers = [offer for offer in OFFERS if offer['points_required'] <= points]
        return {"available_offers": available_offers}
    except Exception as e:
        print(f"Error getting offers: {e}")
        raise HTTPException(status_code=500, detail=str(e))
