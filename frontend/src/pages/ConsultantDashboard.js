import AvailabilityManager from "../components/AvailabilityManager";
import BookingRequests from "../components/BookingRequests";
import ScheduleView from "../components/ScheduleView";

function ConsultantDashboard(){
    return (
        <div>
            <h1>Consultant Dashboard</h1>
            <AvailabilityManager/>
            <BookingRequests/>
            <ScheduleView/>
        </div>
    );
}

export default ConsultantDashboard;