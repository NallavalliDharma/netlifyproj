from flask import Flask
import requests
import json
import uuid
app = Flask(__name__)

@app.route("/menu",methods=["GET","POST"])
def get_the_food():
  with open("./data.json","r") as file:
    data = json.load(file)
    return data["menu"]

@app.post("/menu/<nameoffood>/price/<int:quantity>/<status>")
def place_order(nameoffood,quantity,status):
  with open("./data.json","r") as file:
    data = json.load(file)
    price = 0
    for item in data["menu"]:
      if nameoffood.lower() == item["name"].lower():
        price = item["price"]
        break
    if price == 0:
      return "No Food Item"
    
    new_order = {
      
      "orderId" : str(uuid.uuid4()),
      "orderStatus" : status,
      "orderItems" : [
        {
         "name" : nameoffood,
         "price" : price,
         "quantity" : quantity

         }
      ]
    }
    data["orders"].append(new_order)
    with open("./data.json","w") as file:
        json.dump(data,file)
    
    return new_order


@app.patch("/menu/<orderID>/<status>")
def status_place_order(orderID,status):
  
  with open("./data.json","r") as file:
    data = json.load(file)
    for item in data["orders"]:
      if item["orderId"] == orderID:
        item["orderStatus"] = status

    # data["orders"].append(new_order)
        with open("./data.json","w") as file:
            json.dump(data,file)
        return item
  return "Item not found"



@app.delete("/menu/<orderStatus>")
def remove_Completed_food_order(orderStatus):
  with open("./data.json","r") as file:
    data = json.load(file)
  for item in data["orders"]:
    if item["orderStatus"].lower() == orderStatus.lower():
      data["orders"].remove(item)
      with open("./data.json","w")  as file:
        json.dump(data,file)
      return "order deleted"
  return "Order Not Found"


@app.get("/test")
def test():
    return {
        "message": "Flask API is working!",
        "status": "success"
    }


if __name__ == "__main__":
  app.run(debug=True)