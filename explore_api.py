from app import CSE_API

cse = CSE_API()

data = {
    "symbol": "ABAN.N0000"
}
result = cse.get_top_gainers()

print(result)