import axios from "axios";

const API_URL = "http://127.0.0.1:8000";

export const uploadAndRankResumes = async (formData) => {
  const response = await axios.post(`${API_URL}/rank_resumes/`, formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return response.data.results;
};
