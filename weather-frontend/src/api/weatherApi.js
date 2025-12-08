import axiosClient from "./axiosClient";

const weatherApi = {
  getCurrent: (lat, lon) =>
    axiosClient.get(`/weather/current`, { params: { lat, lon } }),

  getForecast: (lat, lon) =>
    axiosClient.get(`/weather/week`, { params: { lat, lon } }),
};

export default weatherApi;