from locust import HttpUser, task, between, TaskSet

userAndFinancialData = {
  "user": {
    "name": "John Doe",
    "contact": "john.doe@example.com"
  },
  "creditCard": {
    "number": "4111111111111111",
    "expirationDate": "12/25",
    "cvv": "123"
  },
  "userComment": "Please handle with care.",
  "billingAddress": {
    "street": "123 Main St",
    "city": "Springfield",
    "state": "IL",
    "zip": "62701",
    "country": "USA"
  },
  "shippingMethod": "Standard",
  "giftWrapping": True,
  "termsAccepted": True
}

books = [
    {
      "name": "Book A",
      "quantity": 1
    },
    {
      "name": "Book B",
      "quantity": 2
    },
    {
      "name": "Book C",
      "quantity": 3
    }
  ]

class BaseOrderMaking(TaskSet):
    def makeOrder(self, data):
        with self.client.post("/checkout", json=data, catch_response=True) as response:
            #print(f"Response status code: {response.status_code}")
            #print(response)
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Failed with {response.status_code}")

class SingleCorrectOrder(BaseOrderMaking):
    @task
    def CorrectOrder(self):
        data = userAndFinancialData.copy()
        data["items"] = books
        #print(f"Making order with data: {data}")
        self.makeOrder(data)

class MultipleCorrectOrder(BaseOrderMaking):
    @task
    def CorrectOrderA(self):
        data = userAndFinancialData.copy()
        data["items"] = [ {
                "name": "Book A",
                "quantity": 1
        }]
        #print(f"Making order with data: {data}")
        self.makeOrder(data)

    @task
    def CorrectOrderB(self):
        data = userAndFinancialData.copy()
        data["items"] = [ {
                "name": "Book B",
                "quantity": 3
        }]
        #print(f"Making order with data: {data}")
        self.makeOrder(data)
    
    @task
    def CorrectOrderC(self):
        data = userAndFinancialData.copy()
        data["items"] = [ {
                "name": "Book C",
                "quantity": 2
        }]
        #print(f"Making order with data: {data}")
        self.makeOrder(data)

def MultipleMixed(BaseOrderMaking):
    @task
    def CorrectOrderA(self):
        data = userAndFinancialData.copy()
        data["items"] = [ {
                "name": "Book A",
                "quantity": 1
        }]
        self.makeOrder(data)

    @task
    def FradulentOrderB(self):
        data = userAndFinancialData.copy()
        data["creditCard"]["expirationDate"] = "12/20"
        data["items"] = [ {
                "name": "Book B",
                "quantity": 3
        }]
        self.makeOrder(data)
    @task
    def FraudulentOrderC(self):
        data = userAndFinancialData.copy()
        data["creditCard"]["number"] = "123"
        data["items"] = [ {
                "name": "Book C",
                "quantity": 2
        }]
        self.makeOrder(data)
    @task
    def FraudulentOrderD(self):
        data = userAndFinancialData.copy()
        data["user"]["contact"] = "abcnotanemail"
        data["items"] = [ {
                "name": "Book D",
                "quantity": 2
        }]
        self.makeOrder(data)

def ConflictingOrders(BaseOrderMaking):
    @task
    def CorrectOrderA(self):
        data = userAndFinancialData.copy()
        data["items"] = [ {
                "name": "Book A",
                "quantity": 1
            },
            {
                "name": "Book B",
                "quantity": 2
            }
        ]
        self.makeOrder(data)

    @task
    def CorrectOrderB(self):
        data = userAndFinancialData.copy()
        data["items"]= [ {
                "name": "Book A",
                "quantity": 2
            },
            {
                "name": "Book B",
                "quantity": 1
            }
        ]
        self.makeOrder(data)

    @task
    def CorrectOrderC(self):
        data = userAndFinancialData.copy()
        data["items"]= [ {
                "name": "Book B",
                "quantity": 3
            },
            {
                "name": "Book C",
                "quantity": 2
            }
        ]
        self.makeOrder(data)

    @task
    def CorrectOrderD(self):
        data = userAndFinancialData.copy()
        data["items"]= [ {
                "name": "Book A",
                "quantity": 1
            },
            {
                "name": "Book C",
                "quantity": 2
            }
        ]
        self.makeOrder(data)

class WebsiteUserSingleCorrect(HttpUser):
    wait_time = between(1,2)
    tasks = [SingleCorrectOrder]
    host = "http://localhost:8081"

class WebsiteUserMultipleCorrect(HttpUser):
    wait_time = between(1, 2)
    tasks = [MultipleCorrectOrder]
    host = "http://localhost:8081"

class WebsiteUserMultipleMixed(HttpUser):
    wait_time = between(1, 2)
    tasks = [MultipleMixed]
    host = "http://localhost:8081"

class WebsiteUserConflictingOrders(HttpUser):
    wait_time = between(1, 2)
    tasks = [MultipleMixed]
    host = "http://localhost:8081"