from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import os
import sys
import requests # Import the requests library

# Add the current directory to the Python path to import chart.py
sys.path.append(os.path.dirname(__file__))

from chart import (
    generate_average_repair_time_chart,
    generate_problem_description_frequency_chart,
    generate_cost_of_parts_by_asset_type_chart
)

app = FastAPI()

REPORT_DIR = "report"
N8N_WEBHOOK_URL = "http://localhost:5678/webhook-test/bf6d593f-82b8-4eee-9de5-f35e1ad5630f" # Define the n8n webhook URL

@app.on_event("startup")
async def startup_event():
    """
    Ensures the report directory exists on application startup.
    """
    os.makedirs(REPORT_DIR, exist_ok=True)
    print(f"Ensured directory '{REPORT_DIR}' exists.")

@app.get("/")
async def read_root():
    return {"message": "Welcome to the AutoMaint Reports API. Use /generate-charts to create reports."}

@app.post("/generate-charts")
async def generate_charts_endpoint():
    """
    Endpoint to trigger the generation of all charts.
    """
    try:
        print("Generating charts...")
        generate_average_repair_time_chart(output_file=os.path.join(REPORT_DIR, 'average_repair_time_by_asset_type.png'))
        generate_problem_description_frequency_chart(output_file=os.path.join(REPORT_DIR, 'problem_description_frequency.png'))
        generate_cost_of_parts_by_asset_type_chart(output_file=os.path.join(REPORT_DIR, 'cost_of_parts_by_asset_type.png'))
        print("Charts generated successfully.")

        # TODO Construct chart URLs, Telegram need https, can use ngrok or similar for local testing
        base_url = "https://your-url/report/"
        chart_links = {
            "average_repair_time_chart": f"{base_url}average_repair_time_by_asset_type.png",
            "problem_description_frequency_chart": f"{base_url}problem_description_frequency.png",
            "cost_of_parts_by_asset_type_chart": f"{base_url}cost_of_parts_by_asset_type.png"
        }

        # Send chart links to n8n webhook
        try:
            response = requests.post(N8N_WEBHOOK_URL, json=chart_links)
            response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
            print(f"Chart links sent to n8n successfully. Response: {response.status_code}")
        except requests.exceptions.RequestException as req_e:
            print(f"Error sending chart links to n8n: {req_e}")
            raise HTTPException(status_code=500, detail=f"Error sending chart links to n8n: {req_e}")

        return {"message": "Charts generated successfully and links sent to n8n."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating charts: {e}")

# You can add endpoints to serve the generated charts if needed
@app.get("/report/{filename}")
async def get_report_image(filename: str):
    file_path = os.path.join(REPORT_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    raise HTTPException(status_code=404, detail="File not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
