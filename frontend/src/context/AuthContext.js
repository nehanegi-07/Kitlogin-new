import React, { createContext, useContext, useState } from 'react'
import { useHistory } from 'react-router-dom'
import { publicFetch } from 'services/Authentication.Services'


const AuthContext = createContext()
const { Provider } = AuthContext

const AuthProvider = ({ children }) => {
    const history = useHistory();

    const token = localStorage.getItem("token");
    const userInfo = localStorage.getItem('userInfo');


    const [authState, setAuthState] = useState({ token, userInfo: userInfo ? JSON.parse(userInfo) : {} });

    const setAuthInfo = ({ token, userInfo }) => {
        localStorage.setItem('token', token);
        localStorage.setItem('userInfo', JSON.stringify(userInfo))

        setAuthState({ token, userInfo })
    }


    const logoout = async () => {
        try {
            localStorage.removeItem('token');
            localStorage.removeItem('userInfo');
            setAuthState({});
            history.push('/login')

        } catch (err) {
            console.log(err);
        }
    }

    const isAuthenticated = () => {
        if (!authState.token) {
            return false
        };

        return true;
    }

    const getAccessToken = () => localStorage.getItem('token')

    return <Provider value={{ 
            authState, 
            setAuthState: authInfo => setAuthInfo(authInfo), 
            isAuthenticated, 
            logoout, 
            getAccessToken }}>
                {children}
            </Provider>
}

function useAuth(){
    const context = useContext(AuthContext);

    if(!context){
        throw new Error(`useAuth must be used inside the AuthProvider`);
    }

    return context;
}


export {AuthProvider, useAuth}