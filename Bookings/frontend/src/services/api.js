import axios from "axios";

const api = axios.create({
    baseURL: "http://127.0.0.1:5000"
});

api.interceptors.request.use((request) => {

    console.log(
        "Starting Request:",
        request.url
    );

    return request;

});

export default api;