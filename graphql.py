import graphene
from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)


class Stocks(graphene.ObjectType):
    ticker = graphene.String()
    name = graphene.String()
    price = graphene.Float()


class Query(graphene.ObjectType):
    stocks = graphene.List(Stocks)

    def resolve_stocks(self, info):
        try:
            response = requests.get("http://127.0.0.1:5000/")
            response.raise_for_status()
            stocks = response.json()

            graphql_stocks = [
                Stocks(ticker=stock["ticker"], name=stock["name"], price=stock["price"])
                for stock in stocks
            ]

            return graphql_stocks
        except Exception as e:
            print(f"Error fetching data from REST API: {str(e)}")
            return []


schema = graphene.Schema(query=Query)


@app.route("/", methods=["GET"])
def hello_world():
    return "Hello, World!"


@app.route("/graphql", methods=["POST"])
def graphql():
    data = request.get_json()
    query = data["query"]
    variables = data.get("variables")
    result = schema.execute(query, variables=variables)
    return jsonify(result.to_dict())


if __name__ == "__main__":
    app.run(debug=True)
