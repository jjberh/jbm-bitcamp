import { Link } from 'react-router-dom';
import "./Home.css";

const Home = () => {
  return (
    <>
      <div>
        <header className="dashboard-header">
          <div className="header-overlay">
            <h1 className="header-title">Welcome to the Dashboard</h1>
          </div>
        </header>

        <div className="home-buttons">
          {/* Navigation to Signup */}
          <Link to="/signup">
            <button className="home-btn">Get Started</button>
          </Link>

          <div className="login-section">
            <p>Already have an account?</p>
            <Link to="/login">
              <button className="home-btn login-btn">Log In</button>
            </Link>
          </div>
        </div>
      </div>
    </>
  );
};

export default Home;
