import {BrowserRouter as Router, Routes, Route} from 'react-router-dom';
import Home from './pages/Home';
import ClientLogin from './pages/ClientLogin';
import ConsultantLogin from './pages/ConsultantLogin';
import ConsultantDashboard from './pages/ConsultantDashboard';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/client-login" element={<ClientLogin />} />
        <Route path="/consultant-login" element={<ConsultantLogin />} />
        <Route path="/consultant-dashboard" element={<ConsultantDashboard />} />
      </Routes>
    </Router>
  );
}

export default App;
