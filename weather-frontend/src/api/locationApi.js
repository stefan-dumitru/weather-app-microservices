import axiosClient from "./axiosClient";

const locationApi = {
  getLocations: () => axiosClient.get("/location/"),
  addLocation: (data) => axiosClient.post("/location/", data),
  deleteLocation: (id) => axiosClient.delete(`/location/${id}`),
  updateLocation: (id, data) => axiosClient.put(`/location/${id}`, data),
};

export default locationApi;