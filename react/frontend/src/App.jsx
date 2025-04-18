import "./App.css";
import Home from './pages/Home.jsx';
import { useRoutes } from "react-router-dom";
import Signup from './pages/Signup.jsx';
import Dashboard from './pages/Dashboard.jsx';
import Login from './pages/Login.jsx';

function App() {
  let element = useRoutes([
    {
      path: "/",
      element: <Home />,
    },
    {
      path: "/login",
      element: <Login />,
    },
    {
      path: "/dashboard",
      element: <Dashboard />,
    },
    {
      path: "/signup",
      element: <Signup />,
    }
  ]);
  return (
    <div>
        {element}
    </div>
  );
}

export default App;
