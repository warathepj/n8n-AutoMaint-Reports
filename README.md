# ซอร์สโค้ดนี้ ใช้สำหรับเป็นตัวอย่างเท่านั้น ถ้านำไปใช้งานจริง ผู้ใช้ต้องจัดการเรื่องความปลอดภัย และ ประสิทธิภาพด้วยตัวเอง

This `n8n` workflow, named **"AutoMaint Reports Schedule"**, is designed to automatically trigger an HTTP request on a recurring schedule.

---

## Workflow Overview

This simple workflow consists of two main nodes:

1.  **Schedule Trigger**: This node initiates the workflow at a set interval.
2.  **HTTP Request**: This node sends a POST request to a specified URL.

---

## AutoMaint Reports API (Python FastAPI Application)

### Overview
This FastAPI application serves as the backend for generating and distributing maintenance reports. It leverages Python's `pandas` and `matplotlib` libraries to create insightful charts from an Excel data source (`cmms.xlsx`) and integrates with n8n workflows to automate the distribution of these reports.

### Features
*   **Chart Generation**: Dynamically generates three key maintenance charts:
    *   Average Repair Time by Asset Type
    *   Problem Description Frequency
    *   Cost of Parts by Asset Type
*   **API Endpoints**:
    *   `/generate-charts` (POST): Triggers the generation of all charts and sends their public URLs to a configured n8n webhook.
    *   `/report/{filename}` (GET): Serves the generated chart images (e.g., `average_repair_time_by_asset_type.png`) from the `/report` directory.
*   **n8n Integration**: Automatically sends the public links of the generated charts to a specified n8n webhook, enabling further automation like sending reports to Telegram or other platforms.

### Setup & Running
To run the AutoMaint Reports API:

1.  **Prerequisites**:
    *   Python 3.x
    *   `cmms.xlsx` file in the root directory (or specified path in `chart.py` functions).
2.  **Installation**:
    ```bash
    pip install fastapi uvicorn pandas matplotlib requests openpyxl
    ```
3.  **Run the Application**:
    ```bash
    uvicorn main:app --host 0.0.0.0 --port 8000
    ```
    The application will be accessible at `http://localhost:8000`.

### Dependencies
*   `fastapi`: For building the web API.
*   `uvicorn`: An ASGI server for running FastAPI applications.
*   `pandas`: For data manipulation and analysis (reading Excel, grouping data).
*   `matplotlib`: For generating charts.
*   `requests`: For sending HTTP requests to the n8n webhook.
*   `openpyxl`: A dependency for pandas to read `.xlsx` files.

### Chart Output
Generated charts are saved as PNG files in the `report/` directory within the project root. Examples:
*   `report/average_repair_time_by_asset_type.png`
*   `report/problem_description_frequency.png`
*   `report/cost_of_parts_by_asset_type.png`

---

## How it Works

The workflow operates as follows:

* The **Schedule Trigger** is configured to activate every morning **8AM**.
* Upon activation, it triggers the **HTTP Request** node.
* The **HTTP Request** node then sends a `POST` request to `http://localhost:8000/generate-charts`.

---

## Setup and Configuration

### Prerequisites

* `n8n` (workflow automation tool)
* A running service or application listening for `POST` requests on `http://localhost:8000/generate-charts`.

### Installation

1.  Create `n8n` workflow.
2.  Ensure that the `n8n` workflow is **active**. You can toggle its status within the `n8n` interface.

### Customization

* **Schedule Interval**: To change how often the workflow runs, modify the **"Schedule Trigger"** node's `interval` settings. Currently, it's set to 8 AM daily, but you can adjust it to minutes, hours, days, or more specific cron schedules.
* **HTTP Request URL**: If your chart generation service is located at a different address, update the `URL` in the **"HTTP Request"** node.
* **HTTP Request Method and Options**: You can also modify the HTTP method (e.g., GET, PUT, DELETE) or add headers, body data, and other options as required by your `http://localhost:8000/generate-charts` endpoint.

---

## Use Case

This workflow is ideal for scenarios where you need to periodically trigger an external process, such as:

* **Generating reports or charts** at regular intervals.
* **Initiating data synchronization** processes.
* **Performing health checks** on a service.
* **Triggering automated tasks** in a development or testing environment.

---

## Extending the Workflow

You can easily extend this workflow by adding more nodes after the **HTTP Request** node. For example, you could:

* **Process the response** from the `generate-charts` endpoint.
* **Send a notification** (e.g., email, Slack message) based on the success or failure of the request.
* **Log the execution** details to a file or database.
-----

# AutoMaint Reports Webhook

This n8n workflow is designed to receive maintenance reports via a webhook and automatically send various charts and data to a specified Telegram chat. This is particularly useful for teams who want to get automated visual reports directly in their communication channels.

## Features

  * **Webhook Trigger:** Initiates the workflow upon receiving a `POST` request.
  * **Automated Chart Distribution:** Sends three distinct charts related to maintenance reports to a Telegram chat:
      * Average Repair Time Chart
      * Problem Description Frequency Chart
      * Cost of Parts by Asset Type Chart

## How It Works

1.  A **Webhook** node listens for incoming `POST` requests at a specific URL.
2.  When a request is received, the workflow extracts data from the request body.
3.  Three **Telegram** nodes then take specific chart URLs from the received data and send them as messages to a predefined Telegram chat ID.

## Setup

To use this workflow, you'll need:

  * An active n8n instance.
  * A Telegram Bot Token and the chat ID where you want to send the reports.

### 1\. Create the Workflow

1.  In your n8n instance, go to **Workflows**.
2.  Click on **New** and then create a new workflow.

### 2\. Configure Credentials

This workflow requires a Telegram API credential.

1.  In the n8n editor, click on the **Telegram** nodes (there are three of them).
2.  Under the **Credentials** section, you'll see a field for **Telegram API**.
3.  If you don't have one configured, click **Create New**.
4.  Provide a **name** for your credential (e.g., "My Telegram Bot").
5.  Enter your **Telegram Bot Token**. If you don't have one, you can get it from BotFather on Telegram.
6.  Save the credential.
7.  Repeat this step for all three Telegram nodes, ensuring they use the same configured credential.

### 3\. Set Telegram Chat ID

Each Telegram node is configured to send messages to a specific `chatId`. **You must change this to your desired Telegram chat ID.**

1.  Click on each **Telegram** node.
2.  Locate the **Chat ID** field.
3.  Replace with the actual chat ID where you want the reports to be sent. You can find your chat ID by forwarding a message from the target chat to [@RawDataBot](https://t.me/RawDataBot) on Telegram.

### 4\. Activate the Workflow

After configuring the credentials and chat ID:

1.  Toggle the workflow to **Active** in the top right corner of the n8n editor.

### 5\. Obtain the Webhook URL

Once the workflow is active, you'll need the webhook URL to send data to it.

1.  Click on the **Webhook** node.
2.  The **Webhook URL** will be displayed in the node's settings. It should look something like `YOUR_N8N_INSTANCE_URL/webhook/bf6d593f-82b8-4eee-9de5-f35e1ad5630f`.

## Usage

To trigger this workflow, send a `POST` request to the obtained Webhook URL with a JSON body containing the chart URLs. The workflow expects the following keys in the JSON body:

  * `average_repair_time_chart`: URL of the average repair time chart.
  * `problem_description_frequency_chart`: URL of the problem description frequency chart.
  * `cost_of_parts_by_asset_type_chart`: URL of the cost of parts by asset type chart.

### Example `POST` Request Body:

```json
{
  "average_repair_time_chart": "https://example.com/charts/avg_repair_time.png",
  "problem_description_frequency_chart": "https://example.com/charts/problem_freq.png",
  "cost_of_parts_by_asset_type_chart": "https://example.com/charts/cost_by_asset.png"
}
```

You can use tools like `curl`, Postman, or any programming language to send this `POST` request.
