import axios from "axios";

const instance = axios.create({ baseURL: process.env.REACT_APP_SERVER });
instance.defaults.headers.common["Content-Type"] = "application/json";

export default instance;
