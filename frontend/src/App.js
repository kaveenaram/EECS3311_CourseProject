import { BrowserRouter as Router, Routes, Route, useNavigate } from 'react-router-dom';
import Home from './pages/Home';
import ClientLogin from './pages/ClientLogin';
import ConsultantLogin from './pages/ConsultantLogin';
import ConsultantDashboard from './pages/ConsultantDashboard';
import AdminLogin from './pages/AdminLogin';
import AdminDashboard from './pages/AdminDashboard';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/client-login" element={<ClientLogin />} />
        <Route path="/consultant-login" element={<ConsultantLoginWrapper />} />
        <Route path="/consultant-dashboard" element={<ConsultantDashboard />} />
        <Route path="/admin-login" element={<AdminLogin />} />
        <Route path="/admin-dashboard" element={<AdminDashboard />} />
      </Routes>
    </Router>
  );
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