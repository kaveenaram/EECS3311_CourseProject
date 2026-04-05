from database.db import SessionLocal
from patterns.state.paid_state import PaidState
from patterns.state.requested_state import RequestedState
from patterns.state.booking_state import BookingState
from services.availability_service import AvailabilityService 
from services.booking_service import BookingService
from services.payment_service import PaymentService
from entities.client import Client
from entities.consultant import Consultant
from entities.service import Service
from entities.timeslot import TimeSlot

from patterns.strategy.credit_card import CreditCard
from patterns.strategy.debit_card import DebitCard
from patterns.strategy.paypal import Paypal
from patterns.strategy.bank_transfer import BankTransfer

"""
main.py serves as the entry point for the consulting booking system.
main.py uses terminal commands to demonstrate:

• Browsing services
• Booking a session
• Consultant accepting/rejecting bookings
• Processing payment (simulation)

in phase 2, this will be replaced by a proper database	
for now, this is for demonstration purposes only
there exists default consultant in availability_service.py for the example

"""

users = {
    "client1": Client("client1", "client", "client@domain.com", "password"),
    "consultant1": Consultant("consultant1", "consultant", "consultant@domain.com", "password")	
}

db = SessionLocal()
available_services = AvailabilityService(db)
booking_service = BookingService(db)
payment_service = PaymentService(db)

def main():

    print("=====================================")
    print("Welcome to Consulting Booking System\n")
    print("=====================================")

    print("Please log in to continue:\n")

    user_id = input("User ID: ").strip() #ignore white space
    password = input("Password: ").strip() #ignore white space

    consultant1 = users["consultant1"]
    consultant1.approved = True #for demo purposes, we approve the consultant by default

    if (user_id not in users or not users[user_id].logIn(password)):
        print("Invalid credentials. Exiting...")
        return
    # if the logged in user is a client, show the client menu

    if isinstance(users[user_id], Client):
        client_menu(user_id)
    # if the logged in user is a consultant, show the consultant menu
    elif isinstance(users[user_id], Consultant):
        consultant_menu(user_id)
	
def client_menu(user_id):
    client = users[user_id]

    print("1. Browse our Services")
    print("2. Book a Session")
    print("3. Make a Payment")
    print("4. Log Out")

    while True:
        choice = input("Select Option: ")
        services = available_services.browse_services()

        if choice == "1":
           for s in services:
               print(s)

        elif choice == "2":
            #service selection
            service_choice = input("Enter Service: ") #in phase 2 this will be changed to actually create the service object, for now it assume this does that 
            
            #finding the service object 
            selected_service = None 
            for s in services:
             if s.serviceName == service_choice:
                selected_service = s
                break
            
            if selected_service:
                consultant = selected_service.consultant
                available_slots = consultant.get_available_timeslots()
            else:
                raise Exception("Invalid Service")

            #showing user the available timeslots 
            if not available_slots:
                print("No available timeslots for this consultant.")
                continue
            
            print("\nAvailable timeslots:")
            for slot in available_slots:
                print(f"{slot.slot_id}: {slot.start_time} - {slot.end_time}")
            
            slot_id = input("Enter TimeSlot id: ") #in phase 2 this will be changed to actually create the timeslot object, for now it assume this does that 

            timeslot = None
            for slot in available_slots:
                if slot.slot_id == slot_id:
                    timeslot = slot
                    break

            if not timeslot:
                print("Invalid timeslot selected.")
                continue

            #creating the client and booking
            
            book = booking_service.create_booking(client, consultant, selected_service, timeslot)

            #consultant accepting or rejecting 
            available_slot = consultant.get_available_timeslots()

            if timeslot in available_slot:
                booking_service.confirm_booking(book)
                print(f"Booking confirmed! Booking ID: {book.booking_id}")
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
            amount = float(input("Enter amount: "))

            booking = booking_service.get_booking(booking_id)

            if not booking:
                raise Exception("booking id entered is invalid")

            #create correct payment strategy 
            if payment_choice == "1":
                card_number = input("Enter credit card number: ")
                expiry = input("Enter expiry date (MM/YY): ")
                cvv = input("Enter CVV: ")
                payment_method = CreditCard(card_number, expiry, cvv)
            elif payment_choice == "2":
                card_number = input("Enter credit card number: ")
                expiry = input("Enter expiry date (MM/YY): ")
                cvv = input("Enter CVV: ")
                payment_method = DebitCard(card_number, expiry, cvv)
            elif payment_choice == "3":
                email = input("Enter email: ")
                payment_method = Paypal(email)
            elif payment_choice == "4":
                account_no = input("Enter Account No: ")
                routing_no = input("Enter Routing No: ")
                payment_method = BankTransfer(account_no, routing_no)
            else:
                raise Exception("Invalid payment method")

            result = payment_service.process_payment(booking, payment_method, amount)

            if result is not None:
                print("Payment Processed Successfully")
            else:
                print("Something went Wrong, please try again")

        elif choice == "4":
            print("Logging out...")
            break

        else:
            print("Invalid Choice")

        
def consultant_menu(user_id):
    consultant = users[user_id]

    print("1. View Bookings")
    print("2. Add Service")
    print("3. Add Availability")
    print("4. View Services")
    print("5. View Availability")
    print("6. Log Out")

    test_booking_created = False #for demo purposes, we create a test booking for the consultant to show how accepting/rejecting and completing works, and also to show how payment works after accepting the booking. This variable ensures that the test booking is only created once.
    
    while True:

        # consultant will be given test booking for example purposes, to show how the consultant can accept/reject and complete the booking, and also to show how payment works after accepting the booking. 
        if not test_booking_created and (consultant.timeslots and consultant.services):
            test_booking = booking_service.create_booking(users["client1"], consultant, available_services.services[0], consultant.timeslots[0])
            test_booking_created = True

        choice = input("\nSelect Option: \n")

        if choice == "1":
            if not consultant.bookings:
                print("No bookings yet.")
                continue
            else:
                for b in consultant.bookings:
                    print(f"Booking ID: {b.booking_id}, Client: {b.client.name}, Service: {b.service.serviceName}, Time: {b.timeslot.start_time} - {b.timeslot.end_time}, State: {b._state}")

                print("\nEnter Booking ID to accept/reject/complete or press Enter to go back:")
                booking_id = input("Booking ID: ").strip() #ignore white space
                if booking_id:
                    booking = booking_service.get_booking(booking_id)

                    if not booking or booking not in consultant.bookings:
                        print("Invalid Booking ID")
                        continue

                    print("1. Accept Booking")
                    print("2. Reject Booking")
                    print("3. Complete Booking")
                    action_choice = input("Select Option: ")

                    state: BookingState = booking.get_state()

                    if action_choice == "1":
                        if isinstance(state, RequestedState):
                            booking_service.confirm_booking(booking)
                            print("Booking Accepted")
                        else:
                            print("Booking is not requested and cannot be accepted.")
                    elif action_choice == "2":
                        if isinstance(state, RequestedState):
                            booking_service.reject_booking(booking)
                            print("Booking Rejected")
                        else:
                            print("Booking cannot be rejected.")
                    elif action_choice == "3":
                        if isinstance(state, PaidState):
                            if booking_service.complete_booking(booking):
                                print("Booking Completed")
                            else:
                                print("Booking cannot be completed. Please ensure the booking has been paid.")
                        else:
                            print("Only paid bookings can be completed.")
                    else:
                        print("Invalid Choice")
                else:
                    continue 

        elif choice == "2":
            print("Add existing service or create new service?")
            print("1. Add existing service")
            print("2. Create new service")
            service_choice = input("Select Option: ")
            if service_choice == "1":
                services = available_services.browse_services()
                if not services:
                    print("No services available to add. Please create a new service.")
                    continue
                print("Available Services:")
                for s in services:
                    print(f"Service ID: {s.service_id}, Name: {s.serviceName}, Duration: {s.duration} minutes, Price: ${s.price}")
                service_id = input("Enter Service ID to add: ")
                selected_service = None
                for s in services:
                    if s.service_id == service_id:
                        selected_service = s
                        break
                if selected_service:
                    consultant.add_service(selected_service)
                    print("Service Added")
                else:
                    print("Invalid Service ID")
            elif service_choice == "2":
                service_name = input("Enter Service Name: ")
                duration = int(input("Enter Service Duration (in minutes): "))
                price = float(input("Enter Service Price: "))
                service = Service(service_id=f"s{len(available_services.services) + 1}", serviceName=service_name, duration=duration, price=price, consultant=consultant)

                available_services.add_service(service)
                consultant.add_service(service)

                print("Service Added")

        elif choice == "3":
            start_time = input("Enter Start Time: ")
            end_time = input("Enter End Time: ")
            timeslot = TimeSlot(f"ts{len(consultant.timeslots) + 1}", start_time=start_time, end_time=end_time)
            available_services.add_timeslot(consultant, timeslot)
            print("Availability Added")
        
        elif choice == "4":
            if not consultant.services:
                print("No services yet.")
                continue
            print("Viewing Services...")
            for service in consultant.get_services():
                print(f"Service ID: {service.service_id}, Name: {service.serviceName}, Duration: {service.duration} minutes, Price: ${service.price}")

        elif choice == "5":
            if not consultant.get_available_timeslots():
                print("No available timeslots yet.")
                continue
            print("Viewing Availability...")
            for slot in available_services.get_available_slots(consultant):
                print(f"Time Slot ID: {slot.slot_id}, Start Time: {slot.start_time}, End Time: {slot.end_time}")

        elif choice == "6":
            print("Logging out...")
            break

        else:
            print("Invalid Choice") 
        
if __name__ == "__main__":
     main()