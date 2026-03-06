# Team9_Phase1 EECS-3311 Course Project

## Architecture Overview
- Layered structure:
  - Entities: domain objects and simple behaviors ([`backend/entities/booking.Booking`](backend/entities/booking.py), [`backend/entities/timeslot.TimeSlot`](backend/entities/timeslot.py), [`backend/entities/client.Client`](backend/entities/client.py), [`backend/entities/consultant.Consultant`](backend/entities/consultant.py)).
  - Patterns:
    - Observer components in [`backend/patterns/observer`](backend/patterns/observer).
    - State components in [`backend/patterns/state`](backend/patterns/state).
    - Strategy components (payment) in [`backend/patterns/strategy`](backend/patterns/strategy).
  - Services: use-case orchestration ([`backend/services/booking_service.BookingService`](backend/services/booking_service.py), [`backend/services/payment_service.PaymentService`](backend/services/payment_service.py), [`backend/services/availability_service.AvailabilityService`](backend/services/availability_service.py)).
  - Entry point: [`backend/main.py`](backend/main.py)

  ## Design Patterns Used and Locations
- State pattern
  - Interface: [`backend.patterns.state.booking_state.BookingState`](backend/patterns/state/booking_state.py)
  - Concrete states: [`backend/patterns/state/requested_state.RequestedState`](backend/patterns/state/requested_state.py), [`backend/patterns/state/confirmed_state.ConfirmedState`](backend/patterns/state/confirmed_state.py), [`backend/patterns/state/pending_payment_state.PendingPaymentState`](backend/patterns/state/pending_payment_state.py), [`backend/patterns/state/paid_state.PaidState`](backend/patterns/state/paid_state.py), [`backend/patterns/state/rejected_state.RejectedState`](backend/patterns/state/rejected_state.py), [`backend/patterns/state/cancelled_state.CancelledState`](backend/patterns/state/cancelled_state.py), [`backend/patterns/state/completed_state.CompletedState`](backend/patterns/state/completed_state.py)
  - Owner: `Booking` entity ([`backend/entities/booking.Booking`](backend/entities/booking.py))
- Observer pattern
  - Subject API: [`backend/patterns/observer/subject.Subject`](backend/patterns/observer/subject.py)
  - Observer API: [`backend/patterns/observer/observer.Observer`](backend/patterns/observer/observer.py)
  - Concrete notifier: [`backend/patterns/observer/notification_service.NotificationService`](backend/patterns/observer/notification_service.py)
  - Used to broadcast booking lifecycle events (reject/confirm/cancel/paid/complete).
- Strategy pattern
  - Interface: [`backend/patterns/strategy/payment_method.PaymentMethod`](backend/patterns/strategy/payment_method.py)
  - Implementations: [`backend/patterns/strategy/credit_card.CreditCard`](backend/patterns/strategy/credit_card.py), [`backend/patterns/strategy/debit_card.DebitCard`](backend/patterns/strategy/debit_card.py), [`backend/patterns/strategy/paypal.Paypal`](backend/patterns/strategy/paypal.py), [`backend/patterns/strategy/bank_transfer.BankTransfer`](backend/patterns/strategy/bank_transfer.py)
  - Used by [`backend/services/payment_service.PaymentService`](backend/services/payment_service.py)

## How To Run
https://github.com/kaveenaram/EECS3311_CourseProject
- Please make sure your Python version is up to date before proceeding
- Download or clone the GitHub Repository
- Using the terminal, direct yourself to the EECS3311_CourseProject directory
- Run python backend/main.py in the terminal
- For Phase 1, log in using the provided test users as creating a user is not yet supported

## Main Contributions

### Kaveena Ramkissoon — Booking Lifecycle (State Pattern Owner), UML Case Diagram, README.md, main.py
 Use Cases Covered:
 - UC2 Request Booking
 - UC3 Cancel Booking
 - UC9 Accept/Reject Booking
 - UC10 Complete Booking

### Dulja Ranathunga — Payment System (Strategy Pattern Owner), UML Case Diagram, main.py
Use Cases Covered:
- UC5 Process Payment
- UC6 Manage Payment Methods
- UC7 View Payment History

### Ha An Do — Availability & Core Entities, UML Class Diagram
Use Cases Covered:
- UC1 Browse Services
- UC4 View Booking History
- UC8 Manage Availability
    
### Meleena Subasinghe — Admin + Policies + Notifications (Observer Pattern Owner), UML Class Diagram
Use Cases Covered:
- UC11 Approve Consultant
- UC12 Define Policies
