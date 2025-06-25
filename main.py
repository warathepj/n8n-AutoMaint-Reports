from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import os
import sys

# Add the current directory to the Python path to import chart.py
sys.path.append(os.path.dirname(__file__))

from chart import (
    generate_average_repair_time_chart,
    generate_problem_description_frequency_chart,
    generate_cost_of_parts_by_asset_type_chart
)

app = FastAPI()

REPORT_DIR = "report"

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
        return {"message": "Charts generated successfully in the 'report' directory."}
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
