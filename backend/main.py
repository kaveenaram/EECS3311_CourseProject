from services.availability_service import AvailabilityService 
from services.booking_service import BookingService
from services.payment_service import PaymentService
from entities.client import Client
from entities.service import Service
from entities.timeslot import TimeSlot

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
       print(services)
       
    elif choice == "2":
        userid = input("Enter userId: ")
        name = input("Enter name: ")
        email = input("Enter email: ")
        service_choice = input("Enter Service: ") #in phase 2 this will be changed to actually create the service object, for now it assume this does that 
        slot = input("Enter TimeSlot: ") #in phase 2 this will be changed to actually create the timeslot object, for now it assume this does that 

        services = available_services.browse_services() 
        if service_choice in services:
            consultant = service_choice.consultant #consultant that provide that service 
        else:
            raise Exception("Invalid Service")
        

        client = Client(userid,name,email)
        book = booking_service.create_booking(client,consultant,service_choice,slot)


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


        




