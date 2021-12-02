import instance from "./init";

export default {
    getJobs: async (pageNumber) => {
        const response = await instance.get(`/api/jobs/get-jobs?page=${pageNumber}`);
        return response.data;
    },
    getJob: async (jobUid) => {
        const response = await instance.post(`/api/job/${jobUid}`);
        return response.data;
    }
}