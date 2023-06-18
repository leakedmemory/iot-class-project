import axios from "axios";

export const api = axios.create({
    baseURL: "https://projetoiot-linux-function-app.azurewebsites.net/api",
});
