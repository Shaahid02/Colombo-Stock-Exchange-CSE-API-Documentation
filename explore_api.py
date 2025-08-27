from app import CSE_API

cse = CSE_API()

data = {
    
}
result = cse.get_financial_announcements()

print(result)