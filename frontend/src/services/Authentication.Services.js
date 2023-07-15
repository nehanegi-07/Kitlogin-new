import axios from 'axios';

const API_URL = process.env.REACT_APP_API_KEY


export const publicFetch = axios.create({
    baseURL: API_URL
})


export const login = async (userData) => {
    const loginUserState = await publicFetch.post('login/dj-rest-auth/login/', userData);
    return loginUserState;
}


export const register = async (userData) => {
    const RegisterUserState = await axios.post(`https://ghostman2311-scaling-disco-v5rj74j57pvfxprq-8080.preview.app.github.dev/register`, userData);
    return RegisterUserState;
};


export const contract = async (payload) => {
    const contractData = await publicFetch.post('sca/contract/', payload);
    return contractData;
}
