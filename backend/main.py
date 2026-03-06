from services.availability_service import AvailabilityService 
from services.booking_service import BookingService
from services.payment_service import PaymentService
from entities.client import Client
from entities.service import Service
from entities.timeslot import TimeSlot

from patterns.strategy.credit_card import CreditCard
from patterns.strategy.debit_card import DebitCard
from patterns.strategy.paypal import Paypal
from patterns.strategy.bank_transfer import BankTransfer

def main():
    available_services = AvailabilityService()
    booking_service = BookingService()
    payment_service = PaymentService()
    

    print("=====================================")
    print("Welcome to Consulting Booking System\n")
    print("=====================================")

    print("1. Browse our Services")
    print("2. Book a Session")
    print("3. Make a Payment")
    print("4. Exit")

    choice = input("Select Option: ")

    if choice == "1":
       services = available_services.browse_services()
       for s in services:
           print(s)
       
    elif choice == "2":
        userid = input("Enter userId: ")
        name = input("Enter name: ")
        email = input("Enter email: ")
        service_choice = input("Enter Service: ") #in phase 2 this will be changed to actually create the service object, for now it assume this does that 
        slot = input("Enter TimeSlot: ") #in phase 2 this will be changed to actually create the timeslot object, for now it assume this does that 

        services = available_services.browse_services() 

        #finding the service object 
        selected_service = None 
        for s in services:
            if s.name == service_choice:
                selected_service =s
                break

        if selected_service:
            consultant = selected_service.consultant
        else:
            raise Exception("Invalid Service")

        client = Client(userid,name,email)
    
        #time slot object 
        timeslot = TimeSlot(slot)

        book = booking_service.create_booking(client,consultant,service_choice,slot)


        #consultant accepting or rejecting 
        available_slot = consultant.get_available_timeslots()

        if timeslot in available_slot:
            booking_service.confirm_booking(book)
        else:
            booking_service.reject_booking(book)

    elif choice == "3":
        print("If you haven't made a booking yet, please go back and make a booking\n")

        booking_id = input("Enter Booking Id: ")


        print("1. Credit Card")
        print("2. Debit Card")
        print("3. PayPal")
        print("4. Bank transfer")

        payment_choice = input("Enter payment Method: ") #in phase 2 this will ask for the correct choice like credit or debit etc and will direct it to enter the correct details needed to actually create the PaymentMethod Object 
        amount = float(input("Enter amount"))

        booking = booking_service.get_booking(booking_id)
        
        if not booking:
            raise Exception("booking id entered is invalid")
        
        #create correct payment strategy 
        if payment_choice == "1":
            payment_method = CreditCard()
        elif payment_choice == "2":
            payment_method = DebitCard()
        elif payment_choice == "3":
            payment_method = Paypal()
        elif payment_choice == "4":
            payment_method = BankTransfer()
        else:
            raise Exception("Invalid payment method")
        
        result = payment_service.process_payment(booking, payment_method, amount)
        
        if result is not None:
            print("Payment Processed Successfully")
        else:
            print("Something went Wrong, please try again")

    elif choice == "4":
        print("Goodbye")

    else:
        print("Invalid Choice")

if __name__ == "__main__":
    main()


        




