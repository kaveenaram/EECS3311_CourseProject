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


    while True:
        choice = input("Select Option: ")

        if choice == "1":
           services = available_services.browse_services()
           for s in services:
               print(s)

        elif choice == "2":
            userid = input("Enter userId: ")
            name = input("Enter name: ")
            email = input("Enter email: "); 
            password = input("Enter Password: ") #will do the encrypting of password on phaser 2 
            
            #service selection
            service_choice = input("Enter Service: ") #in phase 2 this will be changed to actually create the service object, for now it assume this does that 
            
            services = available_services.browse_services() 
            #finding the service object 
            selected_service = None 
            for s in services:
             if s.serviceName == service_choice:
                selected_service =s
                break
            
            if selected_service:
                consultant = selected_service.consultant
            else:
                raise Exception("Invalid Service")



            #showing user the available timeslots 
            available_slots = consultant.get_available_timeslots()
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
            client = Client(userid,name,email,password)
            book = booking_service.create_booking(client,consultant,selected_service,timeslot)

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
            print("Goodbye")
            break

        else:
            print("Invalid Choice")

if __name__ == "__main__":
    main()


        




