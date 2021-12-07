import instance from "./init";

export default {
    getJobs: async (data) => {
        const response = await instance.post(`/api/jobs/get-jobs`, data);
        return response.data;
    },
    getJob: async (jobUid, source) => {
        const response = await instance.post(`/api/job/${jobUid}?utm_source=${source}`);
        return response.data;
    },
    getFiltredJobs: async (filters) => {
        const response = await instance.post(`/api/jobs/get-filtred-jobs`, filters)
    }
}