import axiosClient from "./axiosClient";

const alertApi = {
  getAlerts: () => axiosClient.get("/alerts/"),
  addAlert: (data) => axiosClient.post("/alerts/", data),
  toggleAlert: (id) => axiosClient.patch(`/alerts/${id}/toggle`),
  deleteAlert: (id) => axiosClient.delete(`/alerts/${id}`),
};

export default alertApi;