import instance from "./init";

export default {
    getJobs: async (data) => {
        const response = await instance.post(`/api/jobs/get-jobs`, data);
        return response.data;
    },
    getJob: async (jobUid) => {
        const response = await instance.post(`/api/job/${jobUid}`);
        return response.data;
    },
    getFiltredJobs: async (filters) => {
        const response = await instance.post(`/api/jobs/get-filtred-jobs`, filters)
    }
}