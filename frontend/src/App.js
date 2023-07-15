import React from "react";
import Login from "./pages/Login";
import { ThemeProvider } from "@mui/material/styles";
import { BrowserRouter as Router, Route } from "react-router-dom";
import theme from "assets/theme";
import themeDark from "assets/theme-dark";
import { useMaterialUIController } from "context";
import SignUp from "pages/SignUp";
import Dashboard from "pages/Dashboard";
import AddCreditCard from "pages/AddCreditCard";
import { AuthProvider } from "context/AuthContext";
import { Switch, Redirect } from "react-router-dom";
import { useAuth } from "context/AuthContext";

const UnauthenticatedRoutes = () => {
  return (
    <Switch>
      <Route path="/login" component={Login} />
      <Route path="/signup" component={SignUp} />
      <Route path="*" component={() => <div>Page Not Found</div>} />
    </Switch>
  );
};

const AuthenticatedRoutes = ({ children, ...rest }) => {
  const auth = useAuth();
  return (
    <Route
      {...rest}
      render={() => {
        return auth.isAuthenticated() ? <>{children}</> : <Redirect to="/login" />;
      }}
    />
  );
};

const AppRoutes = () => {
  console.log('approutes')
  return (
    <React.Fragment>
      <Switch>
      
        <AuthenticatedRoutes exact path="/">
          <Dashboard />
        </AuthenticatedRoutes>
        <AuthenticatedRoutes path="/checkout">
          <AddCreditCard />
        </AuthenticatedRoutes>
        <UnauthenticatedRoutes />
      </Switch>
    </React.Fragment>
  );
};

function App() {
  const [controller, dispatch] = useMaterialUIController();
  const { direction, darkMode } = controller;

  console.log('here');

  return (
    <ThemeProvider theme={darkMode ? themeDark : theme}>
      <div className="App">
        <Router>
          <AuthProvider>
            <AppRoutes/>
          </AuthProvider>
        </Router>
      </div>
    </ThemeProvider>
  );
}

export default App;
