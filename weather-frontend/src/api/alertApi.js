import axiosClient from "./axiosClient";

const alertApi = {
  getAlerts: () => axiosClient.get("/alerts/"),
  addAlert: (data) => axiosClient.post("/alerts/", data),
};

export default alertApi;