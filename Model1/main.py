from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from ClientModel import predict_values
from fastapi import Query
from typing import List
import pathlib
# Define FastAPI instance
app = FastAPI()

# Mount the static directory
# app.mount("/static", StaticFiles(directory="D:/OneDrive/Private/Books/Computer/DataAnalytics/Data/Labo/clients/Model1/app/static"), name="static")
# current_dir = pathlib.Path().resolve()


# Define Pydantic model for the request body
class ValuesModel(BaseModel):
    values: list[float]  # Expect a list of integers

# Define a route to serve the index.html page
@app.get("/", response_class=HTMLResponse)
async def serve_index():
    return """Hello World<br><br>
              End Point for Query Parameter:<br> https://model1-test.de.r.appspot.com/send-values-qry?values=1&values=2&values=3&values=4&values=5&values=6&values=7&values=8<br>
              Method : GET<br>
              Sample Input: ?values=1&values=2&values=3&values=4&values=5&values=6&values=7&values=8<br>
              where 1,2,3... are user inputs, user need to provide 8 integer to float values.<br>In query string "values" is keyword so keep it as it is.<br><br>
              End Point for JSON:<br>https://model1-test.de.r.appspot.com/send-values<br>
              Method : POST<br>
              Sample Input: { "values": [1, 2, 3, 4, 5, 6, 7, 8] }<br><br>
              Sample Output:
              {
  "Status": "Values received and processed successfully",
  "Values": [
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8
  ],
  "Predicted Output": [
    "dibetese"
  ],
  "Model": "This is a Bayes Gaussian model trained on the Diabetes.csv database. \n Date Trained on: 03 September, 2024"
}
           """
    # with open("static/index.html", "r") as file:
    #     content = file.read()
    # return HTMLResponse(content=content)

@app.get("/home", response_class=HTMLResponse)
async def serve_home():
    with open("static/index.html", "r") as file:
        content = file.read()
    return HTMLResponse(content=content)

# Serve the index.html at the root
# @app.get("/", response_class=HTMLResponse)
# async def read_root():
#     with open("static/index.html") as f:
#         return f.read()

# Define the route to accept 8 values and process them
#Json format for send_values : {"values": [1, 1, 31, 2, 2, 2, 2, 0]}
@app.post("/send-values")
async def send_values(values_model: ValuesModel):
    user_values = values_model.values

    # Check if exactly 8 values are provided
    if len(user_values) != 8:
        raise HTTPException(status_code=400, detail="Please provide exactly 8 integer values")

    # Get prediction results
    try:
        result = predict_values(user_values)  # Modify this if predict_values does not return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

   
    # Return a success message
    response = {
        "Status": "Values received and processed successfully",
        "Values": user_values,
        "Predicted Output": result["prediction"],  # Use the prediction from result
        "Model": result["description"]       # Include description in the response
    }

    # Return the response
    return response


# Define the route to accept 8 values through query
# format: http://localhost:8000/send-values-qry?values=1&values=2&values=3&values=4&values=5&values=6&values=7&values=8
@app.get("/send-values-qry")
async def send_values(values: List[int] = Query(...)):
    user_values = values

    # Check if exactly 8 values are provided
    if len(user_values) != 8:
        raise HTTPException(status_code=400, detail="Please provide exactly 8 integer values")

    # Get prediction results
    try:
        result = predict_values(user_values)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

    # Return a success message
    response = {
        "Status": "Values received and processed successfully",
        "Values": user_values,
        "Predicted Output": result["prediction"],
        "Model": result["description"]
    }

    return response



# Run the FastAPI server if executed as the main script
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)