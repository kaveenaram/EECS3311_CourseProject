from services.availability_service import AvailableServices 
from services.booking_service import BookingService
from services.payment_service import PaymentService
from entities.client import Client
from entities.service import Service
from entities.timeslot import TimeSlot

def main():
    available_services = AvailableServices()
    booking_service = BookingService()
    payment_service = PaymentService()
    
    service = Service() # to be changed and add to choice 2 section after available_service.py file is done 
    slot = TimeSlot() # to be changed and add to choice 2 section after available_service.py file is done 

    print("=====================================")
    print("Welcome to Consulting Booking System\n")
    print("=====================================")

    print("1. Browse our Services")
    print("2. Book a Session")
    print("3. Make a Payment")
    print("4. Exit")

    choice = input("Select Option: ")

    if choice == "1":
       available_services.show() #To be changes after the available_service.py file is done 
       
    elif choice == "2":
        userid = input("Enter userId: ")
        name = input("Enter name: ")
        email = input("Enter email: ")

        
        consultant = service.consultant #consultant that provide that service 

        client = Client(userid,name,email)
        book = booking_service.create_booking(client,consultant,service,slot)


        #consultant accepting or rejecting 
        available_slot = consultant.get_available_timeslots()

        if slot in available_slot:
            booking_service.confirm_booking(book)
        else:
            booking_service.reject_booking(book)

    elif choice == "3":
        print("If you haven't made a booking yet, please go back and make a booking\n")

        booking_id = input("Enter Booking Id: ")
        payment_method = ("Enter payment Method: ") #in phase 2 this will ask for the correct choice like credit or debit etc and will direct it to enter the correct details needed to actually create the PaymentMethod Object 
        amount = float(input("Enter amount"))

        booking = booking_service.get_booking(booking_id)
        
        if booking:
            result = payment_service.process_payment(booking,payment_method,amount)
        else:
            raise Exception("booking id entered is invalid")
        
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


        




