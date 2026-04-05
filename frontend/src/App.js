import { BrowserRouter as Router, Routes, Route, useNavigate } from 'react-router-dom';

import Home from './pages/Home';
import ClientLogin from './pages/ClientLogin';
import ConsultantLogin from './pages/ConsultantLogin';
import ConsultantDashboard from './pages/ConsultantDashboard';
import ConsultantSignup from "./pages/ConsultantSignup";


import ClientDashboard from './pages/ClientDashboard';
import BrowseServicesPage from './pages/BrowseServicesPage';
import BookingHistoryPage from './pages/BookingHistoryPage';
import PaymentPage from './pages/PaymentPage';

import AdminLogin from './pages/AdminLogin';
import AdminDashboard from './pages/AdminDashboard';


// Chatbot
import ChatWidget from './components/ChatWidget';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />

        {/* Client */}
        <Route path="/client-login" element={<ClientLoginWrapper />} />
        <Route path="/client-dashboard" element={<ClientDashboard />} />
        <Route path="/services" element={<BrowseServicesPage />} />
        <Route path="/bookings" element={<BookingHistoryPage />} />
        <Route path="/payments" element={<PaymentPage />} />

        {/* Consultant */}
        <Route path="/consultant-login" element={<ConsultantLoginWrapper />} />
        <Route path="/consultant-dashboard" element={<ConsultantDashboard />} />
        <Route path="/consultant-signup" element={<ConsultantSignup />} />

        {/* Admin */}
        <Route path="/admin-login" element={<AdminLogin />} />
        <Route path="/admin-dashboard" element={<AdminDashboard />} />
      </Routes>

      {/* global chatbot */}
      <ChatWidget />
    </Router>
  );
}


// Client login wraper
function ClientLoginWrapper() {
  const navigate = useNavigate();

  const handleLoginSuccess = () => {
    navigate('/client-dashboard');
  };

  return <ClientLogin onLoginSuccess={handleLoginSuccess} />;
}

// Wrapper to use useNavigate inside the Route
function ConsultantLoginWrapper() {
  const navigate = useNavigate();

  const handleLoginSuccess = (consultant) => {
    console.log("Logged in consultant:", consultant);
    // Redirect to dashboard
    navigate('/consultant-dashboard');
  };

  return <ConsultantLogin onLoginSuccess={handleLoginSuccess} />;
}

export default App;
