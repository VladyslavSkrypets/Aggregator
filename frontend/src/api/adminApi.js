import instance from "./init";

export default {
    login: async (data) => {
        const response = await instance.post('/api/admin/login', data);
        return response.data
    },

    runParser: async (data) => {
        const response = await instance.post('/api/admin/run-gathers', data);
        return response.data
    },

    getAdminInfo: async () => {
        const response = await instance.post('/api/admin/get-admin-info');
        return response.data
    }
}