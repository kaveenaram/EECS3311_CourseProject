import { useNavigate } from "react-router-dom";
import "./ConsultantLogin.css";

function ConsultantLogin(){
    const navigate = useNavigate();

    return(
        <div className="full-page">
            <div className="login-box text-white">
                <h2 className="mb-5 text-white text-center">Consultant Login</h2>
                <input className="form-control" placeholder="username"/>
                <input className="form-control" placeholder="password" type="password"/>
                <button className="btn btn-light mt-3" onClick={()=>navigate('/consultant-dashboard')}>Login</button>
            </div>
        </div>
    );
}

export  default ConsultantLogin;