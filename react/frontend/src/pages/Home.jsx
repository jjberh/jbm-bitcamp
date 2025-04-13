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

        {/* Navigation to Signup */}
        <Link to="/signup">
          <button>Get Started</button>
        </Link>

        <h5>Already created account? Log in</h5>
      </div>
    </>
  );
};

export default Home;
