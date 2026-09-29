from models.customer import Customer

class CustomerRepository:
    
    def __init__(self):
        self.customers = [
            Customer("1", "John"),
            Customer("2", "Jane")
        ]
    
    def find_all(self):
        return self.customers
    
    def find_by_id(self, customer_id):
        for customer in self.customers:
            if customer.id == customer_id:
                return customer
        
        return None
    
    def save(self, customer):
        existing = self.find_by_id(customer.id)
        if existing:
            existing.name = customer.name
            return existing
        
        self.customers.append(customer)
        return customer
    
    def delete_by_id(self, customer_id):
        customer = self.find_by_id(customer_id)
        if customer:
            self.customers.remove(customer)
            return True
        return False
    