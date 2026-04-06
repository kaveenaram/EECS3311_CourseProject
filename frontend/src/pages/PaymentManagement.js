import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getPayments } from "../services/api";

export default function PaymentManagement() {
  const [payments, setPayments] = useState([]);
  const [paymentMethods, setPaymentMethods] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showAddMethod, setShowAddMethod] = useState(false);
  const [newMethod, setNewMethod] = useState({
    type: "credit_card",
    cardNumber: "",
    cardHolder: "",
    expiryDate: "",
    cvv: ""
  });
  const navigate = useNavigate();
  const clientId = localStorage.getItem("client_id");

  useEffect(() => {
    async function fetchData() {
      if (!clientId) {
        setError("You must be logged in to view payment information.");
        setLoading(false);
        return;
      }

      try {
        setError(null);
        const paymentsData = await getPayments(clientId);
        
        if (!Array.isArray(paymentsData)) {
          setPayments([]);
        } else {
          setPayments(paymentsData);
        }

        // Load payment methods from localStorage
        const savedMethods = localStorage.getItem(`paymentMethods_${clientId}`);
        if (savedMethods) {
          setPaymentMethods(JSON.parse(savedMethods));
        } else {
          setPaymentMethods([]);
        }
        
        setLoading(false);
      } catch (err) {
        console.error("Error fetching data:", err);
        setError("Failed to load payment information.");
        setLoading(false);
      }
    }

    fetchData();
  }, [clientId]);

  const handleAddPaymentMethod = () => {
    if (!newMethod.cardNumber || !newMethod.cardHolder || !newMethod.expiryDate || !newMethod.cvv) {
      alert("Please fill in all payment method fields");
      return;
    }

    // Basic validation
    if (newMethod.cardNumber.length < 13 || newMethod.cardNumber.length > 19) {
      alert("Card number must be 13-19 digits");
      return;
    }

    if (newMethod.cvv.length !== 3 && newMethod.cvv.length !== 4) {
      alert("CVV must be 3 or 4 digits");
      return;
    }

    const method = {
      id: `pm_${Date.now()}`,
      type: newMethod.type,
      cardNumber: `****-****-****-${newMethod.cardNumber.slice(-4)}`,
      cardHolder: newMethod.cardHolder,
      expiryDate: newMethod.expiryDate,
      addedDate: new Date().toLocaleDateString()
    };

    const updatedMethods = [...paymentMethods, method];
    setPaymentMethods(updatedMethods);
    localStorage.setItem(`paymentMethods_${clientId}`, JSON.stringify(updatedMethods));

    // Reset form
    setNewMethod({
      type: "credit_card",
      cardNumber: "",
      cardHolder: "",
      expiryDate: "",
      cvv: ""
    });
    setShowAddMethod(false);
    alert("Payment method added successfully!");
  };

  const handleDeletePaymentMethod = (methodId) => {
    if (!window.confirm("Are you sure you want to delete this payment method?")) {
      return;
    }

    const updatedMethods = paymentMethods.filter(m => m.id !== methodId);
    setPaymentMethods(updatedMethods);
    localStorage.setItem(`paymentMethods_${clientId}`, JSON.stringify(updatedMethods));
    alert("Payment method deleted successfully!");
  };

  if (loading) {
    return (
      <div className="container mt-5 text-center">
        <p>Loading payment information...</p>
      </div>
    );
  }

  // Calculate totals
  const totalPaid = payments
    .filter(p => p.status === 'COMPLETED')
    .reduce((sum, p) => sum + (parseFloat(p.amount) || 0), 0);

  return (
    <div style={{ padding: "20px" }}>
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h1>Payment Management</h1>
        <button className="btn btn-secondary" onClick={() => navigate("/client-dashboard")}>
          Back
        </button>
      </div>

      {error && (
        <div className="alert alert-danger" role="alert">
          {error}
        </div>
      )}

      {/* Payment Summary */}
      <div className="row mb-4">
        <div className="col-md-6">
          <div className="card bg-success text-white">
            <div className="card-body">
              <h5 className="card-title">Total Paid</h5>
              <h2 className="card-text">${totalPaid.toFixed(2)}</h2>
              <small>{payments.filter(p => p.status === 'COMPLETED').length} payment(s)</small>
            </div>
          </div>
        </div>
        <div className="col-md-6">
          <div className="card bg-info text-white">
            <div className="card-body">
              <h5 className="card-title">Payment Methods</h5>
              <h2 className="card-text">{paymentMethods.length}</h2>
              <small>Saved payment method(s)</small>
            </div>
          </div>
        </div>
      </div>

      {/* Payment History */}
      <div className="card mb-4">
        <div className="card-header bg-dark text-white">
          <h5>Payment History</h5>
        </div>
        <div className="card-body">
          {payments.length === 0 ? (
            <div className="alert alert-info">No payments found</div>
          ) : (
            <div className="table-responsive">
              <table className="table table-striped table-hover">
                <thead className="table-light">
                  <tr>
                    <th>Date</th>
                    <th>Amount</th>
                    <th>Status</th>
                    <th>Booking ID</th>
                  </tr>
                </thead>
                <tbody>
                  {payments.map((p) => (
                    <tr key={p.payment_id}>
                      <td>{p.created_at ? new Date(p.created_at).toLocaleDateString() : "N/A"}</td>
                      <td>${parseFloat(p.amount || 0).toFixed(2)}</td>
                      <td>
                        <span className={`badge ${p.status === 'COMPLETED' ? 'bg-success' : 'bg-danger'}`}>
                          {p.status}
                        </span>
                      </td>
                      <td>{p.booking_id}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>

      {/* Payment Methods */}
      <div className="card">
        <div className="card-header bg-dark text-white d-flex justify-content-between align-items-center">
          <h5 className="mb-0">Saved Payment Methods</h5>
          <button 
            className="btn btn-sm btn-primary" 
            onClick={() => setShowAddMethod(!showAddMethod)}
          >
            {showAddMethod ? "Cancel" : "+ Add New Method"}
          </button>
        </div>
        <div className="card-body">
          {/* Add New Payment Method Form */}
          {showAddMethod && (
            <div className="card mb-3 bg-light">
              <div className="card-body">
                <h6>Add Payment Method</h6>
                <div className="mb-3">
                  <label>Payment Type:</label>
                  <select 
                    className="form-control"
                    value={newMethod.type}
                    onChange={(e) => setNewMethod({...newMethod, type: e.target.value})}
                  >
                    <option value="credit_card">Credit Card</option>
                    <option value="debit_card">Debit Card</option>
                    <option value="paypal">PayPal</option>
                  </select>
                </div>
                <div className="mb-3">
                  <label>Card Number:</label>
                  <input 
                    type="text"
                    className="form-control"
                    placeholder="1234 5678 9012 3456"
                    value={newMethod.cardNumber}
                    onChange={(e) => setNewMethod({...newMethod, cardNumber: e.target.value.replace(/\D/g, '')})}
                  />
                </div>
                <div className="mb-3">
                  <label>Card Holder Name:</label>
                  <input 
                    type="text"
                    className="form-control"
                    placeholder="John Doe"
                    value={newMethod.cardHolder}
                    onChange={(e) => setNewMethod({...newMethod, cardHolder: e.target.value})}
                  />
                </div>
                <div className="row">
                  <div className="col-md-6 mb-3">
                    <label>Expiry Date (MM/YY):</label>
                    <input 
                      type="text"
                      className="form-control"
                      placeholder="12/25"
                      value={newMethod.expiryDate}
                      onChange={(e) => setNewMethod({...newMethod, expiryDate: e.target.value})}
                      maxLength="5"
                    />
                  </div>
                  <div className="col-md-6 mb-3">
                    <label>CVV:</label>
                    <input 
                      type="password"
                      className="form-control"
                      placeholder="123"
                      value={newMethod.cvv}
                      onChange={(e) => setNewMethod({...newMethod, cvv: e.target.value.replace(/\D/g, '')})}
                      maxLength="4"
                    />
                  </div>
                </div>
                <button 
                  className="btn btn-primary"
                  onClick={handleAddPaymentMethod}
                >
                  Save Payment Method
                </button>
              </div>
            </div>
          )}

          {/* Payment Methods List */}
          {paymentMethods.length === 0 ? (
            <div className="alert alert-info">No payment methods saved yet</div>
          ) : (
            <div className="row">
              {paymentMethods.map((method) => (
                <div key={method.id} className="col-md-6 mb-3">
                  <div className="card">
                    <div className="card-body">
                      <h6 className="card-title">{method.type.replace('_', ' ').toUpperCase()}</h6>
                      <p className="card-text">
                        <strong>{method.cardNumber}</strong><br/>
                        {method.cardHolder}<br/>
                        <small className="text-muted">Expires: {method.expiryDate}</small>
                      </p>
                      <small className="text-muted">Added: {method.addedDate}</small>
                      <div className="mt-2">
                        <button 
                          className="btn btn-danger btn-sm"
                          onClick={() => handleDeletePaymentMethod(method.id)}
                        >
                          Delete
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
