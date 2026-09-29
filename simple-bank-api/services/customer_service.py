from models.customer import Customer
from repos.customer_repository import CustomerRepository

class CustomerService:
    def __init__(self, customer_repository):
        self.customer_repository = customer_repository
    
    def get_all_customers(self):
        return self.customer_repository.find_all()
    
    def get_customer_by_id(self, customer_id):
        return self.customer_repository.find_by_id(customer_id)
    
    def create_customer(self, customer):
        return self.customer_repository.save(customer)
    
    def update_customer(self, customer_id, name):
        customer = self.customer_repository.find_by_id(customer_id)
        if customer is None:
            return None
        
        customer.name = name
        return self.customer_repository.save(customer)
    
    def delete_customer(self, customer_id):
        return self.customer_repository.delete_by_id(customer_id)
